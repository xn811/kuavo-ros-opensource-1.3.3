#include <pinocchio/fwd.hpp> // forward declarations must be included first.
#include <pinocchio/algorithm/frames.hpp>
#include <pinocchio/algorithm/kinematics.hpp>
#include "mobile_manipulator_controllers/mobileManipulatorControllerBase.h"

#include <std_msgs/Float64MultiArray.h>
#include <ocs2_sqp/SqpMpc.h>
#include <ocs2_ddp/GaussNewtonDDP_MPC.h>
#include <ocs2_core/thread_support/ExecuteAndSleep.h>
#include <ocs2_core/thread_support/SetThreadPriority.h>

#include <ocs2_ros_interfaces/synchronized_module/RosReferenceManager.h>
#include <sensor_msgs/JointState.h>
#include <chrono>
#include <thread>

namespace mobile_manipulator_controller
{
  MobileManipulatorControllerBase::MobileManipulatorControllerBase(ros::NodeHandle &nh, const std::string& taskFile, const std::string& libFolder, 
    const std::string& urdfFile, MpcType mpcType, int freq, 
    bool dummySimBase, bool dummySimArm, bool visualizeMm)
  : controllerNh_(nh)
  , mpcType_(mpcType)
  , freq_(freq)
  , dummySim_(dummySimBase)
  , dummySimArm_(dummySimArm)
  , visualizeMm_(visualizeMm)
  {
    ros_logger_ = std::make_unique<humanoid::TopicLogger>(nh);
    mpcPolicyPublisher_ = controllerNh_.advertise<ocs2_msgs::mpc_flattened_controller>(robotName_ + "_mpc_policy", 1, true);
    mmEefPosesPublisher_ = controllerNh_.advertise<std_msgs::Float64MultiArray>(robotName_ + "_eef_poses", 10, true);
    mmPlanedTrajPublisher_ = nh.advertise<visualization_msgs::MarkerArray>(robotName_ + "/planed_two_hand_trajectory", 10);// TODO: 考虑去除
    setupMobileManipulatorInterface(taskFile, libFolder, urdfFile, mpcType);
    setupMpc();
    setupMrt();
    starting();
    ROS_INFO("MobileManipulatorControllerBase initialized.");
  }

  MobileManipulatorControllerBase::~MobileManipulatorControllerBase()
  {
    // 安全地停止MPC线程
    controllerRunning_ = false;
    mpcRunning_ = false;
    updateRunning_ = false;
    
    // 通知线程停止
    {
      std::lock_guard<std::mutex> lock(mpcThreadMutex_);
      mpcThreadPaused_ = false;  // 确保线程不会被暂停在条件变量上
      mpcThreadCondition_.notify_all();
    }
    
    if (mpcThread_.joinable())
    {
      mpcThread_.join();
    }
    
    std::cerr << "########################################################################";
    std::cerr << "\n### MPC Benchmarking";
    std::cerr << "\n###   Maximum : " << mpcTimer_.getMaxIntervalInMilliseconds() << "[ms].";
    std::cerr << "\n###   Average : " << mpcTimer_.getAverageInMilliseconds() << "[ms]." << std::endl;
    std::cerr << "########################################################################";
  }

  void MobileManipulatorControllerBase::setupMobileManipulatorInterface(const std::string &taskFile, const std::string &libFolder, const std::string &urdfFile, MpcType mpcType)
  {
    mpcType_ = mpcType;
    mobileManipulatorInterface_ = std::make_shared<ocs2::mobile_manipulator::MobileManipulatorInterface>(taskFile, libFolder, urdfFile);
    info_ = mobileManipulatorInterface_->getManipulatorModelInfo();
    // Visualization
    visualizationPtr_ = std::make_shared<MobileManipulatorVisualization>(controllerNh_, *mobileManipulatorInterface_);
    pinocchioInterface_ptr_.reset(new PinocchioInterface(mobileManipulatorInterface_->getPinocchioInterface()));
    pinocchioMappingPtr_ = std::make_unique<MobileManipulatorPinocchioMapping>(mobileManipulatorInterface_->getManipulatorModelInfo());
    eeSpatialKinematicsPtr_ = std::make_shared<PinocchioEndEffectorSpatialKinematics>(mobileManipulatorInterface_->getPinocchioInterface(), *pinocchioMappingPtr_.get(), 
                                                                                      mobileManipulatorInterface_->getManipulatorModelInfo().eeFrames);
    eeSpatialKinematicsPtr_->setPinocchioInterface(*pinocchioInterface_ptr_.get());
  }

