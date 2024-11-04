
"use strict";

let changeHandArmPosesByConfigName = require('./changeHandArmPosesByConfigName.js')
let changeAMBACCtrlMode = require('./changeAMBACCtrlMode.js')
let changeArmCtrlMode = require('./changeArmCtrlMode.js')
let srvChangePhases = require('./srvChangePhases.js')
let srvClearPositionCMD = require('./srvClearPositionCMD.js')
let srvchangeCtlMode = require('./srvchangeCtlMode.js')

module.exports = {
  changeHandArmPosesByConfigName: changeHandArmPosesByConfigName,
  changeAMBACCtrlMode: changeAMBACCtrlMode,
  changeArmCtrlMode: changeArmCtrlMode,
  srvChangePhases: srvChangePhases,
  srvClearPositionCMD: srvClearPositionCMD,
  srvchangeCtlMode: srvchangeCtlMode,
};
