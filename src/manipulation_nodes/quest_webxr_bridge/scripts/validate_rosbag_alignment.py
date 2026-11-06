#!/usr/bin/env python3
"""Validate that a WebXR bag has the stock Quest3 data-collection contract."""

import argparse
import bisect
import statistics
import sys

import rosbag
import roslib.message

from quest_webxr_bridge.recording_contract import (
    ARM_JOINT_NAMES, CONTROL_MD5, CONTROL_TOPICS, RECORDING_PROFILES,
    profile_optional_topics, profile_topics,
)


def first_message(bag, topic):
    for _, message, _ in bag.read_messages(topics=[topic]):
        return message
    return None


def validate_payload(topic, message):
    if message is None:
        return "contains no messages"
    if topic == "/kuavo_arm_traj":
        if tuple(message.name) != ARM_JOINT_NAMES:
            return "JointState.name is not arm_joint_1..arm_joint_14"
        if len(message.position) != 14:
            return "JointState.position does not contain 14 arm joints"
        if len(message.velocity) != 14:
            return "JointState.velocity does not contain 14 arm joints"
        if len(message.effort) != 14:
            return "JointState.effort does not contain 14 arm joints"
    elif topic == "/control_robot_hand_position":
        if len(message.left_hand_position) != 6 or len(message.right_hand_position) != 6:
            return "robotHandPosition does not contain 6 channels per hand"
    elif topic == "/robot_head_motion_data":
        if len(message.joint_data) != 2:
            return "robotHeadMotionData.joint_data is not [yaw, pitch]"
    return None


