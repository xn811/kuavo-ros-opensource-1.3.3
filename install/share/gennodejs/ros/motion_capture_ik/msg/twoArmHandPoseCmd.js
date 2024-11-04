// Auto-generated. Do not edit!

// (in-package motion_capture_ik.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let twoArmHandPose = require('./twoArmHandPose.js');
let ikSolveParam = require('./ikSolveParam.js');

//-----------------------------------------------------------

class twoArmHandPoseCmd {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.hand_poses = null;
      this.use_custom_ik_param = null;
      this.joint_angles_as_q0 = null;
      this.ik_param = null;
    }
    else {
      if (initObj.hasOwnProperty('hand_poses')) {
        this.hand_poses = initObj.hand_poses
      }
      else {
        this.hand_poses = new twoArmHandPose();
      }
      if (initObj.hasOwnProperty('use_custom_ik_param')) {
        this.use_custom_ik_param = initObj.use_custom_ik_param
      }
      else {
        this.use_custom_ik_param = false;
      }
      if (initObj.hasOwnProperty('joint_angles_as_q0')) {
        this.joint_angles_as_q0 = initObj.joint_angles_as_q0
      }
      else {
        this.joint_angles_as_q0 = false;
      }
      if (initObj.hasOwnProperty('ik_param')) {
        this.ik_param = initObj.ik_param
      }
      else {
        this.ik_param = new ikSolveParam();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type twoArmHandPoseCmd
    // Serialize message field [hand_poses]
    bufferOffset = twoArmHandPose.serialize(obj.hand_poses, buffer, bufferOffset);
    // Serialize message field [use_custom_ik_param]
    bufferOffset = _serializer.bool(obj.use_custom_ik_param, buffer, bufferOffset);
    // Serialize message field [joint_angles_as_q0]
    bufferOffset = _serializer.bool(obj.joint_angles_as_q0, buffer, bufferOffset);
    // Serialize message field [ik_param]
    bufferOffset = ikSolveParam.serialize(obj.ik_param, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type twoArmHandPoseCmd
    let len;
    let data = new twoArmHandPoseCmd(null);
    // Deserialize message field [hand_poses]
    data.hand_poses = twoArmHandPose.deserialize(buffer, bufferOffset);
    // Deserialize message field [use_custom_ik_param]
    data.use_custom_ik_param = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [joint_angles_as_q0]
    data.joint_angles_as_q0 = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [ik_param]
    data.ik_param = ikSolveParam.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += twoArmHandPose.getMessageSize(object.hand_poses);
    return length + 58;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motion_capture_ik/twoArmHandPoseCmd';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'd4b6792a6f960bea428fd7158220110b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    twoArmHandPose  hand_poses
    # params for the IK solver
    bool use_custom_ik_param
    bool joint_angles_as_q0
    ikSolveParam ik_param
    ================================================================================
    MSG: motion_capture_ik/twoArmHandPose
    Header header
    armHandPose  left_pose
    armHandPose  right_pose
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    ================================================================================
    MSG: motion_capture_ik/armHandPose
    float64[3] pos_xyz
    float64[4] quat_xyzw
    
    float64[3] elbow_pos_xyz
    
    float64[7] joint_angles
    ================================================================================
    MSG: motion_capture_ik/ikSolveParam
    # snopt params
    float64 major_optimality_tol
    float64 major_feasibility_tol
    float64 minor_feasibility_tol
    float64 major_iterations_limit
    # constraint and cost params
    float64 oritation_constraint_tol
    float64 pos_constraint_tol # work when pos_cost_weight > 0.0
    float64 pos_cost_weight
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new twoArmHandPoseCmd(null);
    if (msg.hand_poses !== undefined) {
      resolved.hand_poses = twoArmHandPose.Resolve(msg.hand_poses)
    }
    else {
      resolved.hand_poses = new twoArmHandPose()
    }

    if (msg.use_custom_ik_param !== undefined) {
      resolved.use_custom_ik_param = msg.use_custom_ik_param;
    }
    else {
      resolved.use_custom_ik_param = false
    }

    if (msg.joint_angles_as_q0 !== undefined) {
      resolved.joint_angles_as_q0 = msg.joint_angles_as_q0;
    }
    else {
      resolved.joint_angles_as_q0 = false
    }

    if (msg.ik_param !== undefined) {
      resolved.ik_param = ikSolveParam.Resolve(msg.ik_param)
    }
    else {
      resolved.ik_param = new ikSolveParam()
    }

    return resolved;
    }
};

module.exports = twoArmHandPoseCmd;
