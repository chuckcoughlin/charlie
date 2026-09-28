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
from boosteros.types import TrajectoryData, JointState, JointTrajectoryPoint

# Joint names in the order they appear in Easy Teach recordings
EASY_TEACH_JOINTS = [
    "Head_Yaw",
    "Head_Pitch",
    "Left_Shoulder_Pitch",
    "Left_Shoulder_Roll",
    "Left_Elbow_Pitch",
    "Left_Elbow_Yaw",
    "Right_Shoulder_Pitch",
    "Right_Shoulder_Roll",
    "Right_Elbow_Pitch",
    "Right_Elbow_Yaw",
]

# Conversion factor: Easy Teach stores joint positions in millidegrees (0.001 degrees)
# Booster SDK expects positions in radians
MILLIDEGREES_TO_RADIANS = 0.001 * 3.141592653589793 / 180.0


def millidegrees_to_radians(value: int) -> float:
    """Convert a joint position from millidegrees to radians."""
    return value * MILLIDEGREES_TO_RADIANS

# JSON is the result of an EasyTeach session
def jsonToTrajectory(json_string: str) -> List[TrajectoryData]:
    """
    Convert an Easy Teach JSON string into a list of TrajectoryData objects.

    Args:
        json_string: JSON string containing the Easy Teach trajectory data.

    Returns:
        A list containing a single TrajectoryData object representing the full trajectory.

    Raises:
        ValueError: If the JSON string is malformed or has inconsistent frame lengths.
    """
    joint_names = EASY_TEACH_JOINTS
    frames = json.loads(json_string)

    if not frames:
        raise ValueError("Easy Teach JSON contains no frames")

    # Validate frame structure
    num_joints = len(joint_names)
    for i, frame in enumerate(frames):
        if "a" not in frame or "ts" not in frame:
            raise ValueError(f"Frame {i} missing required fields 'a' and 'ts'")
        if len(frame["a"]) != num_joints:
            raise ValueError(
                f"Frame {i} has {len(frame['a'])} joint values, expected {num_joints}"
            )

    # Build trajectory points
    start_ts = frames[0]["ts"]

    trajectory_points: List[JointTrajectoryPoint] = []
    for frame in frames:
        time_from_start = (frame["ts"] - start_ts) / 1000.0  # ms -> seconds
        positions = [millidegrees_to_radians(v) for v in frame["a"]]
        joints : list[JointState] = [] 
        for i,position in enumerate(positions):
            js = JointState(
                name = EASY_TEACH_JOINTS[i],
                position = position,
            )
            joints.append(js)
        point = JointTrajectoryPoint(
           time_from_start=time_from_start,
            joints = joints
        )
        trajectory_points.append(point)

    # Calculate total duration
    total_duration = (frames[-1]["ts"] - start_ts) / 1000.0

    # Create TrajectoryData object with meta and points
    trajectory_data = TrajectoryData(
        points=trajectory_points
    )

    return [trajectory_data]