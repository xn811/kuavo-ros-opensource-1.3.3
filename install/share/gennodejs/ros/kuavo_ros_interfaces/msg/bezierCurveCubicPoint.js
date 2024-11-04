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

class bezierCurveCubicPoint {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.end_point = null;
      this.left_control_point = null;
      this.right_control_point = null;
    }
    else {
      if (initObj.hasOwnProperty('end_point')) {
        this.end_point = initObj.end_point
      }
      else {
        this.end_point = [];
      }
      if (initObj.hasOwnProperty('left_control_point')) {
        this.left_control_point = initObj.left_control_point
      }
      else {
        this.left_control_point = [];
      }
      if (initObj.hasOwnProperty('right_control_point')) {
        this.right_control_point = initObj.right_control_point
      }
      else {
        this.right_control_point = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type bezierCurveCubicPoint
    // Serialize message field [end_point]
    bufferOffset = _arraySerializer.float64(obj.end_point, buffer, bufferOffset, null);
    // Serialize message field [left_control_point]
    bufferOffset = _arraySerializer.float64(obj.left_control_point, buffer, bufferOffset, null);
    // Serialize message field [right_control_point]
    bufferOffset = _arraySerializer.float64(obj.right_control_point, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type bezierCurveCubicPoint
    let len;
    let data = new bezierCurveCubicPoint(null);
    // Deserialize message field [end_point]
    data.end_point = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [left_control_point]
    data.left_control_point = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [right_control_point]
    data.right_control_point = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.end_point.length;
    length += 8 * object.left_control_point.length;
    length += 8 * object.right_control_point.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_ros_interfaces/bezierCurveCubicPoint';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4262726b7e41e02a58fb5df3475aa027';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # [x, y] x is time, y is value
    
    float64[] end_point
    float64[] left_control_point
    float64[] right_control_point
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new bezierCurveCubicPoint(null);
    if (msg.end_point !== undefined) {
      resolved.end_point = msg.end_point;
    }
    else {
      resolved.end_point = []
    }

    if (msg.left_control_point !== undefined) {
      resolved.left_control_point = msg.left_control_point;
    }
    else {
      resolved.left_control_point = []
    }

    if (msg.right_control_point !== undefined) {
      resolved.right_control_point = msg.right_control_point;
    }
    else {
      resolved.right_control_point = []
    }

    return resolved;
    }
};

module.exports = bezierCurveCubicPoint;
