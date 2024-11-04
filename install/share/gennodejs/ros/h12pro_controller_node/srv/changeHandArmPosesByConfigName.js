// Auto-generated. Do not edit!

// (in-package h12pro_controller_node.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class changeHandArmPosesByConfigNameRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.config_name = null;
    }
    else {
      if (initObj.hasOwnProperty('config_name')) {
        this.config_name = initObj.config_name
      }
      else {
        this.config_name = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type changeHandArmPosesByConfigNameRequest
    // Serialize message field [config_name]
    bufferOffset = _serializer.string(obj.config_name, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type changeHandArmPosesByConfigNameRequest
    let len;
    let data = new changeHandArmPosesByConfigNameRequest(null);
    // Deserialize message field [config_name]
    data.config_name = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.config_name);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'h12pro_controller_node/changeHandArmPosesByConfigNameRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'a0441cdaccb9fc3beee1100121e03428';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string config_name
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new changeHandArmPosesByConfigNameRequest(null);
    if (msg.config_name !== undefined) {
      resolved.config_name = msg.config_name;
    }
    else {
      resolved.config_name = ''
    }

    return resolved;
    }
};

class changeHandArmPosesByConfigNameResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.result = null;
    }
    else {
      if (initObj.hasOwnProperty('result')) {
        this.result = initObj.result
      }
      else {
        this.result = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type changeHandArmPosesByConfigNameResponse
    // Serialize message field [result]
    bufferOffset = _serializer.bool(obj.result, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type changeHandArmPosesByConfigNameResponse
    let len;
    let data = new changeHandArmPosesByConfigNameResponse(null);
    // Deserialize message field [result]
    data.result = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'h12pro_controller_node/changeHandArmPosesByConfigNameResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'eb13ac1f1354ccecb7941ee8fa2192e8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool result
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new changeHandArmPosesByConfigNameResponse(null);
    if (msg.result !== undefined) {
      resolved.result = msg.result;
    }
    else {
      resolved.result = false
    }

    return resolved;
    }
};

module.exports = {
  Request: changeHandArmPosesByConfigNameRequest,
  Response: changeHandArmPosesByConfigNameResponse,
  md5sum() { return '981617b9cc6699ade1d3c011b67988a7'; },
  datatype() { return 'h12pro_controller_node/changeHandArmPosesByConfigName'; }
};
