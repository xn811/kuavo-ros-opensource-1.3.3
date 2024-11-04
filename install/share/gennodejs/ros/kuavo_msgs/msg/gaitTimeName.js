// Auto-generated. Do not edit!

// (in-package kuavo_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class gaitTimeName {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.start_time = null;
      this.gait_name = null;
    }
    else {
      if (initObj.hasOwnProperty('start_time')) {
        this.start_time = initObj.start_time
      }
      else {
        this.start_time = 0.0;
      }
      if (initObj.hasOwnProperty('gait_name')) {
        this.gait_name = initObj.gait_name
      }
      else {
        this.gait_name = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type gaitTimeName
    // Serialize message field [start_time]
    bufferOffset = _serializer.float32(obj.start_time, buffer, bufferOffset);
    // Serialize message field [gait_name]
    bufferOffset = _serializer.string(obj.gait_name, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type gaitTimeName
    let len;
    let data = new gaitTimeName(null);
    // Deserialize message field [start_time]
    data.start_time = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [gait_name]
    data.gait_name = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.gait_name);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/gaitTimeName';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c694c8dbb2e8c9d73614407bfe314692';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 start_time
    string  gait_name
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new gaitTimeName(null);
    if (msg.start_time !== undefined) {
      resolved.start_time = msg.start_time;
    }
    else {
      resolved.start_time = 0.0
    }

    if (msg.gait_name !== undefined) {
      resolved.gait_name = msg.gait_name;
    }
    else {
      resolved.gait_name = ''
    }

    return resolved;
    }
};

module.exports = gaitTimeName;
