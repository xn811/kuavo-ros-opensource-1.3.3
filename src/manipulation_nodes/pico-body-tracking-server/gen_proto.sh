#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR/protos

protoc --proto_path=/usr/include --proto_path=. --python_out=. --csharp_out=. body_tracking_extended.proto delayed_diagnosis.proto

cp body_tracking_extended_pb2.py delayed_diagnosis_pb2.py $SCRIPT_DIR/scripts/core/ros/