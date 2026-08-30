#!/bin/sh
#  List log entries that have been generated within the last hour.
#  Robot must be in PREP mode
#
cd ${CHARLIE_HOME}
cd ~/tmp

rm -rf ~/tmp/*
# Get current time, less an hour, by fudging timezone
DATE=`TZ='US/Pacific' date +"%Y%m%d-%H%M%S"`
#echo $DATE
ssh ${BOOSTER}
rm -r /home/booster/Documents/logs/*
booster-cli log -st $DATE -o /home/booster/Documents/logs
exit
rsync -r ${BOOSTER}:/home/booster/Documents/logs/* .
unzip *.zip
find . -name *.log|xargs cat
