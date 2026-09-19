# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Bow - perform a stage bow  using trajectory from Easy Teach."""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)

NAME    = "bow"
COMPONENT_NAME = "bow_action"
TRAJECTORY_PATH = "data/bow.json"

class Bow(IrishAction):
    """Within the IrishAgent, perform a bow"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Bow", "zh": "Take a Bow"}),
            "res/bow.png",
            False,
            self.on_component_click
        )


    # Called on component click
    def execute(self):
        self.logger.info(f"Executing action {self.name}")
        super().load_trajectory(TRAJECTORY_PATH)
        super().playback_trajectory()
        self.logger.info(f"{self.name} action completed")