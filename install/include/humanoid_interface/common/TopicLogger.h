#pragma once

#include "ros/ros.h"
#include "std_msgs/Float64MultiArray.h"
#include "std_msgs/Float64.h"
#include <unordered_map>
#include <string>
#include <ros/master.h>
#include <vector>
#include <string>
#include <rosbag/recorder.h>
#include <ros/callback_queue.h>
#include <ros/topic.h>
#include <ocs2_core/Types.h>

namespace ocs2
{
  namespace humanoid
  {
    class TopicLogger
    {
    public:
      TopicLogger();
      TopicLogger(ros::NodeHandle& input_nh);
      void predefinedTopics();
      
      void publishVector(const std::string &topic_name, const ocs2::vector_t &data, const std::string &label = "");

      void publishVector(const std::string &topic_name, const std::vector<double> &data, const std::string &label = "");
      void publishValue(const std::string &topic_name, const double &data);
      void publishVectorCallback(const std::string &topic_name, const ocs2::vector_t &data)
      {
        publishVector(topic_name, data, "");
      }

    private:
      ros::NodeHandle nh_;
      std::unordered_map<std::string, ros::Publisher> publishedTopics_;
      std::unordered_map<std::string, ros::Publisher> publishedValueTopics_;
    };

  }
}
