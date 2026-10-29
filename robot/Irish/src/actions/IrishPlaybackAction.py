# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Reconstruct upper body motions recorded by Easy Teach"""
from .IrishAction import IrishAction
from ..utils.jsonToTrajectory import jsonToTrajectory
from ..utils.playTrajectory import playTrajectory
from abc import abstractmethod
from pathlib import Path
import traceback
from boosteros.types import TrajectoryData

class IrishPlaybackAction(IrishAction):
    """Abstract class for actions with the Irish agent that play back recorded movements"""
    def __init__(self, name, agent, robot):
        super().__init__(name,agent,robot)
        self.trajectory : TrajectoryData|None = None

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
            self.logger.info(f"Content = {content}")

            self.trajectory = jsonToTrajectory(self.robot,content,self.logger)
            self.logger.info(f"Loaded {self.name} trajectory: {type(self.trajectory)}, {len(self.trajectory.points)} frames")

        except Exception as e:
            self.logger.error(f"Failed to load {self.name} trajectory: {e}. Make sure trajectory data in storage")
            error_string = traceback.format_exc()
            self.logger.error(error_string)
            self.trajectory = None
    

    def playback_trajectory(self):
        if self.trajectory is None:
            self.logger.error(f"No trajectory data available for {self.name} action")
            return

        try:
            playTrajectory(self.robot,self.trajectory,self.logger)
            self.logger.info(f"{self.name} trajectory completed")
        except Exception as e:
            self.logger.error(f"Failed to play {self.name} trajectory: {e}. ")
            error_string = traceback.format_exc()
            self.logger.error(error_string)
   