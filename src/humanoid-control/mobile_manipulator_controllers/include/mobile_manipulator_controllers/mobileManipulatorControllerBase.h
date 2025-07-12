#pragma once

#include <ros/ros.h>
#include <ocs2_core/misc/Benchmark.h>
#include <ocs2_mpc/MPC_MRT_Interface.h>
#include <ocs2_mpc/SystemObservation.h>
#include <ocs2_pinocchio_interface/PinocchioEndEffectorKinematics.h>
#include <ocs2_pinocchio_interface/PinocchioEndEffectorSpatialKinematics.h>
#include "ocs2_pinocchio_interface/PinocchioInterface.h"
#include <ocs2_msgs/mpc_observation.h>
#include <ocs2_msgs/mpc_flattened_controller.h>
#include <ocs2_ros_interfaces/common/RosMsgConversions.h>

#include <ocs2_mobile_manipulator/MobileManipulatorInterface.h>
#include <mobile_manipulator_controllers/mobileManipulatorVisualization.h>
#include <ocs2_mobile_manipulator/MobileManipulatorPinocchioMapping.h>
#include <visualization_msgs/MarkerArray.h>
#include <deque>
#include <mutex>
#include <condition_variable>
#include <memory>
#include "mobile_manipulator_controllers/package_path.h"
#include "humanoid_interface/common/TopicLogger.h"


namespace mobile_manipulator_controller
{
  using namespace ocs2;
  using namespace ocs2::mobile_manipulator;
  
  enum class MpcType
  {
    DDP,
    SQP
  };

  class MobileManipulatorControllerBase
  {
  public:
    MobileManipulatorControllerBase(ros::NodeHandle &nh, const std::string& taskFile, const std::string& libFolder, const std::string& urdfFile, MpcType mpcType, int freq, 
            bool dummySimBase=false, bool dummySimArm=true, bool visualizeMm=true);
    ~MobileManipulatorControllerBase();
    int update(const vector_t& externalState, vector_t& nextState);
    int update(const vector_t& externalState, vector_t& nextState, vector_t& optimizedInput);
    void stop() { updateRunning_ = false; }
    void start() { updateRunning_ = true; }
    /**
     * @brief Reset the controller to the given external state
     * @param externalState: The external state to reset to
     * @return 0 if successful, -1 if failed
     */
    int reset(const vector_t& externalState);
    inline void setExternalState(const vector_t& externalState) {
      vector_t nextState = vector_t::Zero(externalState.size());
      this->update(externalState, nextState);
      mmObservationDummy_.time += 1.0 / freq_;
    }
    int setTargetTrajectory(const TargetTrajectories& targetTrajectories);
    ocs2::vector_t getTargetFromState(const vector_t& state);
    void resetMpcToGivenState(const SystemObservation& resetObservation);
    void starting();
    virtual void setupMobileManipulatorInterface(const std::string &taskFile, const std::string &libFolder, const std::string &urdfFile, MpcType mpcType);
    virtual void setupMpc();
    virtual void setupMrt();
    void getOptimizedStateAndInput(const SystemObservation& currentObservation, vector_t& optimizedStateMrt, vector_t& optimizedInputMrt);
    /**
     * Creates MPC Policy message.
     *
     * @param [in] primalSolution: The policy data of the MPC.
     * @param [in] commandData: The command data of the MPC.
     * @param [in] performanceIndices: The performance indices data of the solver.
     * @return MPC policy message.
     */
    static ocs2_msgs::mpc_flattened_controller createMpcPolicyMsg(const PrimalSolution &primalSolution, const CommandData &commandData,
                                                                  const PerformanceIndex &performanceIndices);
    SystemObservation forwardSimulation(const SystemObservation& currentObservation, scalar_t dt);
    vector_t getMMEefPose(const vector_t& state);
    visualization_msgs::MarkerArray getVisualizeTrajectoryMsg(const std::deque<Eigen::VectorXd>& twoHandPoseTrajectory, std::vector<double> rgba={1,0,0,1});

    std::shared_ptr<MobileManipulatorVisualization> visualizationPtr_;

    ros::Publisher mmEefPosesPublisher_;
    ros::Publisher mmPlanedTrajPublisher_;
    void publishEefPoses(const vector_t& eefPoses);

    int freq_;
    int dummySim_;
    int dummySimArm_;
    bool visualizeMm_;
    std::deque<Eigen::VectorXd> mmPlanedTrajQueue_;

  private:

  protected:
    std::thread mpcThread_;

    std::atomic_bool controllerRunning_{}, mpcRunning_{}, updateRunning_{};
    
    // Thread synchronization for reset operations
    std::mutex mpcThreadMutex_;
    std::condition_variable mpcThreadCondition_;
    std::atomic_bool mpcThreadPaused_{false};
    
    benchmark::RepeatedTimer mpcTimer_;

    // Interface
    std::shared_ptr<ocs2::mobile_manipulator::MobileManipulatorInterface> mobileManipulatorInterface_;
    ocs2::mobile_manipulator::ManipulatorModelInfo info_;

    SystemObservation mmObservationDummy_;

    // Nonlinear MPC
    std::shared_ptr<MPC_BASE> mpc_;
    std::shared_ptr<MPC_MRT_Interface> mpcMrtInterface_;

    ros::Publisher observationPublisher_;
    ros::Publisher mpcPolicyPublisher_;

    std::unique_ptr<PinocchioInterface> pinocchioInterface_ptr_;
    std::shared_ptr<PinocchioEndEffectorSpatialKinematics> eeSpatialKinematicsPtr_;
    std::unique_ptr<MobileManipulatorPinocchioMapping> pinocchioMappingPtr_;

    // Node Handle
    ros::NodeHandle controllerNh_;
    const std::string robotName_ = "mobile_manipulator";
    std::unique_ptr<humanoid::TopicLogger> ros_logger_;
    MpcType mpcType_;
  };

} // namespace mobile_manipulator_controller