  void MobileManipulatorControllerBase::setupMpc()
  {
    if(mpcType_ == MpcType::SQP)
      mpc_ = std::make_shared<SqpMpc>(mobileManipulatorInterface_->mpcSettings(), mobileManipulatorInterface_->sqpSettings(),
                                      mobileManipulatorInterface_->getOptimalControlProblem(), mobileManipulatorInterface_->getInitializer());
    else if(mpcType_ == MpcType::DDP)
      mpc_ = std::make_shared<GaussNewtonDDP_MPC>(mobileManipulatorInterface_->mpcSettings(), mobileManipulatorInterface_->ddpSettings(), mobileManipulatorInterface_->getRollout(),
                                                  mobileManipulatorInterface_->getOptimalControlProblem(), mobileManipulatorInterface_->getInitializer());

    else
    {
      ROS_ERROR_STREAM("MPC type: " << static_cast<int>(mpcType_) << " is not supported.");
      throw std::runtime_error("Invalid MPC type.");
    }
    // ROS ReferenceManager
    auto rosReferenceManagerPtr = std::make_shared<ocs2::RosReferenceManager>(robotName_, mobileManipulatorInterface_->getReferenceManagerPtr());
    rosReferenceManagerPtr->subscribe(controllerNh_);
    mpc_->getSolverPtr()->setReferenceManager(rosReferenceManagerPtr);
    observationPublisher_ = controllerNh_.advertise<ocs2_msgs::mpc_observation>(robotName_ + "_mpc_observation", 1);
  }

  void MobileManipulatorControllerBase::setupMrt()
  {
    mpcMrtInterface_ = std::make_shared<MPC_MRT_Interface>(*mpc_);
    // mpcMrtInterface_->initRollout(&mobileManipulatorInterface_->getRollout());
    mpcTimer_.reset();

    controllerRunning_ = true;
    mpcThread_ = std::thread([&]()
                             {
    while (controllerRunning_) {
      try {
        // Check if thread should be paused
        {
          std::unique_lock<std::mutex> lock(mpcThreadMutex_);
          mpcThreadCondition_.wait(lock, [&]() { return !mpcThreadPaused_.load() || !controllerRunning_.load(); });
          
          if (!controllerRunning_) {
            break;
          }
        }
        executeAndSleep(
            [&]() {
              if (mpcRunning_) {
                mpcTimer_.startTimer();
                mpcMrtInterface_->advanceMpc();
                mpcTimer_.endTimer();
              }
            },
            mobileManipulatorInterface_->mpcSettings().mpcDesiredFrequency_);
      } catch (const std::exception& e) {
        controllerRunning_ = false;
        ROS_ERROR_STREAM("[Ocs2 MPC thread] Error : " << e.what());
      }
    } });
    setThreadPriority(mobileManipulatorInterface_->sqpSettings().threadPriority, mpcThread_);
  }

  ocs2::vector_t MobileManipulatorControllerBase::getTargetFromState(const vector_t& state)
  {
    // initial command
    const size_t baseDim = info_.stateDim - info_.armDim;
    const size_t hand_dim = 7;
    ocs2::vector_t initTarget(baseDim + 2*hand_dim);
    initTarget.head(baseDim) = state.head(baseDim);
    const vector_t eefPoses = getMMEefPose(state);
    if(eefPoses.size() != 2*hand_dim)
      ROS_ERROR_STREAM("eefPoses.size() != 2*hand_dim");
    initTarget.tail(2*hand_dim) = eefPoses;
    return initTarget;
  }

