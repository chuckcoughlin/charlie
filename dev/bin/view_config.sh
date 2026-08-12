#!/bin/sh
# Print configuration parameters as read directly from the robot
#
echo "===== Installed packages ====="
pip list

export PYTHON_ROOT=$(CHARLIE_HOME)/src/charlie
cd $PYTHON_ROOT
python3 tools/inspect.py
