// Auto-generated. Do not edit!

// (in-package kuavo_ros_interfaces.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class planArmState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.progress = null;
      this.is_finished = null;
    }
    else {
      if (initObj.hasOwnProperty('progress')) {
        this.progress = initObj.progress
      }
      else {
        this.progress = 0;
      }
      if (initObj.hasOwnProperty('is_finished')) {
        this.is_finished = initObj.is_finished
      }
      else {
        this.is_finished = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type planArmState
    // Serialize message field [progress]
    bufferOffset = _serializer.int32(obj.progress, buffer, bufferOffset);
    // Serialize message field [is_finished]
    bufferOffset = _serializer.bool(obj.is_finished, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type planArmState
    let len;
    let data = new planArmState(null);
    // Deserialize message field [progress]
    data.progress = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [is_finished]
    data.is_finished = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_ros_interfaces/planArmState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0743feb5221b176f512f6ea58920b201';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 progress
    bool is_finished
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new planArmState(null);
    if (msg.progress !== undefined) {
      resolved.progress = msg.progress;
    }
    else {
      resolved.progress = 0
    }

    if (msg.is_finished !== undefined) {
      resolved.is_finished = msg.is_finished;
    }
    else {
      resolved.is_finished = false
    }

    return resolved;
    }
};

module.exports = planArmState;
