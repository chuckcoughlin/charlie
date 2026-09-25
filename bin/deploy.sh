#!/bin/sh
# Deploy our customizations to the robot. These actions are in addition to Booster Studio.
#
DATA=${CHARLIE_HOME}/robot/Irish/data
STORAGE_MANAGER=/opt/booster/booster_agent_data/data/agent_storage/chuckcoughlin.charlie
cd $DATA
# Make directories
ssh ${BOOSTER}
  mkdir -p ${STORAGE_MANAGER}/cache/audio
  mkdir -p ${STORAGE_MANAGER}/data
  exit

for fil in *; do
    if [ -f $fil ]; then
        echo "Installing $fil"
        rsync $fil ${BOOSTER}:${STORAGE_MANAGER}/data/$fil
    fi
done

