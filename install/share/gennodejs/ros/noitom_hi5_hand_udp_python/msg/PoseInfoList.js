// Auto-generated. Do not edit!

// (in-package noitom_hi5_hand_udp_python.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let PoseInfo = require('./PoseInfo.js');

//-----------------------------------------------------------

class PoseInfoList {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.timestamp_ms = null;
      this.is_high_confidence = null;
      this.is_hand_tracking = null;
      this.poses = null;
    }
    else {
      if (initObj.hasOwnProperty('timestamp_ms')) {
        this.timestamp_ms = initObj.timestamp_ms
      }
      else {
        this.timestamp_ms = 0;
      }
      if (initObj.hasOwnProperty('is_high_confidence')) {
        this.is_high_confidence = initObj.is_high_confidence
      }
      else {
        this.is_high_confidence = false;
      }
      if (initObj.hasOwnProperty('is_hand_tracking')) {
        this.is_hand_tracking = initObj.is_hand_tracking
      }
      else {
        this.is_hand_tracking = false;
      }
      if (initObj.hasOwnProperty('poses')) {
        this.poses = initObj.poses
      }
      else {
        this.poses = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PoseInfoList
    // Serialize message field [timestamp_ms]
    bufferOffset = _serializer.int64(obj.timestamp_ms, buffer, bufferOffset);
    // Serialize message field [is_high_confidence]
    bufferOffset = _serializer.bool(obj.is_high_confidence, buffer, bufferOffset);
    // Serialize message field [is_hand_tracking]
    bufferOffset = _serializer.bool(obj.is_hand_tracking, buffer, bufferOffset);
    // Serialize message field [poses]
    // Serialize the length for message field [poses]
    bufferOffset = _serializer.uint32(obj.poses.length, buffer, bufferOffset);
    obj.poses.forEach((val) => {
      bufferOffset = PoseInfo.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PoseInfoList
    let len;
    let data = new PoseInfoList(null);
    // Deserialize message field [timestamp_ms]
    data.timestamp_ms = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [is_high_confidence]
    data.is_high_confidence = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [is_hand_tracking]
    data.is_hand_tracking = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [poses]
    // Deserialize array length for message field [poses]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.poses = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.poses[i] = PoseInfo.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 56 * object.poses.length;
    return length + 14;
  }

  static datatype() {
    // Returns string type for a message object
    return 'noitom_hi5_hand_udp_python/PoseInfoList';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f56d5e4df1c0e38a423ead4bde9414b3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int64 timestamp_ms
    bool is_high_confidence
    bool is_hand_tracking
    PoseInfo[] poses
    ================================================================================
    MSG: noitom_hi5_hand_udp_python/PoseInfo
    geometry_msgs/Point position
    geometry_msgs/Quaternion orientation
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PoseInfoList(null);
    if (msg.timestamp_ms !== undefined) {
      resolved.timestamp_ms = msg.timestamp_ms;
    }
    else {
      resolved.timestamp_ms = 0
    }

    if (msg.is_high_confidence !== undefined) {
      resolved.is_high_confidence = msg.is_high_confidence;
    }
    else {
      resolved.is_high_confidence = false
    }

    if (msg.is_hand_tracking !== undefined) {
      resolved.is_hand_tracking = msg.is_hand_tracking;
    }
    else {
      resolved.is_hand_tracking = false
    }

    if (msg.poses !== undefined) {
      resolved.poses = new Array(msg.poses.length);
      for (let i = 0; i < resolved.poses.length; ++i) {
        resolved.poses[i] = PoseInfo.Resolve(msg.poses[i]);
      }
    }
    else {
      resolved.poses = []
    }

    return resolved;
    }
};

module.exports = PoseInfoList;
