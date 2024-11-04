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

class robotHeadMotionData {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.joint_data = null;
    }
    else {
      if (initObj.hasOwnProperty('joint_data')) {
        this.joint_data = initObj.joint_data
      }
      else {
        this.joint_data = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type robotHeadMotionData
    // Serialize message field [joint_data]
    bufferOffset = _arraySerializer.float64(obj.joint_data, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type robotHeadMotionData
    let len;
    let data = new robotHeadMotionData(null);
    // Deserialize message field [joint_data]
    data.joint_data = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.joint_data.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/robotHeadMotionData';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '400001e7cf73111efbced59084cb481a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # robotHeadMotionData.msg
    # 
    # - joint_data[0] : yaw,   [-30, 30]
    # - joint_data[1] : pitch, [-25, 25]
    #
    # - [-8.000000, 0.000000]
    
    float64[] joint_data
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new robotHeadMotionData(null);
    if (msg.joint_data !== undefined) {
      resolved.joint_data = msg.joint_data;
    }
    else {
      resolved.joint_data = []
    }

    return resolved;
    }
};

module.exports = robotHeadMotionData;
