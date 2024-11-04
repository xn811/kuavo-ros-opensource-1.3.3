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

class armPoseWithTimeStamp {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.offset = null;
      this.left_hand_pose = null;
      this.right_hand_pose = null;
    }
    else {
      if (initObj.hasOwnProperty('offset')) {
        this.offset = initObj.offset
      }
      else {
        this.offset = 0;
      }
      if (initObj.hasOwnProperty('left_hand_pose')) {
        this.left_hand_pose = initObj.left_hand_pose
      }
      else {
        this.left_hand_pose = [];
      }
      if (initObj.hasOwnProperty('right_hand_pose')) {
        this.right_hand_pose = initObj.right_hand_pose
      }
      else {
        this.right_hand_pose = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type armPoseWithTimeStamp
    // Serialize message field [offset]
    bufferOffset = _serializer.int32(obj.offset, buffer, bufferOffset);
    // Serialize message field [left_hand_pose]
    bufferOffset = _arraySerializer.float64(obj.left_hand_pose, buffer, bufferOffset, null);
    // Serialize message field [right_hand_pose]
    bufferOffset = _arraySerializer.float64(obj.right_hand_pose, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type armPoseWithTimeStamp
    let len;
    let data = new armPoseWithTimeStamp(null);
    // Deserialize message field [offset]
    data.offset = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [left_hand_pose]
    data.left_hand_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [right_hand_pose]
    data.right_hand_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.left_hand_pose.length;
    length += 8 * object.right_hand_pose.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/armPoseWithTimeStamp';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '3404338b5cb042ac3b3cf3de3f0fcb4f';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 offset
    float64[] left_hand_pose
    float64[] right_hand_pose
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new armPoseWithTimeStamp(null);
    if (msg.offset !== undefined) {
      resolved.offset = msg.offset;
    }
    else {
      resolved.offset = 0
    }

    if (msg.left_hand_pose !== undefined) {
      resolved.left_hand_pose = msg.left_hand_pose;
    }
    else {
      resolved.left_hand_pose = []
    }

    if (msg.right_hand_pose !== undefined) {
      resolved.right_hand_pose = msg.right_hand_pose;
    }
    else {
      resolved.right_hand_pose = []
    }

    return resolved;
    }
};

module.exports = armPoseWithTimeStamp;
