#include <Eigen/Dense>
#include "plantIK.h"
#include "drake/solvers/snopt_solver.h"

namespace HighlyDynamic
{
  CoMIK::CoMIK(drake::multibody::MultibodyPlant<double> *plant,
               std::vector<std::string> frames_name)
      : plant_{plant}, frames_name_{std::move(frames_name)}
  {
    plant_context_ = plant_->CreateDefaultContext();
    prev_q_sol.resize(plant_->num_positions());
    prev_q_sol.setZero();
  }

  drake::solvers::Binding<drake::solvers::Constraint>
  CoMIK::AddCoMPositionConstraint(drake::multibody::InverseKinematics &ik,
                                  const Eigen::Vector3d &r_des)
  {
    auto constraint = std::make_shared<drake::multibody::ComPositionConstraint>(
        (const drake::multibody::MultibodyPlant<double> *)plant_, std::nullopt,
        plant_->world_frame(), plant_context_.get());

    drake::solvers::VectorXDecisionVariable r = ik.get_mutable_prog()->NewContinuousVariables(3);

    drake::solvers::VectorXDecisionVariable vars(ik.q().size() + 3);
    vars << ik.q(), r;
    ik.get_mutable_prog()->AddConstraint(constraint, vars);

    drake::solvers::Binding<drake::solvers::Constraint> b = ik.get_mutable_prog()->AddBoundingBoxConstraint(r_des, r_des, r);

    ik.get_mutable_prog()->SetInitialGuess(r, r_des);
    return b;
  }

  bool CoMIK::solve(const FramePoseVec &pose, const Eigen::VectorXd &q0, Eigen::VectorXd &q_sol, IKParams params)
  {
    drake::multibody::InverseKinematics ik(*plant_);
    for (uint32_t i = 0; i < frames_name_.size(); i++)
    {
      const drake::multibody::Frame<double> &frame = plant_->GetFrameByName(frames_name_[i]);
      if (i == 1 || i == 2)
      {
        ik.AddOrientationConstraint(
            plant_->world_frame(),
            drake::math::RotationMatrixd(Eigen::Quaterniond(pose[i].first)), 
            frame,
            drake::math::RotationMatrixd(drake::math::RollPitchYawd(0, 0, 0)), 
            params.oritation_constraint_tol);
      }
      if (i ==1 || i == 2)
      {
        if(params.pos_cost_weight <= 0.0){
          ik.AddPositionConstraint(frame, 
                                  Eigen::Vector3d::Zero(),
                                  plant_->world_frame(),
                                  pose[i].second - Eigen::Vector3d::Constant(params.pos_constraint_tol),
                                  pose[i].second + Eigen::Vector3d::Constant(params.pos_constraint_tol));
        }else{
          ik.AddPositionCost(
                      plant_->world_frame(),
                      pose[i].second,
                      frame,
                      Eigen::Vector3d::Zero(),
                      params.pos_cost_weight * Eigen::MatrixXd::Identity(3, 3));
        }
      }
      else if(i==3 || i==4){//elbow
          ik.AddPositionCost(
                      plant_->world_frame(),
                      pose[i].second,
                      frame,
                      Eigen::Vector3d::Zero(),
                      0.1 * params.pos_cost_weight * Eigen::MatrixXd::Identity(3, 3));
      }
    }
    ik.get_mutable_prog()->SetInitialGuess(ik.q(), q0);
    ik.get_mutable_prog()->SetSolverOption(drake::solvers::SnoptSolver::id(), "Major feasibility tolerance", params.major_feasibility_tol);
    ik.get_mutable_prog()->SetSolverOption(drake::solvers::SnoptSolver::id(), "Minor feasibility tolerance", params.minor_feasibility_tol);
    ik.get_mutable_prog()->SetSolverOption(drake::solvers::SnoptSolver::id(), "Major Optimality Tolerance", params.major_optimality_tol);
    ik.get_mutable_prog()->SetSolverOption(drake::solvers::SnoptSolver::id(), "Major Iterations Limit", params.major_iterations_limit);

    // ik.get_mutable_prog()->SetSolverOption(drake::solvers::SnoptSolver::id(), "Print file", "tmp/snopt.out");
    drake::solvers::MathematicalProgramResult result = drake::solvers::Solve(ik.prog());
    if (!result.is_success())
    {
      // std::cout << "Failed solution: " << result.GetSolution(ik.q()).transpose() << "\n";
      // std::cout << "Previous solution: " << prev_q_sol.transpose() << "\n";
      return false;
    }
    else
    {
      q_sol = result.GetSolution(ik.q());
      prev_q_sol = q_sol;
      return true;
    }
  }

  std::pair<Eigen::Vector3d, Eigen::Quaterniond> CoMIK::FK(const Eigen::VectorXd& q, HandSide side) {
    plant_->SetPositions(plant_context_.get(), q);
    std::string frame_name;
    if(side == HandSide::LEFT)
      frame_name = frames_name_[1];
    else if(side == HandSide::RIGHT)
      frame_name = frames_name_[2];

    auto pose = plant_->GetFrameByName(frame_name).CalcPose(*plant_context_.get(), plant_->GetFrameByName(frames_name_[0]));
    return std::make_pair(pose.translation(), pose.rotation().ToQuaternion());
  }

} // namespace drake