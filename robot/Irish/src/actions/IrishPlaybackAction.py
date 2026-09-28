# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Reconstruct upper body motions recorded by Easy Teach"""
from .IrishAction import IrishAction
from ..utils.jsonToTrajectory import jsonToTrajectory
from abc import abstractmethod
from pathlib import Path
import traceback
from boosteros.types import TrajectoryData

UPPER_BODY_JOINTS = ["AHead_Yaw","Head_Pitch","ALeft_Shoulder_Pitch","Left_Shoulder_Roll","Left_Elbow_Pitch","Left_Elbow_Yaw","ARight_Shoulder_Pitch","Right_Shoulder_Roll","Right_Elbow_Pitch","Right_Elbow_Yaw"]

class IrishPlaybackAction(IrishAction):
    """Abstract class for actions with the Irish agent that play back recorded movements"""
    def __init__(self, name, agent):
        super().__init__(name,agent)
        self.trajectory = TrajectoryData()

    @abstractmethod
    def execute(self):
        # Must be implemented in every subclass
        pass

    def load_trajectory(self,file_string):
        """Load an Easy Teach trajectory from the supplied path."""
        path = Path("data/"+file_string)
        try:
            self.logger.info(f"Root directory = {self.agent.storage_manager.node_config_path}") 
            content = self.agent.storage_manager.read_text_file(path)
            self.logger.info(f"Loading {self.name} trajectory from {path}")
            self.trajectory = jsonToTrajectory(content)
            self.logger.info(f"Loaded {self.name} trajectory: {len(self.trajectory)} frames")
        except Exception as e:
            self.logger.error(f"Failed to load {self.name} trajectory: {e}. Make sure trajectory data in storage")
            error_string = traceback.format_exc()
            self.logger.error(error_string)
            self.trajectory = []
    

    def playback_trajectory(self):
        
        self.agent.robot.upper_body_control(True) # Only affects upper body

        if not self.trajectory:
            self.logger.error(f"No trajectory data available for {self.name} action")
            return

        self.agent.robot.execute_trajectory(self.trajectory)

        self.logger.info(f"{self.name} trajectory completed")

   