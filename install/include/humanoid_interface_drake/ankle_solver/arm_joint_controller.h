#pragma once
#include "Eigen/Core"
#include <iostream>

#include <drake/systems/framework/leaf_system.h>
#include <drake/systems/framework/context.h>
#include <drake/multibody/plant/multibody_plant.h>

using namespace Eigen;
using namespace drake;

namespace lower_leg
{

  class ArmJointController : public drake::systems::LeafSystem<double>
  {
  public:
    DRAKE_NO_COPY_NO_MOVE_NO_ASSIGN(ArmJointController)

    ArmJointController(multibody::MultibodyPlant<double> &plant, const std::vector<std::string> &cfg_str);
    void CalcArmState(Eigen::Vector4d &lower_qv, Eigen::Vector4d &ankle_motor_qv) const;
    void CalcArmStateQv(Eigen::Vector4d &lower_qv, Eigen::VectorXd &ankle_motor_qv) const;

  private:
    int nq_;
    int nv_;
    int i_j_l_arm_;
    int i_j_r_arm_;
    int i_roll_;
    int i_pitch_;
    int i_j_r_link, i_j_l_link;
    double l_Lkleft_;
    double l_Lkright_;
    double l_Armleft_;
    double l_Armright_;
    double qO_Armleft_; // this is "capital ou", not "zero"
    double qO_Armright_;
    double init_l_link_xz, init_l_link_yz, init_r_link_xz, init_r_link_yz;
    multibody::MultibodyPlant<double> &plant_;
    std::unique_ptr<systems::Context<double>> plant_context_;
    double calProjectAngleXZ(Eigen::Vector3d a, Eigen::Vector3d b, Eigen::Vector3d c) const;
    struct ArmAnkleConfig
    {
      ArmAnkleConfig() {}
      ArmAnkleConfig(const std::vector<std::string> &cfg_str)
      {
        if (cfg_str.size() != 19)
          std::cout << "Please check the size of ankle config.\n";
        end_link = cfg_str[0];   // l_hand_pitch
        l_link = cfg_str[1];     // l_l_arm_tendon
        r_link = cfg_str[2];     // l_r_arm_tendon
        l_bar_link = cfg_str[3]; // l_l_arm_bar
        r_bar_link = cfg_str[4]; // l_r_arm_bar

        roll_joint = cfg_str[5];     // l_hand_roll
        pitch_joint = cfg_str[6];    // l_hand_pitch
        l_link_joint = cfg_str[7];   // l_l_arm_tendon
        r_link_joint = cfg_str[8];   // l_r_arm_tendon
        l_motor_joint = cfg_str[9];  // l_l_arm_bar
        r_motor_joint = cfg_str[10]; // l_r_arm_bar

        l_motor_actuator = cfg_str[11]; // l_l_arm_bar_motor
        r_motor_actuator = cfg_str[12]; // l_r_arm_bar_motor

        l_end_frame = cfg_str[13];   // l_l_hand_socket
        r_end_frame = cfg_str[14];   // l_r_hand_socket
        l_frame = cfg_str[15];       // l_l_arm_tendon_socket
        r_frame = cfg_str[16];       // l_r_arm_tendon_socket
        l_motor_frame = cfg_str[17]; // l_l_arm_bar_frame
        r_motor_frame = cfg_str[18]; // l_r_arm_bar_frame
      }
      std::string end_link;
      std::string l_bar_link;
      std::string r_bar_link;
      std::string l_link;
      std::string r_link;

      std::string roll_joint; // first
      std::string pitch_joint;
      std::string l_link_joint;
      std::string r_link_joint;
      std::string l_motor_joint;
      std::string r_motor_joint;

      std::string l_motor_actuator;
      std::string r_motor_actuator;

      std::string l_frame;
      std::string r_frame;
      std::string l_end_frame;
      std::string r_end_frame;
      std::string l_motor_frame;
      std::string r_motor_frame; // 考虑了偏移量
    };
    ArmAnkleConfig cfg_;
  };
} // namespace lower_leg
