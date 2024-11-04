// Auto-generated. Do not edit!

// (in-package kuavo_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class setHwIntialStateRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.q_intial = null;
      this.v_intial = null;
    }
    else {
      if (initObj.hasOwnProperty('q_intial')) {
        this.q_intial = initObj.q_intial
      }
      else {
        this.q_intial = [];
      }
      if (initObj.hasOwnProperty('v_intial')) {
        this.v_intial = initObj.v_intial
      }
      else {
        this.v_intial = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type setHwIntialStateRequest
    // Serialize message field [q_intial]
    bufferOffset = _arraySerializer.float64(obj.q_intial, buffer, bufferOffset, null);
    // Serialize message field [v_intial]
    bufferOffset = _arraySerializer.float64(obj.v_intial, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type setHwIntialStateRequest
    let len;
    let data = new setHwIntialStateRequest(null);
    // Deserialize message field [q_intial]
    data.q_intial = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [v_intial]
    data.v_intial = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.q_intial.length;
    length += 8 * object.v_intial.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'kuavo_msgs/setHwIntialStateRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e059ca7891626ef7f222daadf24b17ad';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] q_intial  
    float64[] v_intial  
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new setHwIntialStateRequest(null);
    if (msg.q_intial !== undefined) {
      resolved.q_intial = msg.q_intial;
    }
    else {
      resolved.q_intial = []
    }

    if (msg.v_intial !== undefined) {
      resolved.v_intial = msg.v_intial;
    }
    else {
      resolved.v_intial = []
    }

    return resolved;
    }
};

class setHwIntialStateResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
      this.message = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
      if (initObj.hasOwnProperty('message')) {
        this.message = initObj.message
      }
      else {
        this.message = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type setHwIntialStateResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [message]
    bufferOffset = _serializer.string(obj.message, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type setHwIntialStateResponse
    let len;
    let data = new setHwIntialStateResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [message]
    data.message = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.message);
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'kuavo_msgs/setHwIntialStateResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '937c9679a518e3a18d831e57125ea522';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    string message
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new setHwIntialStateResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    if (msg.message !== undefined) {
      resolved.message = msg.message;
    }
    else {
      resolved.message = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: setHwIntialStateRequest,
  Response: setHwIntialStateResponse,
  md5sum() { return '5289a64acc27422c552070b8181b8118'; },
  datatype() { return 'kuavo_msgs/setHwIntialState'; }
};
