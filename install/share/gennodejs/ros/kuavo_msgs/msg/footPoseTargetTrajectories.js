// Auto-generated. Do not edit!

// (in-package kuavo_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let footPose = require('./footPose.js');

//-----------------------------------------------------------

class footPoseTargetTrajectories {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.timeTrajectory = null;
      this.footIndexTrajectory = null;
      this.footPoseTrajectory = null;
    }
    else {
      if (initObj.hasOwnProperty('timeTrajectory')) {
        this.timeTrajectory = initObj.timeTrajectory
      }
      else {
        this.timeTrajectory = [];
      }
      if (initObj.hasOwnProperty('footIndexTrajectory')) {
        this.footIndexTrajectory = initObj.footIndexTrajectory
      }
      else {
        this.footIndexTrajectory = [];
      }
      if (initObj.hasOwnProperty('footPoseTrajectory')) {
        this.footPoseTrajectory = initObj.footPoseTrajectory
      }
      else {
        this.footPoseTrajectory = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type footPoseTargetTrajectories
    // Serialize message field [timeTrajectory]
    bufferOffset = _arraySerializer.float64(obj.timeTrajectory, buffer, bufferOffset, null);
    // Serialize message field [footIndexTrajectory]
    bufferOffset = _arraySerializer.int32(obj.footIndexTrajectory, buffer, bufferOffset, null);
    // Serialize message field [footPoseTrajectory]
    // Serialize the length for message field [footPoseTrajectory]
    bufferOffset = _serializer.uint32(obj.footPoseTrajectory.length, buffer, bufferOffset);
    obj.footPoseTrajectory.forEach((val) => {
      bufferOffset = footPose.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type footPoseTargetTrajectories
    let len;
    let data = new footPoseTargetTrajectories(null);
    // Deserialize message field [timeTrajectory]
    data.timeTrajectory = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [footIndexTrajectory]
    data.footIndexTrajectory = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [footPoseTrajectory]
    // Deserialize array length for message field [footPoseTrajectory]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.footPoseTrajectory = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.footPoseTrajectory[i] = footPose.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.timeTrajectory.length;
    length += 4 * object.footIndexTrajectory.length;
    length += 64 * object.footPoseTrajectory.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/footPoseTargetTrajectories';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '6854923406c37831b40979cd2570e027';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[]    timeTrajectory
    int32[]      footIndexTrajectory
    footPose[]   footPoseTrajectory
    ================================================================================
    MSG: kuavo_msgs/footPose
    float64[4] footPose # x, y, z, yaw
    float64[4] torsoPose # x, y, z, yaw
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new footPoseTargetTrajectories(null);
    if (msg.timeTrajectory !== undefined) {
      resolved.timeTrajectory = msg.timeTrajectory;
    }
    else {
      resolved.timeTrajectory = []
    }

    if (msg.footIndexTrajectory !== undefined) {
      resolved.footIndexTrajectory = msg.footIndexTrajectory;
    }
    else {
      resolved.footIndexTrajectory = []
    }

    if (msg.footPoseTrajectory !== undefined) {
      resolved.footPoseTrajectory = new Array(msg.footPoseTrajectory.length);
      for (let i = 0; i < resolved.footPoseTrajectory.length; ++i) {
        resolved.footPoseTrajectory[i] = footPose.Resolve(msg.footPoseTrajectory[i]);
      }
    }
    else {
      resolved.footPoseTrajectory = []
    }

    return resolved;
    }
};

module.exports = footPoseTargetTrajectories;
