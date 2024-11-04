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

class armTargetPoses {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.times = null;
      this.values = null;
    }
    else {
      if (initObj.hasOwnProperty('times')) {
        this.times = initObj.times
      }
      else {
        this.times = [];
      }
      if (initObj.hasOwnProperty('values')) {
        this.values = initObj.values
      }
      else {
        this.values = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type armTargetPoses
    // Serialize message field [times]
    bufferOffset = _arraySerializer.float64(obj.times, buffer, bufferOffset, null);
    // Serialize message field [values]
    bufferOffset = _arraySerializer.float64(obj.values, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type armTargetPoses
    let len;
    let data = new armTargetPoses(null);
    // Deserialize message field [times]
    data.times = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [values]
    data.values = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.times.length;
    length += 8 * object.values.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/armTargetPoses';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '267055a1a7e685e90c17a3ebf7a8a26c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # times: times series
    # values: values matrix
    float64[] times
    float64[] values
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new armTargetPoses(null);
    if (msg.times !== undefined) {
      resolved.times = msg.times;
    }
    else {
      resolved.times = []
    }

    if (msg.values !== undefined) {
      resolved.values = msg.values;
    }
    else {
      resolved.values = []
    }

    return resolved;
    }
};

module.exports = armTargetPoses;
