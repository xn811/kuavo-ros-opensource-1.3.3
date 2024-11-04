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

class footPose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.footPose = null;
      this.torsoPose = null;
    }
    else {
      if (initObj.hasOwnProperty('footPose')) {
        this.footPose = initObj.footPose
      }
      else {
        this.footPose = new Array(4).fill(0);
      }
      if (initObj.hasOwnProperty('torsoPose')) {
        this.torsoPose = initObj.torsoPose
      }
      else {
        this.torsoPose = new Array(4).fill(0);
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type footPose
    // Check that the constant length array field [footPose] has the right length
    if (obj.footPose.length !== 4) {
      throw new Error('Unable to serialize array field footPose - length must be 4')
    }
    // Serialize message field [footPose]
    bufferOffset = _arraySerializer.float64(obj.footPose, buffer, bufferOffset, 4);
    // Check that the constant length array field [torsoPose] has the right length
    if (obj.torsoPose.length !== 4) {
      throw new Error('Unable to serialize array field torsoPose - length must be 4')
    }
    // Serialize message field [torsoPose]
    bufferOffset = _arraySerializer.float64(obj.torsoPose, buffer, bufferOffset, 4);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type footPose
    let len;
    let data = new footPose(null);
    // Deserialize message field [footPose]
    data.footPose = _arrayDeserializer.float64(buffer, bufferOffset, 4)
    // Deserialize message field [torsoPose]
    data.torsoPose = _arrayDeserializer.float64(buffer, bufferOffset, 4)
    return data;
  }

  static getMessageSize(object) {
    return 64;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/footPose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b0acb7ad1ed1ee5a0a630b91b650f49a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[4] footPose # x, y, z, yaw
    float64[4] torsoPose # x, y, z, yaw
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new footPose(null);
    if (msg.footPose !== undefined) {
      resolved.footPose = msg.footPose;
    }
    else {
      resolved.footPose = new Array(4).fill(0)
    }

    if (msg.torsoPose !== undefined) {
      resolved.torsoPose = msg.torsoPose;
    }
    else {
      resolved.torsoPose = new Array(4).fill(0)
    }

    return resolved;
    }
};

module.exports = footPose;
