// Auto-generated. Do not edit!

// (in-package h12pro_controller_node.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class h12proRemoteControllerChannel {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.channels = null;
      this.sbus_state = null;
    }
    else {
      if (initObj.hasOwnProperty('channels')) {
        this.channels = initObj.channels
      }
      else {
        this.channels = [];
      }
      if (initObj.hasOwnProperty('sbus_state')) {
        this.sbus_state = initObj.sbus_state
      }
      else {
        this.sbus_state = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type h12proRemoteControllerChannel
    // Serialize message field [channels]
    bufferOffset = _arraySerializer.uint16(obj.channels, buffer, bufferOffset, null);
    // Serialize message field [sbus_state]
    bufferOffset = _serializer.uint8(obj.sbus_state, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type h12proRemoteControllerChannel
    let len;
    let data = new h12proRemoteControllerChannel(null);
    // Deserialize message field [channels]
    data.channels = _arrayDeserializer.uint16(buffer, bufferOffset, null)
    // Deserialize message field [sbus_state]
    data.sbus_state = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 2 * object.channels.length;
    return length + 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'h12pro_controller_node/h12proRemoteControllerChannel';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'fbc04b5769be8336707a1083b8b107dd';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint16[] channels
    uint8 sbus_state
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new h12proRemoteControllerChannel(null);
    if (msg.channels !== undefined) {
      resolved.channels = msg.channels;
    }
    else {
      resolved.channels = []
    }

    if (msg.sbus_state !== undefined) {
      resolved.sbus_state = msg.sbus_state;
    }
    else {
      resolved.sbus_state = 0
    }

    return resolved;
    }
};

module.exports = h12proRemoteControllerChannel;
