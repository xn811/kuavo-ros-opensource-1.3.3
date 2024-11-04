// Auto-generated. Do not edit!

// (in-package noitom_hi5_hand_udp_python.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class JoySticks {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.left_x = null;
      this.left_y = null;
      this.left_trigger = null;
      this.left_grip = null;
      this.left_first_button_pressed = null;
      this.left_second_button_pressed = null;
      this.left_first_button_touched = null;
      this.left_second_button_touched = null;
      this.right_x = null;
      this.right_y = null;
      this.right_trigger = null;
      this.right_grip = null;
      this.right_first_button_pressed = null;
      this.right_second_button_pressed = null;
      this.right_first_button_touched = null;
      this.right_second_button_touched = null;
    }
    else {
      if (initObj.hasOwnProperty('left_x')) {
        this.left_x = initObj.left_x
      }
      else {
        this.left_x = 0.0;
      }
      if (initObj.hasOwnProperty('left_y')) {
        this.left_y = initObj.left_y
      }
      else {
        this.left_y = 0.0;
      }
      if (initObj.hasOwnProperty('left_trigger')) {
        this.left_trigger = initObj.left_trigger
      }
      else {
        this.left_trigger = 0.0;
      }
      if (initObj.hasOwnProperty('left_grip')) {
        this.left_grip = initObj.left_grip
      }
      else {
        this.left_grip = 0.0;
      }
      if (initObj.hasOwnProperty('left_first_button_pressed')) {
        this.left_first_button_pressed = initObj.left_first_button_pressed
      }
      else {
        this.left_first_button_pressed = false;
      }
      if (initObj.hasOwnProperty('left_second_button_pressed')) {
        this.left_second_button_pressed = initObj.left_second_button_pressed
      }
      else {
        this.left_second_button_pressed = false;
      }
      if (initObj.hasOwnProperty('left_first_button_touched')) {
        this.left_first_button_touched = initObj.left_first_button_touched
      }
      else {
        this.left_first_button_touched = false;
      }
      if (initObj.hasOwnProperty('left_second_button_touched')) {
        this.left_second_button_touched = initObj.left_second_button_touched
      }
      else {
        this.left_second_button_touched = false;
      }
      if (initObj.hasOwnProperty('right_x')) {
        this.right_x = initObj.right_x
      }
      else {
        this.right_x = 0.0;
      }
      if (initObj.hasOwnProperty('right_y')) {
        this.right_y = initObj.right_y
      }
      else {
        this.right_y = 0.0;
      }
      if (initObj.hasOwnProperty('right_trigger')) {
        this.right_trigger = initObj.right_trigger
      }
      else {
        this.right_trigger = 0.0;
      }
      if (initObj.hasOwnProperty('right_grip')) {
        this.right_grip = initObj.right_grip
      }
      else {
        this.right_grip = 0.0;
      }
      if (initObj.hasOwnProperty('right_first_button_pressed')) {
        this.right_first_button_pressed = initObj.right_first_button_pressed
      }
      else {
        this.right_first_button_pressed = false;
      }
      if (initObj.hasOwnProperty('right_second_button_pressed')) {
        this.right_second_button_pressed = initObj.right_second_button_pressed
      }
      else {
        this.right_second_button_pressed = false;
      }
      if (initObj.hasOwnProperty('right_first_button_touched')) {
        this.right_first_button_touched = initObj.right_first_button_touched
      }
      else {
        this.right_first_button_touched = false;
      }
      if (initObj.hasOwnProperty('right_second_button_touched')) {
        this.right_second_button_touched = initObj.right_second_button_touched
      }
      else {
        this.right_second_button_touched = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type JoySticks
    // Serialize message field [left_x]
    bufferOffset = _serializer.float32(obj.left_x, buffer, bufferOffset);
    // Serialize message field [left_y]
    bufferOffset = _serializer.float32(obj.left_y, buffer, bufferOffset);
    // Serialize message field [left_trigger]
    bufferOffset = _serializer.float32(obj.left_trigger, buffer, bufferOffset);
    // Serialize message field [left_grip]
    bufferOffset = _serializer.float32(obj.left_grip, buffer, bufferOffset);
    // Serialize message field [left_first_button_pressed]
    bufferOffset = _serializer.bool(obj.left_first_button_pressed, buffer, bufferOffset);
    // Serialize message field [left_second_button_pressed]
    bufferOffset = _serializer.bool(obj.left_second_button_pressed, buffer, bufferOffset);
    // Serialize message field [left_first_button_touched]
    bufferOffset = _serializer.bool(obj.left_first_button_touched, buffer, bufferOffset);
    // Serialize message field [left_second_button_touched]
    bufferOffset = _serializer.bool(obj.left_second_button_touched, buffer, bufferOffset);
    // Serialize message field [right_x]
    bufferOffset = _serializer.float32(obj.right_x, buffer, bufferOffset);
    // Serialize message field [right_y]
    bufferOffset = _serializer.float32(obj.right_y, buffer, bufferOffset);
    // Serialize message field [right_trigger]
    bufferOffset = _serializer.float32(obj.right_trigger, buffer, bufferOffset);
    // Serialize message field [right_grip]
    bufferOffset = _serializer.float32(obj.right_grip, buffer, bufferOffset);
    // Serialize message field [right_first_button_pressed]
    bufferOffset = _serializer.bool(obj.right_first_button_pressed, buffer, bufferOffset);
    // Serialize message field [right_second_button_pressed]
    bufferOffset = _serializer.bool(obj.right_second_button_pressed, buffer, bufferOffset);
    // Serialize message field [right_first_button_touched]
    bufferOffset = _serializer.bool(obj.right_first_button_touched, buffer, bufferOffset);
    // Serialize message field [right_second_button_touched]
    bufferOffset = _serializer.bool(obj.right_second_button_touched, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type JoySticks
    let len;
    let data = new JoySticks(null);
    // Deserialize message field [left_x]
    data.left_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [left_y]
    data.left_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [left_trigger]
    data.left_trigger = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [left_grip]
    data.left_grip = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [left_first_button_pressed]
    data.left_first_button_pressed = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [left_second_button_pressed]
    data.left_second_button_pressed = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [left_first_button_touched]
    data.left_first_button_touched = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [left_second_button_touched]
    data.left_second_button_touched = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [right_x]
    data.right_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [right_y]
    data.right_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [right_trigger]
    data.right_trigger = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [right_grip]
    data.right_grip = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [right_first_button_pressed]
    data.right_first_button_pressed = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [right_second_button_pressed]
    data.right_second_button_pressed = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [right_first_button_touched]
    data.right_first_button_touched = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [right_second_button_touched]
    data.right_second_button_touched = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 40;
  }

  static datatype() {
    // Returns string type for a message object
    return 'noitom_hi5_hand_udp_python/JoySticks';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c686b65cdd180a9046db651d6492ec65';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 left_x
    float32 left_y
    float32 left_trigger
    float32 left_grip
    bool left_first_button_pressed
    bool left_second_button_pressed
    bool left_first_button_touched
    bool left_second_button_touched
    float32 right_x
    float32 right_y
    float32 right_trigger
    float32 right_grip
    bool right_first_button_pressed
    bool right_second_button_pressed
    bool right_first_button_touched
    bool right_second_button_touched
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new JoySticks(null);
    if (msg.left_x !== undefined) {
      resolved.left_x = msg.left_x;
    }
    else {
      resolved.left_x = 0.0
    }

    if (msg.left_y !== undefined) {
      resolved.left_y = msg.left_y;
    }
    else {
      resolved.left_y = 0.0
    }

    if (msg.left_trigger !== undefined) {
      resolved.left_trigger = msg.left_trigger;
    }
    else {
      resolved.left_trigger = 0.0
    }

    if (msg.left_grip !== undefined) {
      resolved.left_grip = msg.left_grip;
    }
    else {
      resolved.left_grip = 0.0
    }

    if (msg.left_first_button_pressed !== undefined) {
      resolved.left_first_button_pressed = msg.left_first_button_pressed;
    }
    else {
      resolved.left_first_button_pressed = false
    }

    if (msg.left_second_button_pressed !== undefined) {
      resolved.left_second_button_pressed = msg.left_second_button_pressed;
    }
    else {
      resolved.left_second_button_pressed = false
    }

    if (msg.left_first_button_touched !== undefined) {
      resolved.left_first_button_touched = msg.left_first_button_touched;
    }
    else {
      resolved.left_first_button_touched = false
    }

    if (msg.left_second_button_touched !== undefined) {
      resolved.left_second_button_touched = msg.left_second_button_touched;
    }
    else {
      resolved.left_second_button_touched = false
    }

    if (msg.right_x !== undefined) {
      resolved.right_x = msg.right_x;
    }
    else {
      resolved.right_x = 0.0
    }

    if (msg.right_y !== undefined) {
      resolved.right_y = msg.right_y;
    }
    else {
      resolved.right_y = 0.0
    }

    if (msg.right_trigger !== undefined) {
      resolved.right_trigger = msg.right_trigger;
    }
    else {
      resolved.right_trigger = 0.0
    }

    if (msg.right_grip !== undefined) {
      resolved.right_grip = msg.right_grip;
    }
    else {
      resolved.right_grip = 0.0
    }

    if (msg.right_first_button_pressed !== undefined) {
      resolved.right_first_button_pressed = msg.right_first_button_pressed;
    }
    else {
      resolved.right_first_button_pressed = false
    }

    if (msg.right_second_button_pressed !== undefined) {
      resolved.right_second_button_pressed = msg.right_second_button_pressed;
    }
    else {
      resolved.right_second_button_pressed = false
    }

    if (msg.right_first_button_touched !== undefined) {
      resolved.right_first_button_touched = msg.right_first_button_touched;
    }
    else {
      resolved.right_first_button_touched = false
    }

    if (msg.right_second_button_touched !== undefined) {
      resolved.right_second_button_touched = msg.right_second_button_touched;
    }
    else {
      resolved.right_second_button_touched = false
    }

    return resolved;
    }
};

module.exports = JoySticks;
