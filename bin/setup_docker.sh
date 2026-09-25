#!/bin/sh
# Add data files to the docker image. 
#
DOCKER_ID="f4a4cccdeb90"
DATA=${CHARLIE_HOME}/robot/Irish/data
STORAGE_MANAGER=/opt/booster/booster_agent_data/data/agent_storage/chuckcoughlin.charlie
cd $DATA

docker exec -u root -it ${DOCKER_ID} mkdir -p -m 777 ${STORAGE_MANAGER}/data
for fil in *; do
	if [ -f $fil ]; then
		echo "Installing $fil"
        docker cp $fil ${DOCKER_ID}:${STORAGE_MANAGER}/data/$fil
	fi
done

# Make directory fortemporary audio files
docker exec -u root -it ${DOCKER_ID} mkdir -p -m 777 ${STORAGE_MANAGER}/cache/audio

