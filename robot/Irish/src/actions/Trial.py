# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Trial - experiment with various interfaces"""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)
from boosteros.robots.booster import BoosterRobot
from boosteros.types import JointCommand,TrajectoryData,JointTrajectoryPoint

NAME    = "trial"
COMPONENT_NAME = "trial_action"
kp_upper = [40.0, 40.0, 20.0, 30.0, 10.0, 10.0, 20.0, 30.0, 10.0, 10.0]
kd_upper = [2.0, 2.0, 1.5, 2.0, 0.5, 0.5, 1.5, 2.0, 0.5, 0.5]

class Trial(IrishAction):
    """Within the Irish agent, experiment with code"""

    def __init__(self, agent,robot):
        super().__init__(NAME, agent,robot)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Trial", "zh": "Trial Code"}),
            "res/menworking.png",
            False,
            self.on_component_click
        )

   
    # Called on component click
    def execute(self):
        self.logger.info(f"Executing action {self.name}")
        # Read right elbow position, change it, then read it again
        self.read_elbow_position()
        self.write_elbow_position()
        self.read_elbow_position()
        self.logger.info(f"{self.name} action completed")

    def read_elbow_position(self):
        pass

    def write_elbow_position(self):
        self.robot.upper_body_control(True)
        commandList: dict[str, JointCommand] = {}
        self.robot.upper_body_control(False)