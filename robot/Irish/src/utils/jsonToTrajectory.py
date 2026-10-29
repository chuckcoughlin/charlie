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
from typing import List
from boosteros.robots.booster import BoosterRobot
from boosteros.types import TrajectoryData, TrajectoryMeta, JointTrajectoryPoint, JointState
from boosteros.types import time as nanoTime

# Conversion factor: Easy Teach stores joint positions in millidegrees (0.001 degrees)
# Booster SDK expects positions in radians
MILLIDEGREES_TO_RADIANS = 0.001 * 3.141592653589793 / 180.0


def millidegrees_to_radians(value: int) -> float:
    """Convert a joint position from millidegrees to radians."""
    return value * MILLIDEGREES_TO_RADIANS

# JSON is the result of an EasyTeach session
def jsonToTrajectory(robot:BoosterRobot,json_string: str,logger) -> TrajectoryData:
    """
    Convert an Easy Teach JSON string into a list of TrajectoryData objects.

    Args:
        json_string: JSON string containing the Easy Teach trajectory data.

    Returns:
        A list containing a single TrajectoryData object representing the full trajectory.

    Raises:
        ValueError: If the JSON string is malformed or has inconsistent frame lengths.
    """
    joint_names = [joint.name for joint in robot.list_joints()]
    upper_names = joint_names[:10]
    frames = json.loads(json_string)

    if not frames:
        raise ValueError("Easy Teach JSON contains no frames")

    # Validate frame structure
    num_joints = len(upper_names)
    for i, frame in enumerate(frames):
        if "a" not in frame or "ts" not in frame:
            raise ValueError(f"Frame {i} missing required fields 'a' and 'ts'")
        if len(frame["a"]) != num_joints:
            raise ValueError(
                f"Frame {i} has {len(frame['a'])} joint values, expected {num_joints}"
            )

    # Build trajectory points
    trajectory_points: List[JointTrajectoryPoint] = []
    duration = nanoTime.Duration(0)
    for frame in frames:
        ts = int(frame["ts"]) # ms -> seconds
        positions = [millidegrees_to_radians(v) for v in frame["a"]]
        joints : list[JointState] = [] 
        for i,position in enumerate(positions):
            js = JointState(
                name = upper_names[i],
                position = position
            )
            joints.append(js)


        timeFromStart = nanoTime.Duration(ts*1000000)
        duration = timeFromStart
        point = JointTrajectoryPoint(
            time_from_start=timeFromStart,
            joints = joints,
        )
        trajectory_points.append(point)

    
    # Create TrajectoryMreta 
    tmeta = TrajectoryMeta(
        manufacturer = robot.robot_info.manufacturer,
        model = robot.robot_info.model,
        boosteros_version = robot.robot_info.firmware_version,
        id = robot.robot_info.serial_number,
        sample_interval = 0.0,
        duration = duration.seconds 
    )
    # Create TrajectoryData object with meta and points
    trajectory_data = TrajectoryData(
        meta = tmeta,
        points=trajectory_points
    )
    return trajectory_data
