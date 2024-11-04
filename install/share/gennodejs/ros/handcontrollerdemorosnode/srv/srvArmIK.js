// Auto-generated. Do not edit!

// (in-package handcontrollerdemorosnode.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

let sensor_msgs = _finder('sensor_msgs');

//-----------------------------------------------------------

class srvArmIKRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.left_arm_pose = null;
      this.right_arm_pose = null;
    }
    else {
      if (initObj.hasOwnProperty('left_arm_pose')) {
        this.left_arm_pose = initObj.left_arm_pose
      }
      else {
        this.left_arm_pose = [];
      }
      if (initObj.hasOwnProperty('right_arm_pose')) {
        this.right_arm_pose = initObj.right_arm_pose
      }
      else {
        this.right_arm_pose = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type srvArmIKRequest
    // Serialize message field [left_arm_pose]
    bufferOffset = _arraySerializer.float64(obj.left_arm_pose, buffer, bufferOffset, null);
    // Serialize message field [right_arm_pose]
    bufferOffset = _arraySerializer.float64(obj.right_arm_pose, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type srvArmIKRequest
    let len;
    let data = new srvArmIKRequest(null);
    // Deserialize message field [left_arm_pose]
    data.left_arm_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [right_arm_pose]
    data.right_arm_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.left_arm_pose.length;
    length += 8 * object.right_arm_pose.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'handcontrollerdemorosnode/srvArmIKRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c281ae760454cca592ca88fb5b3b708b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] left_arm_pose
    float64[] right_arm_pose
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new srvArmIKRequest(null);
    if (msg.left_arm_pose !== undefined) {
      resolved.left_arm_pose = msg.left_arm_pose;
    }
    else {
      resolved.left_arm_pose = []
    }

    if (msg.right_arm_pose !== undefined) {
      resolved.right_arm_pose = msg.right_arm_pose;
    }
    else {
      resolved.right_arm_pose = []
    }

    return resolved;
    }
};

class srvArmIKResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.joint_state = null;
    }
    else {
      if (initObj.hasOwnProperty('joint_state')) {
        this.joint_state = initObj.joint_state
      }
      else {
        this.joint_state = new sensor_msgs.msg.JointState();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type srvArmIKResponse
    // Serialize message field [joint_state]
    bufferOffset = sensor_msgs.msg.JointState.serialize(obj.joint_state, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type srvArmIKResponse
    let len;
    let data = new srvArmIKResponse(null);
    // Deserialize message field [joint_state]
    data.joint_state = sensor_msgs.msg.JointState.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += sensor_msgs.msg.JointState.getMessageSize(object.joint_state);
    return length;
  }

  static datatype() {
    // Returns string type for a service object
    return 'handcontrollerdemorosnode/srvArmIKResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9ca061465ef0ed08771ed240c43789f5';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    sensor_msgs/JointState joint_state
    
    
    ================================================================================
    MSG: sensor_msgs/JointState
    # This is a message that holds data to describe the state of a set of torque controlled joints. 
    #
    # The state of each joint (revolute or prismatic) is defined by:
    #  * the position of the joint (rad or m),
    #  * the velocity of the joint (rad/s or m/s) and 
    #  * the effort that is applied in the joint (Nm or N).
    #
    # Each joint is uniquely identified by its name
    # The header specifies the time at which the joint states were recorded. All the joint states
    # in one message have to be recorded at the same time.
    #
    # This message consists of a multiple arrays, one for each part of the joint state. 
    # The goal is to make each of the fields optional. When e.g. your joints have no
    # effort associated with them, you can leave the effort array empty. 
    #
    # All arrays in this message should have the same size, or be empty.
    # This is the only way to uniquely associate the joint name with the correct
    # states.
    
    
    Header header
    
    string[] name
    float64[] position
    float64[] velocity
    float64[] effort
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new srvArmIKResponse(null);
    if (msg.joint_state !== undefined) {
      resolved.joint_state = sensor_msgs.msg.JointState.Resolve(msg.joint_state)
    }
    else {
      resolved.joint_state = new sensor_msgs.msg.JointState()
    }

    return resolved;
    }
};

module.exports = {
  Request: srvArmIKRequest,
  Response: srvArmIKResponse,
  md5sum() { return '2b5b0516bd664187d5eefa858c0bc7ee'; },
  datatype() { return 'handcontrollerdemorosnode/srvArmIK'; }
};
