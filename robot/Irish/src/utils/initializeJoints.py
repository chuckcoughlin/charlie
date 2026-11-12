# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
#  -- AI generated

"""
Before setting trajectory, set joints to their current position.
Sets "walk" mode
"""

import json
import logging
import time
from typing import List
from boosteros.robots.booster import BoosterRobot
from boosteros.types import JointCommand,TrajectoryData,JointTrajectoryPoint
from boosteros.types import time as nanoTime

def initializeJoints(robot:BoosterRobot,logger):

    upper_body_enabled = False 

    logger.info(f"Initializing joint positions....")

    robot.set_mode("walk")
    joint_names = [joint.name for joint in robot.list_joints()]
    upper_names = joint_names[:10]
    kp_upper = [40.0, 40.0, 20.0, 30.0, 10.0, 10.0, 20.0, 30.0, 10.0, 10.0]
    kd_upper = [2.0, 2.0, 1.5, 2.0, 0.5, 0.5, 1.5, 2.0, 0.5, 0.5]

    current_state = robot.get_joint_states()
    state_map = {js.name: js.position for js in current_state.joints}


    commands =  {}
    for i, name in enumerate(upper_names):
        pos = state_map.get(name)
        if pos is None:
            pos=0.0
        commands[name] = JointCommand(
                name=name, position=pos,kp=kp_upper[i], kd=kd_upper[i] )

    upper_body_enabled = True
    robot.upper_body_control(upper_body_enabled)
    time.sleep(5)
    robot.set_joints(list(commands.values()))
    logger.info("Initialization complete")