  void MobileManipulatorControllerBase::starting()
  {
    SystemObservation initial_observation;
    initial_observation.time = 0.0;
    initial_observation.state.setZero(info_.stateDim);
    initial_observation.input.setZero(info_.inputDim);

    const size_t baseDim = info_.stateDim - info_.armDim;
    const size_t hand_dim = 7;
    mmObservationDummy_ = initial_observation;
    std::cout << "Initial time: " << initial_observation.time << std::endl;
    std::cout << "Initial state: " << initial_observation.state.transpose() << std::endl;
    std::cout << "Initial state size: " << initial_observation.state.size() << std::endl;
    std::cout << "Initial input size: " << initial_observation.input.size() << std::endl;

    const ocs2::vector_t initTarget = getTargetFromState(initial_observation.state);
    std::cout << "initial target base:       " << initTarget.segment(0, baseDim).transpose() << std::endl;
    std::cout << "initial target hand left:  " << initTarget.segment(baseDim, hand_dim).transpose() << std::endl;
    std::cout << "initial target hand right: " << initTarget.segment(baseDim+hand_dim, hand_dim).transpose() << std::endl;
    const vector_t zeroInput = vector_t::Zero(info_.inputDim);
    const TargetTrajectories target_trajectories({initial_observation.time, initial_observation.time+1.0}, {initTarget, initTarget}, {zeroInput, zeroInput});
    // Set the first observation and command and wait for optimization to finish
    mpcMrtInterface_->setCurrentObservation(initial_observation);
    mpcMrtInterface_->getReferenceManager().setTargetTrajectories(target_trajectories);
    ROS_INFO_STREAM("Waiting for the initial policy ...");
    while (!mpcMrtInterface_->initialPolicyReceived() && ros::ok())
    {
      mpcMrtInterface_->advanceMpc();
      ros::WallRate(mobileManipulatorInterface_->mpcSettings().mrtDesiredFrequency_).sleep();
    }
    ROS_INFO_STREAM("Initial policy received.");
    mpcRunning_ = true;
    updateRunning_ = true;
  }

  int MobileManipulatorControllerBase::update(const vector_t& externalState, vector_t& nextState)
  {
    vector_t optimizedInput = vector_t::Zero(info_.inputDim);
    return update(externalState, nextState, optimizedInput);
  }

  int MobileManipulatorControllerBase::update(const vector_t& externalState, vector_t& nextState, vector_t& optimizedInput)
  {
    if(externalState.size() != info_.stateDim || nextState.size() != info_.stateDim)
    {
      ROS_ERROR_STREAM("externalState.size() != info_.stateDim");
      return -2;
    }
    if(!updateRunning_)
      return -1;
    const size_t baseDim = info_.stateDim - info_.armDim;
    // Update the current state of the system
    SystemObservation obs = mmObservationDummy_;
    obs.time = mmObservationDummy_.time;
    obs.state = externalState;
    obs.input.setZero();
    if(dummySim_)
      obs.state.head(baseDim) = mmObservationDummy_.state.head(baseDim);
    if(dummySimArm_)
      obs.state.tail(info_.armDim) = mmObservationDummy_.state.tail(info_.armDim);

    // ros_logger_->publishVector("/mm/state_before_mpc", obs.state);
    mpcMrtInterface_->setCurrentObservation(obs);

    const scalar_t dt = 1.0 / static_cast<scalar_t>(freq_);
    vector_t optimizedStateMrt, optimizedInputMrt;
    getOptimizedStateAndInput(obs, optimizedStateMrt, optimizedInputMrt);
    ros_logger_->publishVector("/mm/optimized_state", optimizedStateMrt);
    mmObservationDummy_ = forwardSimulation(obs, dt);

    nextState = mmObservationDummy_.state;
    optimizedInput = optimizedInputMrt;
    // ros_logger_->publishVector("/mm/state_after_mpc", nextState);

    const vector_t eefPoses = getMMEefPose(mmObservationDummy_.state);
    publishEefPoses(eefPoses);
    // publish eef poses
    if(mmPlanedTrajQueue_.size() < 200)
      mmPlanedTrajQueue_.push_back(eefPoses);
    else
      mmPlanedTrajQueue_.pop_front();
    // visualize
    mmPlanedTrajPublisher_.publish(getVisualizeTrajectoryMsg(mmPlanedTrajQueue_, {0.1, 0.9, 0.1, 1.0}));
    return 0;
  }

  void MobileManipulatorControllerBase::getOptimizedStateAndInput(const SystemObservation& currentObservation, vector_t& optimizedStateMrt, vector_t& optimizedInputMrt)
  {
    // Load the latest MPC policy
    if (mpcMrtInterface_->updatePolicy())
    {
      auto &policy = mpcMrtInterface_->getPolicy();
      auto &command = mpcMrtInterface_->getCommand();
      auto &performance_indices = mpcMrtInterface_->getPerformanceIndices();
      auto &state_trajectory = policy.stateTrajectory_;

      ocs2_msgs::mpc_flattened_controller mpcPolicyMsg =
          createMpcPolicyMsg(policy, command, performance_indices);

      // publish the message
      mpcPolicyPublisher_.publish(mpcPolicyMsg);
      if(visualizeMm_)
        visualizationPtr_->update(currentObservation, policy, command);
    }
    // Evaluate the current policy
    size_t mode;
    mpcMrtInterface_->evaluatePolicy(currentObservation.time, currentObservation.state, optimizedStateMrt, optimizedInputMrt, mode);
    observationPublisher_.publish(ros_msg_conversions::createObservationMsg(currentObservation));
  };

