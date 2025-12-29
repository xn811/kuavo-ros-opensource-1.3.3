#include <boost/thread/recursive_mutex.hpp>
#include <gazebo/common/Plugin.hh>
#include <ros/ros.h>
#include "gazebo_ros_link_attacher.h"
#include "gazebo_ros_link_attacher/Attach.h"
#include "gazebo_ros_link_attacher/AttachRequest.h"
#include "gazebo_ros_link_attacher/AttachResponse.h"
#include "gazebo_ros_link_attacher/Grasp.h"
#include "gazebo_ros_link_attacher/GraspRequest.h"
#include "gazebo_ros_link_attacher/GraspResponse.h"
#include <ignition/math/Pose3.hh>
#include <cmath>
#include <sstream>
#include <XmlRpcValue.h>

namespace gazebo
{
  // Constructor
  GazeboRosLinkAttacher::GazeboRosLinkAttacher() :
    nh_("link_attacher_node"),
    grasp_nh_("kuavo_attacher_node"),
    max_attach_distance_(0.15),
    min_attach_distance_(0.0),
    min_grasp_distance_(0.0),
    max_grasp_distance_(0.15)
  {
  }

  // Destructor
  GazeboRosLinkAttacher::~GazeboRosLinkAttacher()
  {
  }

  void GazeboRosLinkAttacher::loadGraspConfig()
  {
    ros::NodeHandle nh;  // 使用全局命名空间
    
    // 加载机器人模型名称
    nh.param<std::string>("robot_model_name", robot_model_name_, "biped_s42");
    ROS_INFO_STREAM("[Grasp Service] Robot model name: " << robot_model_name_);
    
    // 加载最小抓取距离
    nh.param<double>("min_grasp_distance", min_grasp_distance_, 0.0);
    ROS_INFO_STREAM("[Grasp Service] Min grasp distance: " << min_grasp_distance_ << "m");
    
    // 加载最大抓取距离
    nh.param<double>("max_grasp_distance", max_grasp_distance_, 0.15);
    ROS_INFO_STREAM("[Grasp Service] Max grasp distance: " << max_grasp_distance_ << "m");
    
    // 加载手臂链接配置
    if (nh.hasParam("arm_links"))
    {
      XmlRpc::XmlRpcValue arm_links_param;
      nh.getParam("arm_links", arm_links_param);
      
      for (auto it = arm_links_param.begin(); it != arm_links_param.end(); ++it)
      {
        std::string arm = it->first;
        std::string link_name = static_cast<std::string>(it->second["link_name"]);
        arm_links_[arm] = link_name;
        ROS_INFO_STREAM("[Grasp Service] Arm " << arm << " -> " << link_name);
      }
    }
    else
    {
      // 默认配置
      arm_links_["left"] = "zarm_l7_link";
      arm_links_["right"] = "zarm_r7_link";
      ROS_INFO("[Grasp Service] Using default arm links config");
    }
    
    // 加载可抓取物品列表
    if (nh.hasParam("graspable_objects"))
    {
      XmlRpc::XmlRpcValue objects_param;
      nh.getParam("graspable_objects", objects_param);
      
      for (auto it = objects_param.begin(); it != objects_param.end(); ++it)
      {
        std::string obj_name = it->first;
        std::string link_name = static_cast<std::string>(it->second["link_name"]);
        graspable_objects_[obj_name] = link_name;
        ROS_INFO_STREAM("[Grasp Service] Graspable object: " << obj_name << " -> " << link_name);
      }
    }
    
    ROS_INFO_STREAM("[Grasp Service] Loaded " << graspable_objects_.size() << " graspable objects");
  }

