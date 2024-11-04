// Auto-generated. Do not edit!

// (in-package kuavo_ros_interfaces.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let bezierCurveCubicPoint = require('./bezierCurveCubicPoint.js');

//-----------------------------------------------------------

class jointBezierTrajectory {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.bezier_curve_points = null;
    }
    else {
      if (initObj.hasOwnProperty('bezier_curve_points')) {
        this.bezier_curve_points = initObj.bezier_curve_points
      }
      else {
        this.bezier_curve_points = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type jointBezierTrajectory
    // Serialize message field [bezier_curve_points]
    // Serialize the length for message field [bezier_curve_points]
    bufferOffset = _serializer.uint32(obj.bezier_curve_points.length, buffer, bufferOffset);
    obj.bezier_curve_points.forEach((val) => {
      bufferOffset = bezierCurveCubicPoint.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type jointBezierTrajectory
    let len;
    let data = new jointBezierTrajectory(null);
    // Deserialize message field [bezier_curve_points]
    // Deserialize array length for message field [bezier_curve_points]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.bezier_curve_points = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.bezier_curve_points[i] = bezierCurveCubicPoint.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.bezier_curve_points.forEach((val) => {
      length += bezierCurveCubicPoint.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_ros_interfaces/jointBezierTrajectory';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '734a11eb72071b59bdbb297c6a53338c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points
    ================================================================================
    MSG: kuavo_ros_interfaces/bezierCurveCubicPoint
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
    const resolved = new jointBezierTrajectory(null);
    if (msg.bezier_curve_points !== undefined) {
      resolved.bezier_curve_points = new Array(msg.bezier_curve_points.length);
      for (let i = 0; i < resolved.bezier_curve_points.length; ++i) {
        resolved.bezier_curve_points[i] = bezierCurveCubicPoint.Resolve(msg.bezier_curve_points[i]);
      }
    }
    else {
      resolved.bezier_curve_points = []
    }

    return resolved;
    }
};

module.exports = jointBezierTrajectory;
