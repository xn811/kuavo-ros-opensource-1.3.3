// Auto-generated. Do not edit!

// (in-package humanoid_interface_ros.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class uwbdebug {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.robot_uwb_cur_x = null;
      this.robot_uwb_cur_y = null;
      this.robot_uwb_cur_angle = null;
      this.robot_uwb_fir_angle = null;
      this.robot_uwb_fir_x = null;
      this.robot_uwb_fir_y = null;
      this.robot_uwb_avr_x = null;
      this.robot_uwb_avr_y = null;
    }
    else {
      if (initObj.hasOwnProperty('robot_uwb_cur_x')) {
        this.robot_uwb_cur_x = initObj.robot_uwb_cur_x
      }
      else {
        this.robot_uwb_cur_x = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_cur_y')) {
        this.robot_uwb_cur_y = initObj.robot_uwb_cur_y
      }
      else {
        this.robot_uwb_cur_y = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_cur_angle')) {
        this.robot_uwb_cur_angle = initObj.robot_uwb_cur_angle
      }
      else {
        this.robot_uwb_cur_angle = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_fir_angle')) {
        this.robot_uwb_fir_angle = initObj.robot_uwb_fir_angle
      }
      else {
        this.robot_uwb_fir_angle = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_fir_x')) {
        this.robot_uwb_fir_x = initObj.robot_uwb_fir_x
      }
      else {
        this.robot_uwb_fir_x = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_fir_y')) {
        this.robot_uwb_fir_y = initObj.robot_uwb_fir_y
      }
      else {
        this.robot_uwb_fir_y = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_avr_x')) {
        this.robot_uwb_avr_x = initObj.robot_uwb_avr_x
      }
      else {
        this.robot_uwb_avr_x = 0.0;
      }
      if (initObj.hasOwnProperty('robot_uwb_avr_y')) {
        this.robot_uwb_avr_y = initObj.robot_uwb_avr_y
      }
      else {
        this.robot_uwb_avr_y = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type uwbdebug
    // Serialize message field [robot_uwb_cur_x]
    bufferOffset = _serializer.float32(obj.robot_uwb_cur_x, buffer, bufferOffset);
    // Serialize message field [robot_uwb_cur_y]
    bufferOffset = _serializer.float32(obj.robot_uwb_cur_y, buffer, bufferOffset);
    // Serialize message field [robot_uwb_cur_angle]
    bufferOffset = _serializer.float32(obj.robot_uwb_cur_angle, buffer, bufferOffset);
    // Serialize message field [robot_uwb_fir_angle]
    bufferOffset = _serializer.float32(obj.robot_uwb_fir_angle, buffer, bufferOffset);
    // Serialize message field [robot_uwb_fir_x]
    bufferOffset = _serializer.float32(obj.robot_uwb_fir_x, buffer, bufferOffset);
    // Serialize message field [robot_uwb_fir_y]
    bufferOffset = _serializer.float32(obj.robot_uwb_fir_y, buffer, bufferOffset);
    // Serialize message field [robot_uwb_avr_x]
    bufferOffset = _serializer.float32(obj.robot_uwb_avr_x, buffer, bufferOffset);
    // Serialize message field [robot_uwb_avr_y]
    bufferOffset = _serializer.float32(obj.robot_uwb_avr_y, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type uwbdebug
    let len;
    let data = new uwbdebug(null);
    // Deserialize message field [robot_uwb_cur_x]
    data.robot_uwb_cur_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_cur_y]
    data.robot_uwb_cur_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_cur_angle]
    data.robot_uwb_cur_angle = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_fir_angle]
    data.robot_uwb_fir_angle = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_fir_x]
    data.robot_uwb_fir_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_fir_y]
    data.robot_uwb_fir_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_avr_x]
    data.robot_uwb_avr_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [robot_uwb_avr_y]
    data.robot_uwb_avr_y = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'humanoid_interface_ros/uwbdebug';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'a496166c5de3c06085e7947afcc759bc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # 机器人uwb x,y 轴滤波后的效果
    float32 robot_uwb_cur_x
    float32 robot_uwb_cur_y
    float32 robot_uwb_cur_angle
    float32 robot_uwb_fir_angle
    float32 robot_uwb_fir_x
    float32 robot_uwb_fir_y
    float32 robot_uwb_avr_x
    float32 robot_uwb_avr_y
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new uwbdebug(null);
    if (msg.robot_uwb_cur_x !== undefined) {
      resolved.robot_uwb_cur_x = msg.robot_uwb_cur_x;
    }
    else {
      resolved.robot_uwb_cur_x = 0.0
    }

    if (msg.robot_uwb_cur_y !== undefined) {
      resolved.robot_uwb_cur_y = msg.robot_uwb_cur_y;
    }
    else {
      resolved.robot_uwb_cur_y = 0.0
    }

    if (msg.robot_uwb_cur_angle !== undefined) {
      resolved.robot_uwb_cur_angle = msg.robot_uwb_cur_angle;
    }
    else {
      resolved.robot_uwb_cur_angle = 0.0
    }

    if (msg.robot_uwb_fir_angle !== undefined) {
      resolved.robot_uwb_fir_angle = msg.robot_uwb_fir_angle;
    }
    else {
      resolved.robot_uwb_fir_angle = 0.0
    }

    if (msg.robot_uwb_fir_x !== undefined) {
      resolved.robot_uwb_fir_x = msg.robot_uwb_fir_x;
    }
    else {
      resolved.robot_uwb_fir_x = 0.0
    }

    if (msg.robot_uwb_fir_y !== undefined) {
      resolved.robot_uwb_fir_y = msg.robot_uwb_fir_y;
    }
    else {
      resolved.robot_uwb_fir_y = 0.0
    }

    if (msg.robot_uwb_avr_x !== undefined) {
      resolved.robot_uwb_avr_x = msg.robot_uwb_avr_x;
    }
    else {
      resolved.robot_uwb_avr_x = 0.0
    }

    if (msg.robot_uwb_avr_y !== undefined) {
      resolved.robot_uwb_avr_y = msg.robot_uwb_avr_y;
    }
    else {
      resolved.robot_uwb_avr_y = 0.0
    }

    return resolved;
    }
};

module.exports = uwbdebug;