  void GazeboRosLinkAttacher::Load(physics::WorldPtr _world, sdf::ElementPtr _sdf)
  {
    if (!ros::isInitialized())
    {
      ROS_FATAL_STREAM("A ROS node for Gazebo has not been initialized, unable to load plugin. "
        << "Load the Gazebo system plugin 'libgazebo_ros_api_plugin.so' in the gazebo_ros package)");
      return;
    }
    
    this->world = _world;
    this->physics = this->world->Physics();
    this->physics_mutex = this->physics->GetPhysicsUpdateMutex();

    // 从SDF参数读取attach服务的距离限制（仅用于attach/detach服务）
    if (_sdf->HasElement("min_attach_distance"))
    {
      this->min_attach_distance_ = _sdf->Get<double>("min_attach_distance");
    }
    if (_sdf->HasElement("max_attach_distance"))
    {
      this->max_attach_distance_ = _sdf->Get<double>("max_attach_distance");
    }
    ROS_INFO_STREAM("[Attach Service] Min attach distance: " << this->min_attach_distance_ << "m");
    ROS_INFO_STREAM("[Attach Service] Max attach distance: " << this->max_attach_distance_ << "m");

    // 加载抓取配置（grasp服务使用独立的距离参数）
    loadGraspConfig();

    this->attach_service_ = this->nh_.advertiseService("attach", &GazeboRosLinkAttacher::attach_callback, this);
    ROS_INFO_STREAM("Attach service at: " << this->nh_.resolveName("attach"));
    this->detach_service_ = this->nh_.advertiseService("detach", &GazeboRosLinkAttacher::detach_callback, this);
    ROS_INFO_STREAM("Detach service at: " << this->nh_.resolveName("detach"));
    this->grasp_service_ = this->grasp_nh_.advertiseService("grasp", &GazeboRosLinkAttacher::grasp_callback, this);
    ROS_INFO_STREAM("Grasp service at: " << this->grasp_nh_.resolveName("grasp"));
    ROS_INFO("Link attacher node initialized.");
  }

  double GazeboRosLinkAttacher::getDistance(std::string model1, std::string link1,
                                            std::string model2, std::string link2)
  {
    physics::ModelPtr m1 = this->world->ModelByName(model1);
    physics::ModelPtr m2 = this->world->ModelByName(model2);
    
    if (!m1)
    {
      ROS_ERROR_STREAM("Model '" << model1 << "' not found for distance calculation");
      return -1.0;
    }
    if (!m2)
    {
      ROS_ERROR_STREAM("Model '" << model2 << "' not found for distance calculation");
      return -1.0;
    }
    
    physics::LinkPtr l1 = m1->GetLink(link1);
    physics::LinkPtr l2 = m2->GetLink(link2);
    
    if (!l1)
    {
      ROS_ERROR_STREAM("Link '" << link1 << "' not found in model '" << model1 << "'");
      return -1.0;
    }
    if (!l2)
    {
      ROS_ERROR_STREAM("Link '" << link2 << "' not found in model '" << model2 << "'");
      return -1.0;
    }
    
    ignition::math::Pose3d pose1 = l1->WorldPose();
    ignition::math::Pose3d pose2 = l2->WorldPose();
    
    double dx = pose1.Pos().X() - pose2.Pos().X();
    double dy = pose1.Pos().Y() - pose2.Pos().Y();
    double dz = pose1.Pos().Z() - pose2.Pos().Z();
    
    return std::sqrt(dx*dx + dy*dy + dz*dz);
  }

  std::pair<std::string, double> GazeboRosLinkAttacher::findNearestObject(const std::string& arm)
  {
    std::string nearest_obj = "";
    double min_distance = std::numeric_limits<double>::max();
    
    auto arm_it = arm_links_.find(arm);
    if (arm_it == arm_links_.end())
    {
      ROS_ERROR_STREAM("Unknown arm: " << arm);
      return std::make_pair("", -1.0);
    }
    
    std::string arm_link = arm_it->second;
    
    for (const auto& obj : graspable_objects_)
    {
      std::string obj_name = obj.first;
      std::string obj_link = obj.second;
      
      double distance = getDistance(robot_model_name_, arm_link, obj_name, obj_link);
      
      if (distance >= 0 && distance < min_distance)
      {
        min_distance = distance;
        nearest_obj = obj_name;
      }
    }
    
    return std::make_pair(nearest_obj, min_distance);
  }

