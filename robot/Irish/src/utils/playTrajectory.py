# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
#  -- AI generated

"""
Utility to convert Easy Teach JSON trajectory files into Booster SDK TrajectoryData objects.

Easy Teach JSON format:
    Array of frames, each with:
    - "a": array of joint position values (integers, in millidegrees)
    - "ts": timestamp in milliseconds

Output: List of TrajectoryData objects suitable for robot.execute_trajectory()
"""

import json
import logging
import time
from typing import List
from boosteros.robots.booster import BoosterRobot
from boosteros.types import JointCommand,TrajectoryData,JointTrajectoryPoint
from boosteros.types import time as nanoTime

# Conversion factor: Easy Teach stores joint positions in millidegrees (0.001 degrees)
# Booster SDK expects positions in radians
MILLIDEGREES_TO_RADIANS = 0.001 * 3.141592653589793 / 180.0

# JSON is the result of an EasyTeach session
def playTrajectory(robot:BoosterRobot,trajectory:TrajectoryData,logger):
    """
    Iterate through trajectopry frames, moving robot extremeties accordingly

    Args:
        trajectory: TrajectoryData

    Raises:
        ValueError: If the JSON string is malformed or has inconsistent frame lengths.
    """
    joint_names = [joint.name for joint in robot.list_joints()]
    upper_names = joint_names[:10]

    current_state = robot.get_joint_states()
    state_map = {js.name: js.position for js in current_state.joints}
    upper_body_enabled = False 
    # TODO: Replace these example gains with firmware-provided recommended
    # Booster K1/T1 gain tables once the lower-level control team publishes
    # validated per-joint kp/kd values.
    kp_upper = [40.0, 40.0, 20.0, 30.0, 10.0, 10.0, 20.0, 30.0, 10.0, 10.0]
    kd_upper = [2.0, 2.0, 1.5, 2.0, 0.5, 0.5, 1.5, 2.0, 0.5, 0.5]

    logger.info(f"Playing trajectory ....")
    try:
        # point is a JointTrajectoryPoint
        # ts is time-from-start in milliseconds
        
        priorTime = nanoTime.Duration(0)
        for point in trajectory.points:
            # startTime = point.time_from_Start
            commandList: dict[str, JointCommand] = {}
            for i, name in enumerate(point.joint_names):
                joint = point.get_joint(name)
                if joint is not None and joint.position is not None:
                    commandList[name] = JointCommand(
                        name=name, position=joint.position, kp=kp_upper[i], kd=kd_upper[i]
                    )

            upper_body_enabled = True
            robot.upper_body_control(upper_body_enabled)
            jointTime = point.time_from_start
            delay = jointTime.seconds - priorTime.seconds
            logger.info(f"Trajectory delay = {delay:.1f} secs")
            time.sleep(delay) # ms
            priorTime = jointTime

            robot.set_joints(list(commandList.values()))

    except KeyboardInterrupt:
        logger.info("\nAction playback interrupted by keystroke")
    except Exception as e:
        logger.error(f"Exception during action playback: {e}")
    finally:
        if upper_body_enabled:
            logger.info("Disabling upper body ...")
            try:
                robot.upper_body_control(False)  # No longer controlling
            except Exception as e:
                logger.error(f"Exception setting upper body control off: {e}")

        logger.info("Action complete")

