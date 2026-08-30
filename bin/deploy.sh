#!/bin/sh
# Deploy our customizations to the robot. These actions are in addition to Booster Studio.
#
cd ${CHARLIE_HOME}
cd config
# Map controller buttons to action
rsync task_instruction.yaml booster@10.0.0.245:/opt/booster/G``ait/configs/K1/task_instruction.yaml
