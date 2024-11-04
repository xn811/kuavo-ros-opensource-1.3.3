
"use strict";

let setHwIntialState = require('./setHwIntialState.js')
let singleStepControl = require('./singleStepControl.js')
let changeTorsoCtrlMode = require('./changeTorsoCtrlMode.js')
let jointMoveTo = require('./jointMoveTo.js')
let changeArmCtrlMode = require('./changeArmCtrlMode.js')

module.exports = {
  setHwIntialState: setHwIntialState,
  singleStepControl: singleStepControl,
  changeTorsoCtrlMode: changeTorsoCtrlMode,
  jointMoveTo: jointMoveTo,
  changeArmCtrlMode: changeArmCtrlMode,
};
