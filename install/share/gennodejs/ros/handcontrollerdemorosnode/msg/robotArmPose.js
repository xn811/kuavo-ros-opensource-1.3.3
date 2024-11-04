// Auto-generated. Do not edit!

// (in-package handcontrollerdemorosnode.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class robotArmPose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.left_arm_pose = null;
      this.right_arm_pose = null;
    }
    else {
      if (initObj.hasOwnProperty('left_arm_pose')) {
        this.left_arm_pose = initObj.left_arm_pose
      }
      else {
        this.left_arm_pose = [];
      }
      if (initObj.hasOwnProperty('right_arm_pose')) {
        this.right_arm_pose = initObj.right_arm_pose
      }
      else {
        this.right_arm_pose = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type robotArmPose
    // Serialize message field [left_arm_pose]
    bufferOffset = _arraySerializer.float64(obj.left_arm_pose, buffer, bufferOffset, null);
    // Serialize message field [right_arm_pose]
    bufferOffset = _arraySerializer.float64(obj.right_arm_pose, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type robotArmPose
    let len;
    let data = new robotArmPose(null);
    // Deserialize message field [left_arm_pose]
    data.left_arm_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [right_arm_pose]
    data.right_arm_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.left_arm_pose.length;
    length += 8 * object.right_arm_pose.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'handcontrollerdemorosnode/robotArmPose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c281ae760454cca592ca88fb5b3b708b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] left_arm_pose
    float64[] right_arm_pose
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new robotArmPose(null);
    if (msg.left_arm_pose !== undefined) {
      resolved.left_arm_pose = msg.left_arm_pose;
    }
    else {
      resolved.left_arm_pose = []
    }

    if (msg.right_arm_pose !== undefined) {
      resolved.right_arm_pose = msg.right_arm_pose;
    }
    else {
      resolved.right_arm_pose = []
    }

    return resolved;
    }
};

module.exports = robotArmPose;
