# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Wave - dwave right hand"""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)

NAME    = "wave"
COMPONENT_NAME = "wave_action"

class DanceJig(IrishAction):
    """Within the IrishAgent, wave right hand"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Jig", "zh": "Irish jig"}),
            "res/irishjig.png",
            False,
            self.on_component_click
        )

    # Called on component click
    def execute(self):
        self.logger.info( f"Executing action {self.name}")