  ocs2_msgs::mpc_flattened_controller MobileManipulatorControllerBase::createMpcPolicyMsg(const PrimalSolution &primalSolution,
                                                                             const CommandData &commandData,
                                                                             const PerformanceIndex &performanceIndices)
  {
    ocs2_msgs::mpc_flattened_controller mpcPolicyMsg;

    mpcPolicyMsg.initObservation = ros_msg_conversions::createObservationMsg(commandData.mpcInitObservation_);
    mpcPolicyMsg.planTargetTrajectories = ros_msg_conversions::createTargetTrajectoriesMsg(commandData.mpcTargetTrajectories_);
    mpcPolicyMsg.modeSchedule = ros_msg_conversions::createModeScheduleMsg(primalSolution.modeSchedule_);
    mpcPolicyMsg.performanceIndices =
        ros_msg_conversions::createPerformanceIndicesMsg(commandData.mpcInitObservation_.time, performanceIndices);

    switch (primalSolution.controllerPtr_->getType())
    {
    case ControllerType::FEEDFORWARD:
      mpcPolicyMsg.controllerType = ocs2_msgs::mpc_flattened_controller::CONTROLLER_FEEDFORWARD;
      break;
    case ControllerType::LINEAR:
      mpcPolicyMsg.controllerType = ocs2_msgs::mpc_flattened_controller::CONTROLLER_LINEAR;
      break;
    default:
      throw std::runtime_error("MPC_ROS_Interface::createMpcPolicyMsg: Unknown ControllerType");
    }

    // maximum length of the message
    const size_t N = primalSolution.timeTrajectory_.size();

    mpcPolicyMsg.timeTrajectory.clear();
    mpcPolicyMsg.timeTrajectory.reserve(N);
    mpcPolicyMsg.stateTrajectory.clear();
    mpcPolicyMsg.stateTrajectory.reserve(N);
    mpcPolicyMsg.data.clear();
    mpcPolicyMsg.data.reserve(N);
    mpcPolicyMsg.postEventIndices.clear();
    mpcPolicyMsg.postEventIndices.reserve(primalSolution.postEventIndices_.size());

    // time
    for (auto t : primalSolution.timeTrajectory_)
    {
      mpcPolicyMsg.timeTrajectory.emplace_back(t);
    }

    // post-event indices
    for (auto ind : primalSolution.postEventIndices_)
    {
      mpcPolicyMsg.postEventIndices.emplace_back(static_cast<uint16_t>(ind));
    }

    // state
    for (size_t k = 0; k < N; k++)
    {
      ocs2_msgs::mpc_state mpcState;
      mpcState.value.resize(primalSolution.stateTrajectory_[k].rows());
      for (size_t j = 0; j < primalSolution.stateTrajectory_[k].rows(); j++)
      {
        mpcState.value[j] = primalSolution.stateTrajectory_[k](j);
      }
      mpcPolicyMsg.stateTrajectory.emplace_back(mpcState);
    } // end of k loop

    // input
    for (size_t k = 0; k < N; k++)
    {
      ocs2_msgs::mpc_input mpcInput;
      mpcInput.value.resize(primalSolution.inputTrajectory_[k].rows());
      for (size_t j = 0; j < primalSolution.inputTrajectory_[k].rows(); j++)
      {
        mpcInput.value[j] = primalSolution.inputTrajectory_[k](j);
      }
      mpcPolicyMsg.inputTrajectory.emplace_back(mpcInput);
    } // end of k loop

    // controller
    scalar_array_t timeTrajectoryTruncated;
    std::vector<std::vector<float> *> policyMsgDataPointers;
    policyMsgDataPointers.reserve(N);
    for (auto t : primalSolution.timeTrajectory_)
    {
      mpcPolicyMsg.data.emplace_back(ocs2_msgs::controller_data());

      policyMsgDataPointers.push_back(&mpcPolicyMsg.data.back().data);
      timeTrajectoryTruncated.push_back(t);
    } // end of k loop

    // serialize controller into data buffer
    primalSolution.controllerPtr_->flatten(timeTrajectoryTruncated, policyMsgDataPointers);

    return std::move(mpcPolicyMsg);
  }

