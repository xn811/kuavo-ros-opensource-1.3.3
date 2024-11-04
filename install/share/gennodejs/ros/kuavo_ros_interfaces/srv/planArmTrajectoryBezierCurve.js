// Auto-generated. Do not edit!

// (in-package kuavo_ros_interfaces.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let jointBezierTrajectory = require('../msg/jointBezierTrajectory.js');

//-----------------------------------------------------------


//-----------------------------------------------------------

class planArmTrajectoryBezierCurveRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.multi_joint_bezier_trajectory = null;
      this.start_frame_time = null;
      this.end_frame_time = null;
      this.joint_names = null;
    }
    else {
      if (initObj.hasOwnProperty('multi_joint_bezier_trajectory')) {
        this.multi_joint_bezier_trajectory = initObj.multi_joint_bezier_trajectory
      }
      else {
        this.multi_joint_bezier_trajectory = [];
      }
      if (initObj.hasOwnProperty('start_frame_time')) {
        this.start_frame_time = initObj.start_frame_time
      }
      else {
        this.start_frame_time = 0.0;
      }
      if (initObj.hasOwnProperty('end_frame_time')) {
        this.end_frame_time = initObj.end_frame_time
      }
      else {
        this.end_frame_time = 0.0;
      }
      if (initObj.hasOwnProperty('joint_names')) {
        this.joint_names = initObj.joint_names
      }
      else {
        this.joint_names = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type planArmTrajectoryBezierCurveRequest
    // Serialize message field [multi_joint_bezier_trajectory]
    // Serialize the length for message field [multi_joint_bezier_trajectory]
    bufferOffset = _serializer.uint32(obj.multi_joint_bezier_trajectory.length, buffer, bufferOffset);
    obj.multi_joint_bezier_trajectory.forEach((val) => {
      bufferOffset = jointBezierTrajectory.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [start_frame_time]
    bufferOffset = _serializer.float64(obj.start_frame_time, buffer, bufferOffset);
    // Serialize message field [end_frame_time]
    bufferOffset = _serializer.float64(obj.end_frame_time, buffer, bufferOffset);
    // Serialize message field [joint_names]
    bufferOffset = _arraySerializer.string(obj.joint_names, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type planArmTrajectoryBezierCurveRequest
    let len;
    let data = new planArmTrajectoryBezierCurveRequest(null);
    // Deserialize message field [multi_joint_bezier_trajectory]
    // Deserialize array length for message field [multi_joint_bezier_trajectory]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.multi_joint_bezier_trajectory = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.multi_joint_bezier_trajectory[i] = jointBezierTrajectory.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [start_frame_time]
    data.start_frame_time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [end_frame_time]
    data.end_frame_time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint_names]
    data.joint_names = _arrayDeserializer.string(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.multi_joint_bezier_trajectory.forEach((val) => {
      length += jointBezierTrajectory.getMessageSize(val);
    });
    object.joint_names.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    return length + 24;
  }

  static datatype() {
    // Returns string type for a service object
    return 'kuavo_ros_interfaces/planArmTrajectoryBezierCurveRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'fd4c2b9f2a4883680ef63a437da922a8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    kuavo_ros_interfaces/jointBezierTrajectory[] multi_joint_bezier_trajectory
    float64 start_frame_time
    float64 end_frame_time
    string[] joint_names
    
    ================================================================================
    MSG: kuavo_ros_interfaces/jointBezierTrajectory
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
    const resolved = new planArmTrajectoryBezierCurveRequest(null);
    if (msg.multi_joint_bezier_trajectory !== undefined) {
      resolved.multi_joint_bezier_trajectory = new Array(msg.multi_joint_bezier_trajectory.length);
      for (let i = 0; i < resolved.multi_joint_bezier_trajectory.length; ++i) {
        resolved.multi_joint_bezier_trajectory[i] = jointBezierTrajectory.Resolve(msg.multi_joint_bezier_trajectory[i]);
      }
    }
    else {
      resolved.multi_joint_bezier_trajectory = []
    }

    if (msg.start_frame_time !== undefined) {
      resolved.start_frame_time = msg.start_frame_time;
    }
    else {
      resolved.start_frame_time = 0.0
    }

    if (msg.end_frame_time !== undefined) {
      resolved.end_frame_time = msg.end_frame_time;
    }
    else {
      resolved.end_frame_time = 0.0
    }

    if (msg.joint_names !== undefined) {
      resolved.joint_names = msg.joint_names;
    }
    else {
      resolved.joint_names = []
    }

    return resolved;
    }
};

class planArmTrajectoryBezierCurveResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type planArmTrajectoryBezierCurveResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type planArmTrajectoryBezierCurveResponse
    let len;
    let data = new planArmTrajectoryBezierCurveResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'kuavo_ros_interfaces/planArmTrajectoryBezierCurveResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '358e233cde0c8a8bcfea4ce193f8fc15';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new planArmTrajectoryBezierCurveResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    return resolved;
    }
};

module.exports = {
  Request: planArmTrajectoryBezierCurveRequest,
  Response: planArmTrajectoryBezierCurveResponse,
  md5sum() { return '4dbc940608d7275f775b6fdef47eb369'; },
  datatype() { return 'kuavo_ros_interfaces/planArmTrajectoryBezierCurve'; }
};
