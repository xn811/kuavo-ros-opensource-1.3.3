
"use strict";

let robotState = require('./robotState.js');
let footPoseTargetTrajectories = require('./footPoseTargetTrajectories.js');
let footPose = require('./footPose.js');
let armPoseWithTimeStamp = require('./armPoseWithTimeStamp.js');
let endEffectorData = require('./endEffectorData.js');
let gaitTimeName = require('./gaitTimeName.js');
let robotHandPosition = require('./robotHandPosition.js');
let jointCmd = require('./jointCmd.js');
let robotHeadMotionData = require('./robotHeadMotionData.js');
let questJoySticks = require('./questJoySticks.js');
let imuData = require('./imuData.js');
let sensorsData = require('./sensorsData.js');
let headBodyPose = require('./headBodyPose.js');
let jointData = require('./jointData.js');
let armTargetPoses = require('./armTargetPoses.js');

module.exports = {
  robotState: robotState,
  footPoseTargetTrajectories: footPoseTargetTrajectories,
  footPose: footPose,
  armPoseWithTimeStamp: armPoseWithTimeStamp,
  endEffectorData: endEffectorData,
  gaitTimeName: gaitTimeName,
  robotHandPosition: robotHandPosition,
  jointCmd: jointCmd,
  robotHeadMotionData: robotHeadMotionData,
  questJoySticks: questJoySticks,
  imuData: imuData,
  sensorsData: sensorsData,
  headBodyPose: headBodyPose,
  jointData: jointData,
  armTargetPoses: armTargetPoses,
};