  bool GazeboRosLinkAttacher::attach(std::string model1, std::string link1,
                                     std::string model2, std::string link2)
  {
    fixedJoint j;
    if(this->getJoint(model1, link1, model2, link2, j)){
        ROS_INFO_STREAM("Joint already existed, reusing it.");
        j.joint->Attach(j.l1, j.l2);
        return true;
    }
    else{
        ROS_INFO_STREAM("Creating new joint.");
    }
    j.model1 = model1;
    j.link1 = link1;
    j.model2 = model2;
    j.link2 = link2;
    ROS_DEBUG_STREAM("Getting BasePtr of " << model1);
    physics::BasePtr b1 = this->world->ModelByName(model1);

    if (b1 == NULL){
      ROS_ERROR_STREAM(model1 << " model was not found");
      return false;
    }
    ROS_DEBUG_STREAM("Getting BasePtr of " << model2);
    physics::BasePtr b2 = this->world->ModelByName(model2);
    if (b2 == NULL){
      ROS_ERROR_STREAM(model2 << " model was not found");
      return false;
    }

    ROS_DEBUG_STREAM("Casting into ModelPtr");
    physics::ModelPtr m1(dynamic_cast<physics::Model*>(b1.get()));
    j.m1 = m1;
    physics::ModelPtr m2(dynamic_cast<physics::Model*>(b2.get()));
    j.m2 = m2;

    ROS_DEBUG_STREAM("Getting link: '" << link1 << "' from model: '" << model1 << "'");
    physics::LinkPtr l1 = m1->GetLink(link1);
    if (l1 == NULL){
      ROS_ERROR_STREAM(link1 << " link was not found");
      return false;
    }
    if (l1->GetInertial() == NULL){
        ROS_ERROR_STREAM("link1 inertia is NULL!");
    }
    else
        ROS_DEBUG_STREAM("link1 inertia is not NULL, for example, mass is: " << l1->GetInertial()->Mass());
    j.l1 = l1;
    ROS_DEBUG_STREAM("Getting link: '" << link2 << "' from model: '" << model2 << "'");
    physics::LinkPtr l2 = m2->GetLink(link2);
    if (l2 == NULL){
      ROS_ERROR_STREAM(link2 << " link was not found");
      return false;
    }
    if (l2->GetInertial() == NULL){
        ROS_ERROR_STREAM("link2 inertia is NULL!");
    }
    else
        ROS_DEBUG_STREAM("link2 inertia is not NULL, for example, mass is: " << l2->GetInertial()->Mass());
    j.l2 = l2;

    ROS_DEBUG_STREAM("Links are: "  << l1->GetName() << " and " << l2->GetName());

    ROS_DEBUG_STREAM("Creating revolute joint on model: '" << model1 << "'");
    j.joint = this->physics->CreateJoint("revolute", m1);
    this->joints.push_back(j);

    ROS_DEBUG_STREAM("Attach");
    j.joint->Attach(l1, l2);
    ROS_DEBUG_STREAM("Loading links");
    j.joint->Load(l1, l2, ignition::math::Pose3d());
    ROS_DEBUG_STREAM("SetModel");
    j.joint->SetModel(m2);

    ROS_DEBUG_STREAM("SetHightstop");
    j.joint->SetUpperLimit(0, 0);
    ROS_DEBUG_STREAM("SetLowStop");
    j.joint->SetLowerLimit(0, 0);
    ROS_DEBUG_STREAM("Init");
    j.joint->Init();
    ROS_INFO_STREAM("Attach finished.");

    return true;
  }