def timing_contract(path):
    control_topics = [
        "/kuavo_arm_traj",
        "/control_robot_hand_position",
        "/robot_head_motion_data",
    ]
    times = {topic: [] for topic in control_topics}
    header_lag = {topic: [] for topic in control_topics}
    with rosbag.Bag(path, "r") as bag:
        for topic, message, bag_time in bag.read_messages(topics=control_topics):
            stamp = bag_time.to_sec()
            times[topic].append(stamp)
            if hasattr(message, "header") and message.header.stamp.to_sec() > 0.0:
                header_lag[topic].append(stamp - message.header.stamp.to_sec())

    metrics = {}
    for topic in control_topics:
        values = times[topic]
        intervals = [b - a for a, b in zip(values, values[1:]) if b > a]
        metrics[topic] = {
            "count": len(values),
            "hz": (1.0 / statistics.median(intervals)) if intervals else 0.0,
            "header_lag_ms": (
                1000.0 * statistics.median(header_lag[topic])
                if header_lag[topic] else None
            ),
        }

    def nearest_ms(source, target):
        if not source or not target:
            return None
        stride = max(1, len(source) // 10000)
        offsets = []
        for value in source[::stride]:
            index = bisect.bisect_left(target, value)
            candidates = []
            if index < len(target):
                candidates.append(abs(target[index] - value))
            if index:
                candidates.append(abs(target[index - 1] - value))
            offsets.append(min(candidates))
        return 1000.0 * statistics.median(offsets)

    metrics["alignment"] = {
        "arm_to_hand_ms": nearest_ms(
            times["/kuavo_arm_traj"], times["/control_robot_hand_position"]
        ),
        "head_to_hand_ms": nearest_ms(
            times["/robot_head_motion_data"], times["/control_robot_hand_position"]
        ),
    }
    return metrics


def compare_timing(candidate, reference):
    errors = []
    # Arm and hand are 100 Hz control-loop outputs in both modes. Quest3 head
    # samples in the reference bags range roughly 188-292 Hz, while WebXR is
    # limited by the headset/browser frame rate, so its rate is not compared
    # numerically to the controller transport.
    for topic in ("/kuavo_arm_traj", "/control_robot_hand_position"):
        candidate_hz = candidate[topic]["hz"]
        reference_hz = reference[topic]["hz"]
        if reference_hz > 1.0:
            relative_error = abs(candidate_hz - reference_hz) / reference_hz
            if relative_error > 0.35:
                errors.append(
                    "{}: median rate {:.1f} Hz differs from reference {:.1f} Hz".format(
                        topic, candidate_hz, reference_hz
                    )
                )
    if candidate["/robot_head_motion_data"]["hz"] < 20.0:
        errors.append("/robot_head_motion_data: median rate is below 20 Hz")
    arm_count = candidate["/kuavo_arm_traj"]["count"]
    hand_count = candidate["/control_robot_hand_position"]["count"]
    if abs(arm_count - hand_count) > 1:
        errors.append(
            "arm/hand message counts differ: {} vs {}".format(arm_count, hand_count)
        )
    for name in ("arm_to_hand_ms", "head_to_hand_ms"):
        candidate_ms = candidate["alignment"][name]
        reference_ms = reference["alignment"][name]
        if candidate_ms is not None and reference_ms is not None:
            if candidate_ms > max(20.0, reference_ms + 15.0):
                errors.append(
                    "{}: median offset {:.1f} ms exceeds reference {:.1f} ms".format(
                        name, candidate_ms, reference_ms
                    )
                )
    return errors


def print_timing(label, metrics):
    print("{} timing:".format(label))
    for topic in ("/kuavo_arm_traj", "/control_robot_hand_position",
                  "/robot_head_motion_data"):
        item = metrics[topic]
        lag = item["header_lag_ms"]
        lag_text = "n/a" if lag is None else "{:.2f} ms".format(lag)
        print("  {}: {:.1f} Hz, {} messages, header lag {}".format(
            topic, item["hz"], item["count"], lag_text
        ))
    print("  median nearest offsets: arm-hand={}, head-hand={}".format(
        "n/a" if metrics["alignment"]["arm_to_hand_ms"] is None else
        "{:.2f} ms".format(metrics["alignment"]["arm_to_hand_ms"]),
        "n/a" if metrics["alignment"]["head_to_hand_ms"] is None else
        "{:.2f} ms".format(metrics["alignment"]["head_to_hand_ms"]),
    ))


def bag_contract(path, expected_types, allowed_missing=()):
    errors = []
    allowed_missing = set(allowed_missing)
    with rosbag.Bag(path, "r") as bag:
        topics = bag.get_type_and_topic_info().topics
        for topic, expected_type in expected_types.items():
            info = topics.get(topic)
            if info is None:
                if topic not in allowed_missing:
                    errors.append("{}: missing".format(topic))
                continue
            if info.msg_type != expected_type:
                errors.append("{}: type {} != {}".format(
                    topic, info.msg_type, expected_type
                ))
                continue
            message_class = roslib.message.get_message_class(expected_type)
            connections = list(bag._get_connections(topics=[topic]))
            bag_md5s = {connection.md5sum for connection in connections}
            canonical_md5 = CONTROL_MD5.get(topic)
            if canonical_md5 is not None and bag_md5s != {canonical_md5}:
                errors.append("{}: message MD5 differs from the reference contract".format(topic))
                continue
            if (canonical_md5 is None and message_class is not None and
                    bag_md5s != {message_class._md5sum}):
                errors.append("{}: message MD5 does not match the sourced workspace".format(topic))
                continue
            if topic in CONTROL_TOPICS:
                payload_error = validate_payload(topic, first_message(bag, topic))
                if payload_error:
                    errors.append("{}: {}".format(topic, payload_error))
        observed = {
            topic: (
                info.msg_type,
                tuple(sorted({connection.md5sum for connection in
                              bag._get_connections(topics=[topic])})),
                info.message_count,
            )
            for topic, info in topics.items() if topic in expected_types
        }
    return observed, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", help="WebXR-recorded .bag")
    parser.add_argument("--reference", help="Quest3-controller reference .bag")
    parser.add_argument(
        "--profile", choices=sorted(RECORDING_PROFILES), default="sim-control",
        help="topic contract to validate (default: sim-control)",
    )
    args = parser.parse_args()

    expected_types = profile_topics(args.profile)
    optional_topics = profile_optional_topics(args.profile)
    candidate, errors = bag_contract(
        args.candidate, expected_types, allowed_missing=optional_topics
    )
    absent_optional = [
        topic for topic in expected_types
        if topic in optional_topics and topic not in candidate
    ]
    if absent_optional:
        print(
            "candidate simulation topics without recorded messages (allowed): {}".format(
                len(absent_optional)
            )
        )
        for topic in absent_optional:
            print("  {}".format(topic))
    candidate_timing = timing_contract(args.candidate)
    print_timing("candidate", candidate_timing)
    if args.reference:
        # A real Quest3 reference is always checked strictly, even when the
        # candidate uses the simulation profile.
        reference, reference_errors = bag_contract(args.reference, expected_types)
        reference_timing = timing_contract(args.reference)
        print_timing("reference", reference_timing)
        errors.extend("reference: {}".format(error) for error in reference_errors)
        for topic in expected_types:
            if topic in reference and topic in candidate:
                if reference[topic][:2] != candidate[topic][:2]:
                    errors.append(
                        "{}: candidate/reference ROS type or MD5 differs".format(topic)
                    )
        errors.extend(compare_timing(candidate_timing, reference_timing))

    if errors:
        print("Rosbag alignment: FAILED")
        for error in errors:
            print("  - {}".format(error))
        return 1
    print("Rosbag alignment: OK (schema and control-topic timing are compatible)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
