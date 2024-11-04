// Auto-generated. Do not edit!

// (in-package motion_capture_ik.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class headBodyPose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.head_pitch = null;
      this.head_yaw = null;
      this.body_roll = null;
      this.body_pitch = null;
      this.body_yaw = null;
      this.body_x = null;
      this.body_y = null;
      this.body_height = null;
    }
    else {
      if (initObj.hasOwnProperty('head_pitch')) {
        this.head_pitch = initObj.head_pitch
      }
      else {
        this.head_pitch = 0.0;
      }
      if (initObj.hasOwnProperty('head_yaw')) {
        this.head_yaw = initObj.head_yaw
      }
      else {
        this.head_yaw = 0.0;
      }
      if (initObj.hasOwnProperty('body_roll')) {
        this.body_roll = initObj.body_roll
      }
      else {
        this.body_roll = 0.0;
      }
      if (initObj.hasOwnProperty('body_pitch')) {
        this.body_pitch = initObj.body_pitch
      }
      else {
        this.body_pitch = 0.0;
      }
      if (initObj.hasOwnProperty('body_yaw')) {
        this.body_yaw = initObj.body_yaw
      }
      else {
        this.body_yaw = 0.0;
      }
      if (initObj.hasOwnProperty('body_x')) {
        this.body_x = initObj.body_x
      }
      else {
        this.body_x = 0.0;
      }
      if (initObj.hasOwnProperty('body_y')) {
        this.body_y = initObj.body_y
      }
      else {
        this.body_y = 0.0;
      }
      if (initObj.hasOwnProperty('body_height')) {
        this.body_height = initObj.body_height
      }
      else {
        this.body_height = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type headBodyPose
    // Serialize message field [head_pitch]
    bufferOffset = _serializer.float64(obj.head_pitch, buffer, bufferOffset);
    // Serialize message field [head_yaw]
    bufferOffset = _serializer.float64(obj.head_yaw, buffer, bufferOffset);
    // Serialize message field [body_roll]
    bufferOffset = _serializer.float64(obj.body_roll, buffer, bufferOffset);
    // Serialize message field [body_pitch]
    bufferOffset = _serializer.float64(obj.body_pitch, buffer, bufferOffset);
    // Serialize message field [body_yaw]
    bufferOffset = _serializer.float64(obj.body_yaw, buffer, bufferOffset);
    // Serialize message field [body_x]
    bufferOffset = _serializer.float64(obj.body_x, buffer, bufferOffset);
    // Serialize message field [body_y]
    bufferOffset = _serializer.float64(obj.body_y, buffer, bufferOffset);
    // Serialize message field [body_height]
    bufferOffset = _serializer.float64(obj.body_height, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type headBodyPose
    let len;
    let data = new headBodyPose(null);
    // Deserialize message field [head_pitch]
    data.head_pitch = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [head_yaw]
    data.head_yaw = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [body_roll]
    data.body_roll = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [body_pitch]
    data.body_pitch = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [body_yaw]
    data.body_yaw = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [body_x]
    data.body_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [body_y]
    data.body_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [body_height]
    data.body_height = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 64;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motion_capture_ik/headBodyPose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '86a58d9f885335d8a0b389ace07ba692';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # head (rad)
    float64 head_pitch
    float64 head_yaw
    # body (rad)
    float64 body_roll
    float64 body_pitch
    float64 body_yaw
    
    float64 body_x
    float64 body_y
    float64 body_height
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new headBodyPose(null);
    if (msg.head_pitch !== undefined) {
      resolved.head_pitch = msg.head_pitch;
    }
    else {
      resolved.head_pitch = 0.0
    }

    if (msg.head_yaw !== undefined) {
      resolved.head_yaw = msg.head_yaw;
    }
    else {
      resolved.head_yaw = 0.0
    }

    if (msg.body_roll !== undefined) {
      resolved.body_roll = msg.body_roll;
    }
    else {
      resolved.body_roll = 0.0
    }

    if (msg.body_pitch !== undefined) {
      resolved.body_pitch = msg.body_pitch;
    }
    else {
      resolved.body_pitch = 0.0
    }

    if (msg.body_yaw !== undefined) {
      resolved.body_yaw = msg.body_yaw;
    }
    else {
      resolved.body_yaw = 0.0
    }

    if (msg.body_x !== undefined) {
      resolved.body_x = msg.body_x;
    }
    else {
      resolved.body_x = 0.0
    }

    if (msg.body_y !== undefined) {
      resolved.body_y = msg.body_y;
    }
    else {
      resolved.body_y = 0.0
    }

    if (msg.body_height !== undefined) {
      resolved.body_height = msg.body_height;
    }
    else {
      resolved.body_height = 0.0
    }

    return resolved;
    }
};

module.exports = headBodyPose;
