// Auto-generated. Do not edit!

// (in-package noitom_hi5_hand_udp_python.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Vector4 = require('./Vector4.js');

//-----------------------------------------------------------

class handRotationEular {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.eulerAngles = null;
    }
    else {
      if (initObj.hasOwnProperty('eulerAngles')) {
        this.eulerAngles = initObj.eulerAngles
      }
      else {
        this.eulerAngles = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type handRotationEular
    // Serialize message field [eulerAngles]
    // Serialize the length for message field [eulerAngles]
    bufferOffset = _serializer.uint32(obj.eulerAngles.length, buffer, bufferOffset);
    obj.eulerAngles.forEach((val) => {
      bufferOffset = Vector4.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type handRotationEular
    let len;
    let data = new handRotationEular(null);
    // Deserialize message field [eulerAngles]
    // Deserialize array length for message field [eulerAngles]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.eulerAngles = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.eulerAngles[i] = Vector4.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 16 * object.eulerAngles.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'noitom_hi5_hand_udp_python/handRotationEular';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '75ea7fdfd1913bbabb0a96c424b42024';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    noitom_hi5_hand_udp_python/Vector4[] eulerAngles
    
    ================================================================================
    MSG: noitom_hi5_hand_udp_python/Vector4
    float32 x
    float32 y
    float32 z
    float32 w
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new handRotationEular(null);
    if (msg.eulerAngles !== undefined) {
      resolved.eulerAngles = new Array(msg.eulerAngles.length);
      for (let i = 0; i < resolved.eulerAngles.length; ++i) {
        resolved.eulerAngles[i] = Vector4.Resolve(msg.eulerAngles[i]);
      }
    }
    else {
      resolved.eulerAngles = []
    }

    return resolved;
    }
};

module.exports = handRotationEular;
