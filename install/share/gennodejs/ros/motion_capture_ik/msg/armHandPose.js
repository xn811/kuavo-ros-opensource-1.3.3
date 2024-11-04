// Auto-generated. Do not edit!

// (in-package motion_capture_ik.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class armHandPose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pos_xyz = null;
      this.quat_xyzw = null;
      this.elbow_pos_xyz = null;
      this.joint_angles = null;
    }
    else {
      if (initObj.hasOwnProperty('pos_xyz')) {
        this.pos_xyz = initObj.pos_xyz
      }
      else {
        this.pos_xyz = new Array(3).fill(0);
      }
      if (initObj.hasOwnProperty('quat_xyzw')) {
        this.quat_xyzw = initObj.quat_xyzw
      }
      else {
        this.quat_xyzw = new Array(4).fill(0);
      }
      if (initObj.hasOwnProperty('elbow_pos_xyz')) {
        this.elbow_pos_xyz = initObj.elbow_pos_xyz
      }
      else {
        this.elbow_pos_xyz = new Array(3).fill(0);
      }
      if (initObj.hasOwnProperty('joint_angles')) {
        this.joint_angles = initObj.joint_angles
      }
      else {
        this.joint_angles = new Array(7).fill(0);
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type armHandPose
    // Check that the constant length array field [pos_xyz] has the right length
    if (obj.pos_xyz.length !== 3) {
      throw new Error('Unable to serialize array field pos_xyz - length must be 3')
    }
    // Serialize message field [pos_xyz]
    bufferOffset = _arraySerializer.float64(obj.pos_xyz, buffer, bufferOffset, 3);
    // Check that the constant length array field [quat_xyzw] has the right length
    if (obj.quat_xyzw.length !== 4) {
      throw new Error('Unable to serialize array field quat_xyzw - length must be 4')
    }
    // Serialize message field [quat_xyzw]
    bufferOffset = _arraySerializer.float64(obj.quat_xyzw, buffer, bufferOffset, 4);
    // Check that the constant length array field [elbow_pos_xyz] has the right length
    if (obj.elbow_pos_xyz.length !== 3) {
      throw new Error('Unable to serialize array field elbow_pos_xyz - length must be 3')
    }
    // Serialize message field [elbow_pos_xyz]
    bufferOffset = _arraySerializer.float64(obj.elbow_pos_xyz, buffer, bufferOffset, 3);
    // Check that the constant length array field [joint_angles] has the right length
    if (obj.joint_angles.length !== 7) {
      throw new Error('Unable to serialize array field joint_angles - length must be 7')
    }
    // Serialize message field [joint_angles]
    bufferOffset = _arraySerializer.float64(obj.joint_angles, buffer, bufferOffset, 7);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type armHandPose
    let len;
    let data = new armHandPose(null);
    // Deserialize message field [pos_xyz]
    data.pos_xyz = _arrayDeserializer.float64(buffer, bufferOffset, 3)
    // Deserialize message field [quat_xyzw]
    data.quat_xyzw = _arrayDeserializer.float64(buffer, bufferOffset, 4)
    // Deserialize message field [elbow_pos_xyz]
    data.elbow_pos_xyz = _arrayDeserializer.float64(buffer, bufferOffset, 3)
    // Deserialize message field [joint_angles]
    data.joint_angles = _arrayDeserializer.float64(buffer, bufferOffset, 7)
    return data;
  }

  static getMessageSize(object) {
    return 136;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motion_capture_ik/armHandPose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4f28a253cb60d59c6491569369f38f4d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[3] pos_xyz
    float64[4] quat_xyzw
    
    float64[3] elbow_pos_xyz
    
    float64[7] joint_angles
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new armHandPose(null);
    if (msg.pos_xyz !== undefined) {
      resolved.pos_xyz = msg.pos_xyz;
    }
    else {
      resolved.pos_xyz = new Array(3).fill(0)
    }

    if (msg.quat_xyzw !== undefined) {
      resolved.quat_xyzw = msg.quat_xyzw;
    }
    else {
      resolved.quat_xyzw = new Array(4).fill(0)
    }

    if (msg.elbow_pos_xyz !== undefined) {
      resolved.elbow_pos_xyz = msg.elbow_pos_xyz;
    }
    else {
      resolved.elbow_pos_xyz = new Array(3).fill(0)
    }

    if (msg.joint_angles !== undefined) {
      resolved.joint_angles = msg.joint_angles;
    }
    else {
      resolved.joint_angles = new Array(7).fill(0)
    }

    return resolved;
    }
};

module.exports = armHandPose;
