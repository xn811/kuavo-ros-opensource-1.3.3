// Auto-generated. Do not edit!

// (in-package kuavo_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let jointData = require('./jointData.js');
let imuData = require('./imuData.js');
let endEffectorData = require('./endEffectorData.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class sensorsData {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.sensor_time = null;
      this.joint_data = null;
      this.imu_data = null;
      this.end_effector_data = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('sensor_time')) {
        this.sensor_time = initObj.sensor_time
      }
      else {
        this.sensor_time = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('joint_data')) {
        this.joint_data = initObj.joint_data
      }
      else {
        this.joint_data = new jointData();
      }
      if (initObj.hasOwnProperty('imu_data')) {
        this.imu_data = initObj.imu_data
      }
      else {
        this.imu_data = new imuData();
      }
      if (initObj.hasOwnProperty('end_effector_data')) {
        this.end_effector_data = initObj.end_effector_data
      }
      else {
        this.end_effector_data = new endEffectorData();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type sensorsData
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [sensor_time]
    bufferOffset = _serializer.time(obj.sensor_time, buffer, bufferOffset);
    // Serialize message field [joint_data]
    bufferOffset = jointData.serialize(obj.joint_data, buffer, bufferOffset);
    // Serialize message field [imu_data]
    bufferOffset = imuData.serialize(obj.imu_data, buffer, bufferOffset);
    // Serialize message field [end_effector_data]
    bufferOffset = endEffectorData.serialize(obj.end_effector_data, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type sensorsData
    let len;
    let data = new sensorsData(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [sensor_time]
    data.sensor_time = _deserializer.time(buffer, bufferOffset);
    // Deserialize message field [joint_data]
    data.joint_data = jointData.deserialize(buffer, bufferOffset);
    // Deserialize message field [imu_data]
    data.imu_data = imuData.deserialize(buffer, bufferOffset);
    // Deserialize message field [end_effector_data]
    data.end_effector_data = endEffectorData.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += jointData.getMessageSize(object.joint_data);
    length += endEffectorData.getMessageSize(object.end_effector_data);
    return length + 112;
  }

  static datatype() {
    // Returns string type for a message object
    return 'kuavo_msgs/sensorsData';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '54439d3ac2ef33d46fd7cf6d324860c3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    time sensor_time
    kuavo_msgs/jointData joint_data
    kuavo_msgs/imuData imu_data
    kuavo_msgs/endEffectorData end_effector_data
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    ================================================================================
    MSG: kuavo_msgs/jointData
    float64[] joint_q  
    float64[] joint_v  
    float64[] joint_vd    
    float64[] joint_current  
    
    ================================================================================
    MSG: kuavo_msgs/imuData
    geometry_msgs/Vector3 gyro    #陀螺仪数据
    geometry_msgs/Vector3 acc     #加速计数据
    geometry_msgs/Vector3 free_acc    #无重力加速度数据
    geometry_msgs/Quaternion quat    #四元数数据
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    ================================================================================
    MSG: kuavo_msgs/endEffectorData
    string[] name  
    float64[] position
    float64[] velocity  
    float64[] effort
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new sensorsData(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.sensor_time !== undefined) {
      resolved.sensor_time = msg.sensor_time;
    }
    else {
      resolved.sensor_time = {secs: 0, nsecs: 0}
    }

    if (msg.joint_data !== undefined) {
      resolved.joint_data = jointData.Resolve(msg.joint_data)
    }
    else {
      resolved.joint_data = new jointData()
    }

    if (msg.imu_data !== undefined) {
      resolved.imu_data = imuData.Resolve(msg.imu_data)
    }
    else {
      resolved.imu_data = new imuData()
    }

    if (msg.end_effector_data !== undefined) {
      resolved.end_effector_data = endEffectorData.Resolve(msg.end_effector_data)
    }
    else {
      resolved.end_effector_data = new endEffectorData()
    }

    return resolved;
    }
};

module.exports = sensorsData;