  SystemObservation MobileManipulatorControllerBase::forwardSimulation(const SystemObservation& currentObservation, scalar_t dt) {
    SystemObservation nextObservation;
    nextObservation.time = currentObservation.time + dt;
    if (mpcMrtInterface_->isRolloutSet()) {  // If available, use the provided rollout as to integrate the dynamics.
      // ROS_INFO_STREAM("Using rollout to integrate the dynamics.");
      mpcMrtInterface_->rolloutPolicy(currentObservation.time, currentObservation.state, dt, nextObservation.state, nextObservation.input,
                        nextObservation.mode);
    } else {  // Otherwise, we fake integration by interpolating the current MPC policy at t+dt
      // ROS_INFO_STREAM("Using MPC policy to integrate the dynamics.");
      mpcMrtInterface_->evaluatePolicy(currentObservation.time + dt, currentObservation.state, nextObservation.state, nextObservation.input,
                          nextObservation.mode);
    }

    return std::move(nextObservation);
  }


  vector_t MobileManipulatorControllerBase::getMMEefPose(const vector_t& state)
  {
    vector_t eefPoses;// pos(x,y,z) + quat(x,y,z,w)
    const auto& model = pinocchioInterface_ptr_->getModel();
    auto& data = pinocchioInterface_ptr_->getData();
    const auto q = pinocchioMappingPtr_->getPinocchioJointPosition(state);

    pinocchio::forwardKinematics(model, data, q);
    pinocchio::updateFramePlacements(model, data);

    const auto eefPositions = eeSpatialKinematicsPtr_->getPosition(state);
    const auto eefOrientations = eeSpatialKinematicsPtr_->getOrientation(state);

    if(eefPositions.size() != eefOrientations.size())
      ROS_ERROR("[MobileManipulatorControllerBase] eefPositions.size() != eefOrientations.size()");
    eefPoses.resize(7*eefPositions.size());
    for(int i = 0; i < eefPositions.size(); i++)
    {
      eefPoses.segment<7>(7*i).head(3) = eefPositions[i];
      eefPoses.segment<7>(7*i).tail(4) = eefOrientations[i].coeffs();
    }
    return std::move(eefPoses);
  }

  // 可视化轨迹
  visualization_msgs::MarkerArray MobileManipulatorControllerBase::getVisualizeTrajectoryMsg(const std::deque<Eigen::VectorXd>& twoHandPoseTrajectory, std::vector<double> rgba)
  {
    visualization_msgs::MarkerArray marker_array;
    visualization_msgs::Marker marker_l, marker_r;
    marker_l.header.frame_id = "mm/world";
    marker_l.header.stamp = ros::Time::now();
    // marker_l.ns = "l_hand";
    marker_l.id = 0;
    marker_l.type = visualization_msgs::Marker::LINE_STRIP;
    marker_l.action = visualization_msgs::Marker::ADD;
    marker_l.scale.x = 0.01;    // 设置线宽
    marker_l.color.r = rgba[0]; // 设置颜色
    marker_l.color.g = rgba[1]; // 设置颜色
    marker_l.color.b = rgba[2]; // 设置颜色
    marker_l.color.a = rgba[3]; // 设置透明度

    marker_r = marker_l;
    // marker_r.ns = "r_hand";
    marker_r.id = 1;
    auto getTraj = [&](visualization_msgs::Marker &marker, bool isLeft)
    {
      for(const auto& pose : twoHandPoseTrajectory)
      {
        const auto hand_pose = (isLeft ? pose.head(7) : pose.tail(7));
        geometry_msgs::Point p;
        p.x = hand_pose(0);
        p.y = hand_pose(1);
        p.z = hand_pose(2);
        marker.points.push_back(p);
      }
    };
    // left hand
    getTraj(marker_l, true);
    marker_array.markers.push_back(marker_l);
    // right hand
    getTraj(marker_r, false);
    marker_array.markers.push_back(marker_r);

    return std::move(marker_array);
  }

