#!/usr/bin/env python3
"""Interactive WebXR rosbag recorder matching the real-robot workflow."""

import argparse
import datetime
import json
import os
import signal
import subprocess
import sys
from pathlib import Path


DEFAULT_OUTPUT_DIR = "/root/kuavo_ws/.docker-runtime/records"
DEFAULT_BAG_PREFIX = "vr_record"


def default_topics_file():
    """Find the bridge-owned topic list in source, devel, or install space."""
    configured = os.environ.get("WEBXR_RECORD_TOPICS_FILE")
    if configured:
        return Path(configured).expanduser()

    # catkin's devel-space wrapper is normally a symlink to this source file.
    source_candidate = Path(__file__).resolve().parent.parent / "config" / "record_topics.json"
    if source_candidate.is_file():
        return source_candidate

    try:
        import rospkg
    except ImportError:
        rospkg = None
    if rospkg is not None:
        try:
            package_root = Path(rospkg.RosPack().get_path("quest_webxr_bridge"))
            package_candidate = package_root / "config" / "record_topics.json"
            if package_candidate.is_file():
                return package_candidate
        except rospkg.ResourceNotFound:
            pass

    return source_candidate


def load_topics(path):
    path = Path(path).expanduser()
    with path.open("r", encoding="utf-8") as stream:
        config = json.load(stream)
    topics = config.get("record_topics")
    if not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
        raise ValueError("record_topics must be a JSON list of topic strings")
    if len(topics) != len(set(topics)):
        raise ValueError("record_topics contains duplicate topic names")
    return topics


def output_path(root, prefix=DEFAULT_BAG_PREFIX, now=None):
    now = now or datetime.datetime.now()
    date_dir = Path(root).expanduser() / now.strftime("%Y-%m-%d")
    filename = "{}_{}.bag".format(prefix, now.strftime("%Y-%m-%d-%H-%M-%S"))
    return date_dir, date_dir / filename


def build_record_command(bag_path, topics):
    command = ["rosbag", "record", "-O", str(bag_path)]
    command.extend(topics if topics else ["-a"])
    return command


def stop_process_cleanly(process, label):
    if process.poll() is not None:
        return process.returncode
    print("\nStopping {} cleanly...".format(label))
    os.killpg(process.pid, signal.SIGINT)
    return process.wait()


def record_rosbag(topics, output_dir, prefix, dry_run=False):
    date_dir, bag_path = output_path(output_dir, prefix)
    command = build_record_command(bag_path, topics)

    print("Topics file selects {} topic(s):".format(len(topics) if topics else "all"))
    for topic in topics:
        print("  {}".format(topic))
    print("Bag output: {}".format(bag_path))
    if dry_run:
        print("Command: {}".format(" ".join(command)))
        return 0

    date_dir.mkdir(parents=True, exist_ok=True)
    try:
        process = subprocess.Popen(command, start_new_session=True)
    except OSError as error:
        print("Failed to start rosbag record: {}".format(error), file=sys.stderr)
        return 1

    print("Recording started. Press Ctrl+C once to stop and save the bag.")
    try:
        return_code = process.wait()
    except KeyboardInterrupt:
        return_code = stop_process_cleanly(process, "rosbag record")

    if return_code != 0:
        print("rosbag record failed with exit code {}".format(return_code), file=sys.stderr)
        return return_code
    print("Bag saved: {}".format(bag_path))
    return 0


def available_bags(output_dir):
    root = Path(output_dir).expanduser()
    if not root.is_dir():
        return []
    return sorted(root.glob("*/*.bag"), key=lambda path: path.stat().st_mtime, reverse=True)


def choose_from_menu(prompt, choices):
    print(prompt)
    for index, choice in enumerate(choices, 1):
        print("  {}) {}".format(index, choice))
    while True:
        try:
            value = input("请输入序号: ").strip()
        except EOFError:
            return None
        try:
            index = int(value)
        except ValueError:
            print("请输入有效序号。")
            continue
        if 1 <= index <= len(choices):
            return index - 1
        print("请输入 1 到 {}。".format(len(choices)))


def playback_rosbag(output_dir):
    bags = available_bags(output_dir)
    if not bags:
        print("No rosbag files found under {}".format(Path(output_dir).expanduser()))
        return 1
    selection = choose_from_menu("请选择一个 rosbag 文件进行回放", [str(path) for path in bags])
    if selection is None:
        return 1
    command = ["rosbag", "play", str(bags[selection])]
    try:
        process = subprocess.Popen(command, start_new_session=True)
    except OSError as error:
        print("Failed to start rosbag play: {}".format(error), file=sys.stderr)
        return 1
    print("Playing: {}".format(bags[selection]))
    try:
        return process.wait()
    except KeyboardInterrupt:
        return stop_process_cleanly(process, "rosbag play")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Record the real-robot-compatible 22-topic WebXR rosbag profile"
    )
    parser.add_argument(
        "--action", choices=("menu", "record", "playback"), default="menu",
        help="default: show the same record/playback menu as the real-robot tool",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("WEBXR_ROSBAG_DIR", DEFAULT_OUTPUT_DIR),
        help="persistent bag root (default: %(default)s)",
    )
    parser.add_argument(
        "--topics-file", default=str(default_topics_file()),
        help="JSON file containing record_topics (default: bridge config)",
    )
    parser.add_argument("--prefix", default=DEFAULT_BAG_PREFIX)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    action = args.action
    if args.dry_run and action == "menu":
        action = "record"
    elif action == "menu":
        selection = choose_from_menu(
            "请选择一个操作",
            ["录制 VR 手臂数据和相机数据 ROSBAG", "回放 VR 手臂数据和相机数据 ROSBAG"],
        )
        if selection is None:
            return 1
        action = ("record", "playback")[selection]

    if action == "playback":
        return playback_rosbag(args.output_dir)

    try:
        topics = load_topics(args.topics_file)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("Failed to load topics from {}: {}".format(args.topics_file, error), file=sys.stderr)
        return 1
    return record_rosbag(topics, args.output_dir, args.prefix, args.dry_run)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled before recording started.")
        sys.exit(130)
