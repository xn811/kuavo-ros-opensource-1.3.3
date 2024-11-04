// Auto-generated. Do not edit!

// (in-package motion_capture_ik.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let handPose = require('./handPose.js');

//-----------------------------------------------------------

class ikSolveError {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.ik_type = null;
      this.left_pose_error = null;
      this.right_pose_error = null;
    }
    else {
      if (initObj.hasOwnProperty('ik_type')) {
        this.ik_type = initObj.ik_type
      }
      else {
        this.ik_type = '';
      }
      if (initObj.hasOwnProperty('left_pose_error')) {
        this.left_pose_error = initObj.left_pose_error
      }
      else {
        this.left_pose_error = new handPose();
      }
      if (initObj.hasOwnProperty('right_pose_error')) {
        this.right_pose_error = initObj.right_pose_error
      }
      else {
        this.right_pose_error = new handPose();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ikSolveError
    // Serialize message field [ik_type]
    bufferOffset = _serializer.string(obj.ik_type, buffer, bufferOffset);
    // Serialize message field [left_pose_error]
    bufferOffset = handPose.serialize(obj.left_pose_error, buffer, bufferOffset);
    // Serialize message field [right_pose_error]
    bufferOffset = handPose.serialize(obj.right_pose_error, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ikSolveError
    let len;
    let data = new ikSolveError(null);
    // Deserialize message field [ik_type]
    data.ik_type = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [left_pose_error]
    data.left_pose_error = handPose.deserialize(buffer, bufferOffset);
    // Deserialize message field [right_pose_error]
    data.right_pose_error = handPose.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.ik_type);
    return length + 100;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motion_capture_ik/ikSolveError';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '06c12c0e6e08f286627a6f856e26223c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string     ik_type 
    handPose  left_pose_error
    handPose  right_pose_error
    ================================================================================
    MSG: motion_capture_ik/handPose
    # pos
    float64 x
    float64 y
    float64 z
    # rpy
    float64 roll
    float64 pitch
    float64 yaw
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ikSolveError(null);
    if (msg.ik_type !== undefined) {
      resolved.ik_type = msg.ik_type;
    }
    else {
      resolved.ik_type = ''
    }

    if (msg.left_pose_error !== undefined) {
      resolved.left_pose_error = handPose.Resolve(msg.left_pose_error)
    }
    else {
      resolved.left_pose_error = new handPose()
    }

    if (msg.right_pose_error !== undefined) {
      resolved.right_pose_error = handPose.Resolve(msg.right_pose_error)
    }
    else {
      resolved.right_pose_error = new handPose()
    }

    return resolved;
    }
};

module.exports = ikSolveError;
