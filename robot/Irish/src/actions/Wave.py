# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Wave - wave right hand  using trajectory from Easy Teach."""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)

NAME    = "wave"
COMPONENT_NAME = "wave_action"
TRAJECTORY_PATH = "data/wave.json"

class Wave(IrishAction):
    """Within the IrishAgent, wave right hand"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Wave", "zh": "Excited wave"}),
            "res/wave.png",
            False,
            self.on_component_click
        )

    # Called on component click
    def execute(self):
        self.logger.info(f"Executing action {self.name}")
        super().load_trajectory(TRAJECTORY_PATH)
        super().playback_trajectory()
        self.logger.info(f"{self.name} action completed")