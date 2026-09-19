# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Stand - stand at attention using recorded trajectory from Easy Teach."""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)

NAME    = "stand"
COMPONENT_NAME = "stand_action"
TRAJECTORY_PATH = "data/stand.json"

class Stand(IrishAction):
    """Within the IrishAgent, stand at attention"""

    def __init__(self, agent):
        super().__init__(NAME, agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Stand", "zh": "Stand Attention"}),
            "res/stand.png",
            False,
            self.on_component_click
        )

   
    # Called on component click
    def execute(self):
        self.logger.info(f"Executing action {self.name}")
        super().load_trajectory(TRAJECTORY_PATH)
        super().playback_trajectory()
        self.logger.info(f"{self.name} action completed")
