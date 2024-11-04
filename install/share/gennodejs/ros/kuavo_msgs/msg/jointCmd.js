// Auto-generated. Do not edit!

// (in-package kuavo_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class jointCmd {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.joint_q = null;
      this.joint_v = null;
      this.tau = null;
      this.tau_max = null;
      this.tau_ratio = null;
      this.joint_kp = null;
      this.joint_kd = null;
      this.control_modes = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('joint_q')) {
        this.joint_q = initObj.joint_q
      }
      else {
        this.joint_q = [];
      }
      if (initObj.hasOwnProperty('joint_v')) {
        this.joint_v = initObj.joint_v
      }
      else {
        this.joint_v = [];
      }
      if (initObj.hasOwnProperty('tau')) {
        this.tau = initObj.tau
      }
      else {
        this.tau = [];
      }
      if (initObj.hasOwnProperty('tau_max')) {
        this.tau_max = initObj.tau_max
      }
      else {
        this.tau_max = [];
      }
      if (initObj.hasOwnProperty('tau_ratio')) {
        this.tau_ratio = initObj.tau_ratio
      }
      else {
        this.tau_ratio = [];
      }
      if (initObj.hasOwnProperty('joint_kp')) {
        this.joint_kp = initObj.joint_kp
      }
      else {
        this.joint_kp = [];
      }
      if (initObj.hasOwnProperty('joint_kd')) {
        this.joint_kd = initObj.joint_kd
      }
      else {
        this.joint_kd = [];
      }
      if (initObj.hasOwnProperty('control_modes')) {
        this.control_modes = initObj.control_modes
      }
      else {
        this.control_modes = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type jointCmd
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [joint_q]
    bufferOffset = _arraySerializer.float64(obj.joint_q, buffer, bufferOffset, null);
    // Serialize message field [joint_v]
    bufferOffset = _arraySerializer.float64(obj.joint_v, buffer, bufferOffset, null);
    // Serialize message field [tau]
    bufferOffset = _arraySerializer.float64(obj.tau, buffer, bufferOffset, null);
    // Serialize message field [tau_max]
    bufferOffset = _arraySerializer.float64(obj.tau_max, buffer, bufferOffset, null);
    // Serialize message field [tau_ratio]
    bufferOffset = _arraySerializer.float64(obj.tau_ratio, buffer, bufferOffset, null);
    // Serialize message field [joint_kp]
    bufferOffset = _arraySerializer.float64(obj.joint_kp, buffer, bufferOffset, null);
    // Serialize message field [joint_kd]
    bufferOffset = _arraySerializer.float64(obj.joint_kd, buffer, bufferOffset, null);
    // Serialize message field [control_modes]
    bufferOffset = _arraySerializer.int32(obj.control_modes, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type jointCmd
    let len;
    let data = new jointCmd(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [joint_q]
    data.joint_q = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_v]
    data.joint_v = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [tau]
    data.tau = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [tau_max]
    data.tau_max = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [tau_ratio]
    data.tau_ratio = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_kp]
    data.joint_kp = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_kd]
    data.joint_kd = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [control_modes]
    data.control_modes = _arrayDeserializer.int32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 8 * object.joint_q.length;
    length += 8 * object.joint_v.length;
    length += 8 * object.tau.length;
    length += 8 * object.tau_max.length;
    length += 8 * object.tau_ratio.length;
    length += 8 * object.joint_kp.length;
    length += 8 * object.joint_kd.length;
    length += 4 * object.control_modes.length;
    return length + 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/jointCmd';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9ed16f87b9f90b25cdeeb417f3c21f9e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    float64[] joint_q  
    float64[] joint_v  
    float64[] tau  
    float64[] tau_max
    float64[] tau_ratio  
    float64[] joint_kp  
    float64[] joint_kd
    int32[] control_modes  
    
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
    const resolved = new jointCmd(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.joint_q !== undefined) {
      resolved.joint_q = msg.joint_q;
    }
    else {
      resolved.joint_q = []
    }

    if (msg.joint_v !== undefined) {
      resolved.joint_v = msg.joint_v;
    }
    else {
      resolved.joint_v = []
    }

    if (msg.tau !== undefined) {
      resolved.tau = msg.tau;
    }
    else {
      resolved.tau = []
    }

    if (msg.tau_max !== undefined) {
      resolved.tau_max = msg.tau_max;
    }
    else {
      resolved.tau_max = []
    }

    if (msg.tau_ratio !== undefined) {
      resolved.tau_ratio = msg.tau_ratio;
    }
    else {
      resolved.tau_ratio = []
    }

    if (msg.joint_kp !== undefined) {
      resolved.joint_kp = msg.joint_kp;
    }
    else {
      resolved.joint_kp = []
    }

    if (msg.joint_kd !== undefined) {
      resolved.joint_kd = msg.joint_kd;
    }
    else {
      resolved.joint_kd = []
    }

    if (msg.control_modes !== undefined) {
      resolved.control_modes = msg.control_modes;
    }
    else {
      resolved.control_modes = []
    }

    return resolved;
    }
};

module.exports = jointCmd;
