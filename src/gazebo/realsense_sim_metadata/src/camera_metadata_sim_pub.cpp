#include <ros/ros.h>
#include <kuavo_msgs/Metadata.h>
#include <string>
#include <sstream>

class MetadataSimPublisher {
private:
    ros::NodeHandle nh_;
    std::string camera_name_;
    
    ros::Publisher color_pub_;
    ros::Publisher depth_pub_;
    ros::Publisher infra1_pub_;
    ros::Publisher infra2_pub_;
    
    ros::Timer timer_;
    uint64_t frame_number_;

    // 创建模拟的JSON metadata
    std::string createMetadataJson(const std::string& stream_type, uint64_t frame_number) {
        std::stringstream ss;
        uint64_t current_time = ros::Time::now().toNSec();
        uint32_t hw_timestamp = frame_number * 16667; // 模拟60fps的硬件时间戳 (1/60 ≈ 0.01667秒)
        
        if (stream_type == "Color") {
            ss << "{"
               << "\"frame_number\":" << frame_number << ","
               << "\"clock_domain\":\"global_time\","
               << "\"frame_timestamp\":" << current_time / 1e3 << "," // 转换为微秒
               << "\"frame_counter\":" << frame_number << ","
               << "\"hw_timestamp\":" << hw_timestamp << ","
               << "\"auto_exposure\":1,"
               << "\"time_of_arrival\":" << (current_time / 1e6) << "," // 转换为毫秒
               << "\"backend_timestamp\":0,"
               << "\"actual_fps\":60,"
               << "\"brightness\":0,"
               << "\"contrast\":50,"
               << "\"saturation\":64,"
               << "\"sharpness\":50,"
               << "\"auto_white_balance_temperature\":1,"
               << "\"backlight_compensation\":0,"
               << "\"hue\":0,"
               << "\"gamma\":300,"
               << "\"manual_white_balance\":4600,"
               << "\"power_line_frequency\":3,"
               << "\"low_light_compensation\":0,"
               << "\"raw_frame_size\":614400"
               << "}";
        } else {
            // depth和infrared的metadata
            ss << "{"
               << "\"frame_number\":" << frame_number << ","
               << "\"clock_domain\":\"global_time\","
               << "\"frame_timestamp\":" << current_time / 1e3 << ","
               << "\"frame_counter\":" << frame_number << ","
               << "\"hw_timestamp\":" << hw_timestamp << ","
               << "\"sensor_timestamp\":" << (hw_timestamp - 16000) << ","
               << "\"actual_exposure\":31979,"
               << "\"gain_level\":16,"
               << "\"auto_exposure\":1,"
               << "\"time_of_arrival\":" << (current_time / 1e6) << ","
               << "\"backend_timestamp\":0,"
               << "\"actual_fps\":60,"
               << "\"frame_laser_power\":" << (frame_number % 2 ? 0 : 150) << ","
               << "\"frame_laser_power_mode\":" << (frame_number % 2 ? 0 : 1) << ","
               << "\"exposure_priority\":1,"
               << "\"exposure_roi_left\":0,"
               << "\"exposure_roi_right\":847,"
               << "\"exposure_roi_top\":0,"
               << "\"exposure_roi_bottom\":479,"
               << "\"frame_emitter_mode\":" << (frame_number % 2 ? 0 : 1) << ","
               << "\"raw_frame_size\":814080,"
               << "\"gpio_input_data\":0,"
               << "\"sequence_name\":15,"
               << "\"sequence_id\":" << (frame_number % 2) << ","
               << "\"sequence_size\":2"
               << "}";
        }
        return ss.str();
    }

    void publishMetadata(const ros::TimerEvent&) {
        kuavo_msgs::Metadata msg;
        msg.header.stamp = ros::Time::now();
        frame_number_++;

        // 发布color metadata
        msg.header.frame_id = "camera_color_optical_frame";
        msg.json_data = createMetadataJson("Color", frame_number_);
        color_pub_.publish(msg);

        // 发布depth metadata
        msg.header.frame_id = "camera_depth_optical_frame";
        msg.json_data = createMetadataJson("Depth", frame_number_);
        depth_pub_.publish(msg);

        // 发布infra1 metadata
        msg.header.frame_id = "camera_infra1_optical_frame";
        msg.json_data = createMetadataJson("Infrared 1", frame_number_);
        infra1_pub_.publish(msg);

        // 发布infra2 metadata
        msg.header.frame_id = "camera_infra2_optical_frame";
        msg.json_data = createMetadataJson("Infrared 2", frame_number_);
        infra2_pub_.publish(msg);
    }

public:
    MetadataSimPublisher() : frame_number_(0) {
        ros::NodeHandle private_nh("~");  // 创建私有节点句柄用于获取私有参数
        
        // 获取参数，如果没有设置，默认使用 "camera"
        private_nh.param<std::string>("camera_name", camera_name_, "camera");

        // 创建发布者
        color_pub_ = nh_.advertise<kuavo_msgs::Metadata>(
            camera_name_ + "/color/metadata", 1);
        depth_pub_ = nh_.advertise<kuavo_msgs::Metadata>(
            camera_name_ + "/depth/metadata", 1);
        infra1_pub_ = nh_.advertise<kuavo_msgs::Metadata>(
            camera_name_ + "/infra1/metadata", 1);
        infra2_pub_ = nh_.advertise<kuavo_msgs::Metadata>(
            camera_name_ + "/infra2/metadata", 1);

        // 修改为60Hz发布频率
        timer_ = nh_.createTimer(ros::Duration(1.0/60.0), 
                               &MetadataSimPublisher::publishMetadata, this);

        ROS_INFO("Metadata simulator started for camera: %s at 60Hz", camera_name_.c_str());
    }
};

int main(int argc, char **argv) {
    ros::init(argc, argv, "camera_metadata_sim_pub");
    MetadataSimPublisher metadata_sim;
    ros::spin();
    return 0;
}