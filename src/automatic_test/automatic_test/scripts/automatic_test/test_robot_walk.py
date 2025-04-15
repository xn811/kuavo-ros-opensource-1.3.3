#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pytest
import rospy
from std_msgs.msg import String
from enum import Enum
from trace_path.mpc_client_example import start_mpc_tracer, stop_mpc_tracer, back_to_home
from trace_path.mpc_path_tracer import FollowState
from std_msgs.msg import Int8
from std_srvs.srv import Trigger, TriggerRequest

class AutoTrackingStats(Enum):
    NOT_FOLLOWING = 0
    FOLLOWING = 1

follow_state = FollowState.NOT_FOLLOWING
auto_tracking_stats = AutoTrackingStats.FOLLOWING


def follow_state_callback(msg):
    global follow_state
    follow_state = FollowState(msg.data)

def auto_tracking_stats_callback(msg):
    global auto_tracking_stats
    if msg.data == AutoTrackingStats.FOLLOWING.value:
        auto_tracking_stats = AutoTrackingStats.FOLLOWING
    else:
        auto_tracking_stats = AutoTrackingStats.NOT_FOLLOWING

@pytest.mark.usefixtures("ros_setup")
class TestRobotWalk:
    def setup_class(self):
        self.follow_state_sub = rospy.Subscriber('trace_path/follow_state', Int8, follow_state_callback)
        self.auto_tracking_stats_sub = rospy.Subscriber('/auto_tracking_stats', Int8, auto_tracking_stats_callback)
    
    @pytest.mark.walk
    def test_robot_walk(self, check_robot_ready, check_robot_alive, mpc_tracer_process, test_timer):
        round = rospy.get_param('/test_robot_walk/round', 10)
        rospy.loginfo(f"Test Robot Walk Round: {round}")
        while round > 0:
            types = ['circle', 'square', 'scurve']
            for type in types:
                start_mpc_tracer(type)
                rospy.sleep(1.0)
                while follow_state != FollowState.FINISHED:
                    rospy.sleep(0.1)
                    assert check_robot_alive.get_status(), f"机器人死亡: {check_robot_alive.get_error()}"
                    assert auto_tracking_stats == AutoTrackingStats.FOLLOWING, "动捕天轨系统自动跟踪机器人失败"
                back_to_home()
                rospy.sleep(1.0)
                while follow_state != FollowState.FINISHED:
                    rospy.sleep(0.1)
                    assert check_robot_alive.get_status(), f"机器人死亡: {check_robot_alive.get_error()}"
                    assert auto_tracking_stats == AutoTrackingStats.FOLLOWING, "动捕天轨系统自动跟踪机器人失败"
                round -= 1