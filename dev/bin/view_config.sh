#!/bin/sh
# Print configuration parameters as read directly from the robot
export PYTHON_ROOT=$(CHARLIE_HOME)/src/charlie
cd $PYTHON_ROOT
python3 robot/inspect.py