  bool GazeboRosLinkAttacher::detach(std::string model1, std::string link1,
                                     std::string model2, std::string link2)
  {
      fixedJoint j;
      if(this->getJoint(model1, link1, model2, link2, j)){
          boost::recursive_mutex::scoped_lock lock(*this->physics_mutex);
          j.joint->Detach();
          return true;
      }

    return false;
  }

  bool GazeboRosLinkAttacher::getJoint(std::string model1, std::string link1,
                                       std::string model2, std::string link2,
                                       fixedJoint &joint){
    fixedJoint j;
    for(std::vector<fixedJoint>::iterator it = this->joints.begin(); it != this->joints.end(); ++it){
        j = *it;
        if ((j.model1.compare(model1) == 0) && (j.model2.compare(model2) == 0)
                && (j.link1.compare(link1) == 0) && (j.link2.compare(link2) == 0)){
            joint = j;
            return true;
        }
    }
    return false;
  }

  bool GazeboRosLinkAttacher::attach_callback(gazebo_ros_link_attacher::Attach::Request &req,
                                              gazebo_ros_link_attacher::Attach::Response &res)
  {
    ROS_INFO_STREAM("Received request to attach model: '" << req.model_name_1
                    << "' using link: '" << req.link_name_1 << "' with model: '"
                    << req.model_name_2 << "' using link: '" <<  req.link_name_2 << "'");
    
    double distance = this->getDistance(req.model_name_1, req.link_name_1,
                                        req.model_name_2, req.link_name_2);
    
    if (distance < 0)
    {
      ROS_ERROR_STREAM("Could not calculate distance between links.");
      res.ok = false;
      res.message = "Could not calculate distance between links";
      return true;
    }
    
    ROS_INFO_STREAM("Distance between links: " << distance << "m (min: " << this->min_attach_distance_ << "m, max: " << this->max_attach_distance_ << "m)");
    
    if (distance < this->min_attach_distance_)
    {
      std::stringstream ss;
      ss << "Links too close! Distance: " << distance << "m (min: " << this->min_attach_distance_ << "m)";
      ROS_WARN_STREAM(ss.str());
      res.ok = false;
      res.message = ss.str();
      return true;
    }
    
    if (distance > this->max_attach_distance_)
    {
      std::stringstream ss;
      ss << "Links too far apart! Distance: " << distance << "m (max: " << this->max_attach_distance_ << "m)";
      ROS_WARN_STREAM(ss.str());
      res.ok = false;
      res.message = ss.str();
      return true;
    }
    
    if (! this->attach(req.model_name_1, req.link_name_1,
                       req.model_name_2, req.link_name_2)){
      ROS_ERROR_STREAM("Could not make the attach.");
      res.ok = false;
      res.message = "Could not make the attach";
    }
    else{
      ROS_INFO_STREAM("Attach was succesful");
      res.ok = true;
      res.message = "Attach successful";
    }
    return true;
  }

  bool GazeboRosLinkAttacher::detach_callback(gazebo_ros_link_attacher::Attach::Request &req,
                                              gazebo_ros_link_attacher::Attach::Response &res){
      ROS_INFO_STREAM("Received request to detach model: '" << req.model_name_1
                      << "' using link: '" << req.link_name_1 << "' with model: '"
                      << req.model_name_2 << "' using link: '" <<  req.link_name_2 << "'");
      if (! this->detach(req.model_name_1, req.link_name_1,
                         req.model_name_2, req.link_name_2)){
        ROS_ERROR_STREAM("Could not make the detach.");
        res.ok = false;
        res.message = "Could not make the detach";
      }
      else{
        ROS_INFO_STREAM("Detach was succesful");
        res.ok = true;
        res.message = "Detach successful";
      }
      return true;
  }