  void MobileManipulatorControllerBase::publishEefPoses(const vector_t& eefPoses)
  {
    std_msgs::Float64MultiArray eefPosesMsg;
    eefPosesMsg.data.resize(eefPoses.size());
    for(size_t i = 0; i < eefPoses.size(); i++)
      eefPosesMsg.data[i] = eefPoses[i];
    mmEefPosesPublisher_.publish(eefPosesMsg);
  }

  int MobileManipulatorControllerBase::reset(const vector_t& externalState)
  {
    if(externalState.size() != info_.stateDim)
    {
      ROS_ERROR_STREAM("externalState.size() != info_.stateDim");
      return -1;
    }
    
    ROS_INFO("Starting MPC reset process...");
    
    // 暂停MPC线程运行
    mpcRunning_ = false;
    updateRunning_ = false;
    
    // 使用条件变量暂停MPC线程，避免硬编码等待时间
    {
      std::unique_lock<std::mutex> lock(mpcThreadMutex_);
      mpcThreadPaused_ = true;
      
      // 通知线程暂停
      mpcThreadCondition_.notify_all();
      
      ROS_INFO("MPC thread paused successfully");
    }
    
    // 给线程一点时间来响应暂停请求
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    
    // 强制重置MRT_BASE状态
    try
    {
      mpcMrtInterface_->reset();
      ROS_INFO("MRT_BASE reset completed");
    }
    catch(const std::exception& e)
    {
      ROS_ERROR_STREAM("Failed to reset MRT_BASE: " << e.what());
      return -2;
    }

    SystemObservation resetObservation;
    resetObservation.time = mmObservationDummy_.time; // 使用当前时间,避免时间跳变
    resetObservation.state = externalState;
    resetObservation.input.setZero(info_.inputDim);
    resetMpcToGivenState(resetObservation);

    // 重新启动MPC线程
    {
      std::lock_guard<std::mutex> lock(mpcThreadMutex_);
      mpcThreadPaused_ = false;
      mpcRunning_ = true;
      updateRunning_ = true;
      mpcThreadCondition_.notify_all();
    }
    
    // 清理轨迹队列
    mmPlanedTrajQueue_.clear();

    // 重置observation，保证update函数使用重置后的observation
    mmObservationDummy_ = resetObservation;
    
    ROS_INFO("MPC reset process completed successfully");
    return 0;
  }

  // reset observation
  void MobileManipulatorControllerBase::resetMpcToGivenState(const SystemObservation& resetObservation)
  {
    mpcMrtInterface_->setCurrentObservation(resetObservation);
    // reset mpc
    const ocs2::vector_t externalTarget = getTargetFromState(resetObservation.state);
    const TargetTrajectories target_trajectories({resetObservation.time, resetObservation.time+1.0}, {externalTarget, externalTarget}, {resetObservation.input, resetObservation.input});
    ROS_INFO_STREAM("Resetting MPC to state: " << resetObservation.state.transpose());
    ROS_INFO_STREAM("Target trajectories after reset: " << externalTarget.transpose());
    mpcMrtInterface_->resetMpcNode(target_trajectories);

    std::cout << "Waiting for the initial policy after reset ..." << std::endl;
    auto start_time = std::chrono::steady_clock::now();
    while (!mpcMrtInterface_->initialPolicyReceived() && ros::ok())
    {
      if(std::chrono::steady_clock::now() - start_time > std::chrono::seconds(5)) {
        ROS_ERROR("Timeout while waiting for initial policy after reset.");
        break;
      }
      // 确保使用重置后的观测值
      mpcMrtInterface_->setCurrentObservation(resetObservation);
      mpcMrtInterface_->advanceMpc();
      ros::WallRate(mobileManipulatorInterface_->mpcSettings().mrtDesiredFrequency_).sleep();
    }
    std::cout << "Initial policy received after " << std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - start_time).count() << " milliseconds" << std::endl;    
    if(mpcMrtInterface_->updatePolicy())
    {
      std::cout << "Policy updated successfully" << std::endl;
    
      auto policy = mpcMrtInterface_->getPolicy();
      std::cout << "Initial policy after reset start at: " << policy.timeTrajectory_[0] << " and end at: " << policy.timeTrajectory_.back() << std::endl;
    }
  };

  int MobileManipulatorControllerBase::setTargetTrajectory(const TargetTrajectories& targetTrajectories)
  {
    mpcMrtInterface_->getReferenceManager().setTargetTrajectories(targetTrajectories);
    return 0;
  }

} // namespace mobile_manipulator