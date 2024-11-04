// Auto-generated. Do not edit!

// (in-package motion_capture_ik.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let twoArmHandPoseCmd = require('../msg/twoArmHandPoseCmd.js');

//-----------------------------------------------------------

let twoArmHandPose = require('../msg/twoArmHandPose.js');

//-----------------------------------------------------------

class twoArmHandPoseCmdSrvRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.twoArmHandPoseCmdRequest = null;
    }
    else {
      if (initObj.hasOwnProperty('twoArmHandPoseCmdRequest')) {
        this.twoArmHandPoseCmdRequest = initObj.twoArmHandPoseCmdRequest
      }
      else {
        this.twoArmHandPoseCmdRequest = new twoArmHandPoseCmd();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type twoArmHandPoseCmdSrvRequest
    // Serialize message field [twoArmHandPoseCmdRequest]
    bufferOffset = twoArmHandPoseCmd.serialize(obj.twoArmHandPoseCmdRequest, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type twoArmHandPoseCmdSrvRequest
    let len;
    let data = new twoArmHandPoseCmdSrvRequest(null);
    // Deserialize message field [twoArmHandPoseCmdRequest]
    data.twoArmHandPoseCmdRequest = twoArmHandPoseCmd.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += twoArmHandPoseCmd.getMessageSize(object.twoArmHandPoseCmdRequest);
    return length;
  }

  static datatype() {
    // Returns string type for a service object
    return 'motion_capture_ik/twoArmHandPoseCmdSrvRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2b372ee6cf4101587f773b62c6572c72';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    twoArmHandPoseCmd twoArmHandPoseCmdRequest
    
    ================================================================================
    MSG: motion_capture_ik/twoArmHandPoseCmd
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
    const resolved = new twoArmHandPoseCmdSrvRequest(null);
    if (msg.twoArmHandPoseCmdRequest !== undefined) {
      resolved.twoArmHandPoseCmdRequest = twoArmHandPoseCmd.Resolve(msg.twoArmHandPoseCmdRequest)
    }
    else {
      resolved.twoArmHandPoseCmdRequest = new twoArmHandPoseCmd()
    }

    return resolved;
    }
};

class twoArmHandPoseCmdSrvResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
      this.with_torso = null;
      this.q_arm = null;
      this.q_torso = null;
      this.time_cost = null;
      this.hand_poses = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
      if (initObj.hasOwnProperty('with_torso')) {
        this.with_torso = initObj.with_torso
      }
      else {
        this.with_torso = false;
      }
      if (initObj.hasOwnProperty('q_arm')) {
        this.q_arm = initObj.q_arm
      }
      else {
        this.q_arm = [];
      }
      if (initObj.hasOwnProperty('q_torso')) {
        this.q_torso = initObj.q_torso
      }
      else {
        this.q_torso = [];
      }
      if (initObj.hasOwnProperty('time_cost')) {
        this.time_cost = initObj.time_cost
      }
      else {
        this.time_cost = 0.0;
      }
      if (initObj.hasOwnProperty('hand_poses')) {
        this.hand_poses = initObj.hand_poses
      }
      else {
        this.hand_poses = new twoArmHandPose();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type twoArmHandPoseCmdSrvResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [with_torso]
    bufferOffset = _serializer.bool(obj.with_torso, buffer, bufferOffset);
    // Serialize message field [q_arm]
    bufferOffset = _arraySerializer.float64(obj.q_arm, buffer, bufferOffset, null);
    // Serialize message field [q_torso]
    bufferOffset = _arraySerializer.float64(obj.q_torso, buffer, bufferOffset, null);
    // Serialize message field [time_cost]
    bufferOffset = _serializer.float64(obj.time_cost, buffer, bufferOffset);
    // Serialize message field [hand_poses]
    bufferOffset = twoArmHandPose.serialize(obj.hand_poses, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type twoArmHandPoseCmdSrvResponse
    let len;
    let data = new twoArmHandPoseCmdSrvResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [with_torso]
    data.with_torso = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [q_arm]
    data.q_arm = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [q_torso]
    data.q_torso = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [time_cost]
    data.time_cost = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [hand_poses]
    data.hand_poses = twoArmHandPose.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.q_arm.length;
    length += 8 * object.q_torso.length;
    length += twoArmHandPose.getMessageSize(object.hand_poses);
    return length + 18;
  }

  static datatype() {
    // Returns string type for a service object
    return 'motion_capture_ik/twoArmHandPoseCmdSrvResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7dba8c11b6c3ac9ec243b4520ad906c7';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    bool with_torso
    float64[] q_arm
    float64[] q_torso
    
    float64   time_cost # unit: ms
    # ik result
    twoArmHandPose  hand_poses
    
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new twoArmHandPoseCmdSrvResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    if (msg.with_torso !== undefined) {
      resolved.with_torso = msg.with_torso;
    }
    else {
      resolved.with_torso = false
    }

    if (msg.q_arm !== undefined) {
      resolved.q_arm = msg.q_arm;
    }
    else {
      resolved.q_arm = []
    }

    if (msg.q_torso !== undefined) {
      resolved.q_torso = msg.q_torso;
    }
    else {
      resolved.q_torso = []
    }

    if (msg.time_cost !== undefined) {
      resolved.time_cost = msg.time_cost;
    }
    else {
      resolved.time_cost = 0.0
    }

    if (msg.hand_poses !== undefined) {
      resolved.hand_poses = twoArmHandPose.Resolve(msg.hand_poses)
    }
    else {
      resolved.hand_poses = new twoArmHandPose()
    }

    return resolved;
    }
};

module.exports = {
  Request: twoArmHandPoseCmdSrvRequest,
  Response: twoArmHandPoseCmdSrvResponse,
  md5sum() { return '4cedfbf98f38ce7e92b358cb2d3ef39d'; },
  datatype() { return 'motion_capture_ik/twoArmHandPoseCmdSrv'; }
};