  bool GazeboRosLinkAttacher::grasp_callback(gazebo_ros_link_attacher::Grasp::Request &req,
                                             gazebo_ros_link_attacher::Grasp::Response &res)
  {
    std::string arm = req.arm;
    std::string action = req.action;
    
    // 转小写
    std::transform(arm.begin(), arm.end(), arm.begin(), ::tolower);
    std::transform(action.begin(), action.end(), action.begin(), ::tolower);
    
    ROS_INFO_STREAM("Grasp request: arm=" << arm << ", action=" << action);
    
    // 验证手臂参数
    if (arm != "left" && arm != "right")
    {
      res.ok = false;
      res.message = "Invalid arm: must be 'left' or 'right'";
      return true;
    }
    
    // 验证动作参数
    if (action != "grasp" && action != "release")
    {
      res.ok = false;
      res.message = "Invalid action: must be 'grasp' or 'release'";
      return true;
    }
    
    std::string arm_link = arm_links_[arm];
    
    if (action == "grasp")
    {
      // 检查该手是否已经抓着物品
      if (grasped_objects_.find(arm) != grasped_objects_.end() && !grasped_objects_[arm].empty())
      {
        res.ok = false;
        res.message = "Arm " + arm + " already holding: " + grasped_objects_[arm];
        res.object_name = grasped_objects_[arm];
        return true;
      }
      
      // 查找最近的物品
      auto result = findNearestObject(arm);
      std::string nearest_obj = result.first;
      double distance = result.second;
      
      res.distance = distance;
      res.object_name = nearest_obj;
      
      if (nearest_obj.empty())
      {
        res.ok = false;
        res.message = "No graspable objects found";
        return true;
      }
      
      // 检查距离 - 最小和最大限制
      if (distance < min_grasp_distance_)
      {
        std::stringstream ss;
        ss << "Object " << nearest_obj << " too close: " << distance << "m (min: " << min_grasp_distance_ << "m)";
        res.ok = false;
        res.message = ss.str();
        return true;
      }
      
      if (distance > max_grasp_distance_)
      {
        std::stringstream ss;
        ss << "Object " << " too far.";
        res.ok = false;
        res.message = ss.str();
        return true;
      }
      
      // 检查物品是否已被另一只手抓取
      std::string other_arm = (arm == "left") ? "right" : "left";
      if (grasped_objects_.find(other_arm) != grasped_objects_.end() && 
          grasped_objects_[other_arm] == nearest_obj)
      {
        res.ok = false;
        res.message = "Object " + nearest_obj + " already held by " + other_arm + " arm";
        return true;
      }
      
      // 执行抓取
      std::string obj_link = graspable_objects_[nearest_obj];
      if (attach(robot_model_name_, arm_link, nearest_obj, obj_link))
      {
        grasped_objects_[arm] = nearest_obj;
        res.ok = true;
        res.message = "Successfully grasped " + nearest_obj + " with " + arm + " arm";
        ROS_INFO_STREAM(res.message);
      }
      else
      {
        res.ok = false;
        res.message = "Failed to grasp " + nearest_obj;
        ROS_ERROR_STREAM(res.message);
      }
    }
    else  // release
    {
      // 检查该手是否抓着物品
      if (grasped_objects_.find(arm) == grasped_objects_.end() || grasped_objects_[arm].empty())
      {
        res.ok = false;
        res.message = "Arm " + arm + " is not holding anything";
        return true;
      }
      
      std::string object_name = grasped_objects_[arm];
      res.object_name = object_name;
      
      // 执行释放
      std::string obj_link = graspable_objects_[object_name];
      if (detach(robot_model_name_, arm_link, object_name, obj_link))
      {
        grasped_objects_[arm] = "";
        res.ok = true;
        res.message = "Successfully released " + object_name + " from " + arm + " arm";
        ROS_INFO_STREAM(res.message);
      }
      else
      {
        res.ok = false;
        res.message = "Failed to release " + object_name;
        ROS_ERROR_STREAM(res.message);
      }
    }
    
    return true;
  }

}
