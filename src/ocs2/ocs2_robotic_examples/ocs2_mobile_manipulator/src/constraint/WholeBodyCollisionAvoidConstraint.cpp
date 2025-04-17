#include <ocs2_mobile_manipulator/MobileManipulatorPreComputation.h>
#include <ocs2_mobile_manipulator/constraint/WholeBodyCollisionAvoidConstraint.h>

#include <ocs2_core/misc/LinearInterpolation.h>

namespace ocs2 {
namespace mobile_manipulator {

/******************************************************************************************************/
/******************************************************************************************************/
/******************************************************************************************************/
WholeBodyCollisionAvoidConstraint::WholeBodyCollisionAvoidConstraint(const EndEffectorKinematics<scalar_t>& endEffectorKinematics,
                                             const ReferenceManager& referenceManager, int eefIdx)
    : StateConstraint(ConstraintOrder::Linear),
      endEffectorKinematicsPtr_(endEffectorKinematics.clone()),
      eefIdx_(eefIdx),
      referenceManagerPtr_(&referenceManager) {
  if (endEffectorKinematics.getIds().size() != 1) {
    throw std::runtime_error("[WholeBodyCollisionAvoidConstraint] endEffectorKinematics has wrong number of end effector IDs.");
  }
  pinocchioEEKinPtr_ = dynamic_cast<PinocchioEndEffectorKinematics*>(endEffectorKinematicsPtr_.get());
}

/******************************************************************************************************/
/******************************************************************************************************/
/******************************************************************************************************/
size_t WholeBodyCollisionAvoidConstraint::getNumConstraints(scalar_t time) const {
  return 6;
}

/******************************************************************************************************/
/******************************************************************************************************/
/******************************************************************************************************/
vector_t WholeBodyCollisionAvoidConstraint::getValue(scalar_t time, const vector_t& state, const PreComputation& preComputation) const {
  // PinocchioEndEffectorKinematics requires pre-computation with shared PinocchioInterface.
  if (pinocchioEEKinPtr_ != nullptr) {
    const auto& preCompMM = cast<MobileManipulatorPreComputation>(preComputation);
    pinocchioEEKinPtr_->setPinocchioInterface(preCompMM.getPinocchioInterface());
  }

  const auto desiredPositionOrientation = interpolateEndEffectorPose(time);

  vector_t constraint(6);
  constraint.head<3>() = endEffectorKinematicsPtr_->getPosition(state).front() - desiredPositionOrientation.first;
  constraint.tail<3>() = endEffectorKinematicsPtr_->getOrientationError(state, {desiredPositionOrientation.second}).front();
  return constraint;
}

/******************************************************************************************************/
/******************************************************************************************************/
/******************************************************************************************************/
VectorFunctionLinearApproximation WholeBodyCollisionAvoidConstraint::getLinearApproximation(scalar_t time, const vector_t& state,
                                                                                const PreComputation& preComputation) const {
  // PinocchioEndEffectorKinematics requires pre-computation with shared PinocchioInterface.
  if (pinocchioEEKinPtr_ != nullptr) {
    const auto& preCompMM = cast<MobileManipulatorPreComputation>(preComputation);
    pinocchioEEKinPtr_->setPinocchioInterface(preCompMM.getPinocchioInterface());
  }

  const auto desiredPositionOrientation = interpolateEndEffectorPose(time);

  auto approximation = VectorFunctionLinearApproximation(6, state.rows(), 0);

  const auto eePosition = endEffectorKinematicsPtr_->getPositionLinearApproximation(state).front();
  approximation.f.head<3>() = eePosition.f - desiredPositionOrientation.first;
  approximation.dfdx.topRows<3>() = eePosition.dfdx;

  const auto eeOrientationError =
      endEffectorKinematicsPtr_->getOrientationErrorLinearApproximation(state, {desiredPositionOrientation.second}).front();
  approximation.f.tail<3>() = eeOrientationError.f;
  approximation.dfdx.bottomRows<3>() = eeOrientationError.dfdx;

  return approximation;
}

/******************************************************************************************************/
/******************************************************************************************************/
/******************************************************************************************************/
auto WholeBodyCollisionAvoidConstraint::interpolateEndEffectorPose(scalar_t time) const -> std::pair<vector_t, quaternion_t> {
  const auto& targetTrajectories = referenceManagerPtr_->getTargetTrajectories();
  const auto& timeTrajectory = targetTrajectories.timeTrajectory;
  const auto& stateTrajectory = targetTrajectories.stateTrajectory;

  vector_t position;
  quaternion_t orientation;

  const size_t Nb = stateTrajectory[0].size() - 14;// base state dim
  if (stateTrajectory.size() > 1) {
    // Normal interpolation case
    int index;
    scalar_t alpha;
    std::tie(index, alpha) = LinearInterpolation::timeSegment(time, timeTrajectory);

    const auto& lhs = stateTrajectory[index];
    const auto& rhs = stateTrajectory[index + 1];
    const quaternion_t q_lhs(lhs.segment<4>(7*eefIdx_+3+Nb));
    const quaternion_t q_rhs(rhs.segment<4>(7*eefIdx_+3+Nb));

    position = alpha * lhs.segment<3>(7*eefIdx_+Nb) + (1.0 - alpha) * rhs.segment<3>(7*eefIdx_+Nb);
    orientation = q_lhs.slerp((1.0 - alpha), q_rhs);
  } else {  // stateTrajectory.size() == 1
    position = stateTrajectory.front().segment<3>(7*eefIdx_+Nb);
    orientation = quaternion_t(stateTrajectory.front().segment<4>(7*eefIdx_+3+Nb));
  }

  return {position, orientation};
}

}  // namespace mobile_manipulator
}  // namespace ocs2
