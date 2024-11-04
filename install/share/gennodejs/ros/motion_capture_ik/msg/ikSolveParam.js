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

class ikSolveParam {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.major_optimality_tol = null;
      this.major_feasibility_tol = null;
      this.minor_feasibility_tol = null;
      this.major_iterations_limit = null;
      this.oritation_constraint_tol = null;
      this.pos_constraint_tol = null;
      this.pos_cost_weight = null;
    }
    else {
      if (initObj.hasOwnProperty('major_optimality_tol')) {
        this.major_optimality_tol = initObj.major_optimality_tol
      }
      else {
        this.major_optimality_tol = 0.0;
      }
      if (initObj.hasOwnProperty('major_feasibility_tol')) {
        this.major_feasibility_tol = initObj.major_feasibility_tol
      }
      else {
        this.major_feasibility_tol = 0.0;
      }
      if (initObj.hasOwnProperty('minor_feasibility_tol')) {
        this.minor_feasibility_tol = initObj.minor_feasibility_tol
      }
      else {
        this.minor_feasibility_tol = 0.0;
      }
      if (initObj.hasOwnProperty('major_iterations_limit')) {
        this.major_iterations_limit = initObj.major_iterations_limit
      }
      else {
        this.major_iterations_limit = 0.0;
      }
      if (initObj.hasOwnProperty('oritation_constraint_tol')) {
        this.oritation_constraint_tol = initObj.oritation_constraint_tol
      }
      else {
        this.oritation_constraint_tol = 0.0;
      }
      if (initObj.hasOwnProperty('pos_constraint_tol')) {
        this.pos_constraint_tol = initObj.pos_constraint_tol
      }
      else {
        this.pos_constraint_tol = 0.0;
      }
      if (initObj.hasOwnProperty('pos_cost_weight')) {
        this.pos_cost_weight = initObj.pos_cost_weight
      }
      else {
        this.pos_cost_weight = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ikSolveParam
    // Serialize message field [major_optimality_tol]
    bufferOffset = _serializer.float64(obj.major_optimality_tol, buffer, bufferOffset);
    // Serialize message field [major_feasibility_tol]
    bufferOffset = _serializer.float64(obj.major_feasibility_tol, buffer, bufferOffset);
    // Serialize message field [minor_feasibility_tol]
    bufferOffset = _serializer.float64(obj.minor_feasibility_tol, buffer, bufferOffset);
    // Serialize message field [major_iterations_limit]
    bufferOffset = _serializer.float64(obj.major_iterations_limit, buffer, bufferOffset);
    // Serialize message field [oritation_constraint_tol]
    bufferOffset = _serializer.float64(obj.oritation_constraint_tol, buffer, bufferOffset);
    // Serialize message field [pos_constraint_tol]
    bufferOffset = _serializer.float64(obj.pos_constraint_tol, buffer, bufferOffset);
    // Serialize message field [pos_cost_weight]
    bufferOffset = _serializer.float64(obj.pos_cost_weight, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ikSolveParam
    let len;
    let data = new ikSolveParam(null);
    // Deserialize message field [major_optimality_tol]
    data.major_optimality_tol = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [major_feasibility_tol]
    data.major_feasibility_tol = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [minor_feasibility_tol]
    data.minor_feasibility_tol = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [major_iterations_limit]
    data.major_iterations_limit = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [oritation_constraint_tol]
    data.oritation_constraint_tol = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [pos_constraint_tol]
    data.pos_constraint_tol = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [pos_cost_weight]
    data.pos_cost_weight = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 56;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motion_capture_ik/ikSolveParam';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'be29d8b02ad14da680464b8c4f590f98';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # snopt params
    float64 major_optimality_tol
    float64 major_feasibility_tol
    float64 minor_feasibility_tol
    float64 major_iterations_limit
    # constraint and cost params
    float64 oritation_constraint_tol
    float64 pos_constraint_tol # work when pos_cost_weight > 0.0
    float64 pos_cost_weight
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ikSolveParam(null);
    if (msg.major_optimality_tol !== undefined) {
      resolved.major_optimality_tol = msg.major_optimality_tol;
    }
    else {
      resolved.major_optimality_tol = 0.0
    }

    if (msg.major_feasibility_tol !== undefined) {
      resolved.major_feasibility_tol = msg.major_feasibility_tol;
    }
    else {
      resolved.major_feasibility_tol = 0.0
    }

    if (msg.minor_feasibility_tol !== undefined) {
      resolved.minor_feasibility_tol = msg.minor_feasibility_tol;
    }
    else {
      resolved.minor_feasibility_tol = 0.0
    }

    if (msg.major_iterations_limit !== undefined) {
      resolved.major_iterations_limit = msg.major_iterations_limit;
    }
    else {
      resolved.major_iterations_limit = 0.0
    }

    if (msg.oritation_constraint_tol !== undefined) {
      resolved.oritation_constraint_tol = msg.oritation_constraint_tol;
    }
    else {
      resolved.oritation_constraint_tol = 0.0
    }

    if (msg.pos_constraint_tol !== undefined) {
      resolved.pos_constraint_tol = msg.pos_constraint_tol;
    }
    else {
      resolved.pos_constraint_tol = 0.0
    }

    if (msg.pos_cost_weight !== undefined) {
      resolved.pos_cost_weight = msg.pos_cost_weight;
    }
    else {
      resolved.pos_cost_weight = 0.0
    }

    return resolved;
    }
};

module.exports = ikSolveParam;
