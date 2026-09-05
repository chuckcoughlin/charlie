# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Irish Agent - includes 4 custom actions."""
from chuckcoughlin_charlie.actions.IrishAction import IrishAction
from typing import cast
from booster_agent_framework import (
    AgentFeatures,
    Component,
    ComponentStatePageProxy,
    DefaultStateIconComponent,
    LocaleString,
)
NAME    = "countin"
COMPONENT_NAME = "count_action"

class Countin(IrishAction):
    """Within the IrishAgent, perform a count down before dancing"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Count", "zh": "Count down"}),
            "res/countdown.png",
            False,
            self.on_component_click
        )

        # Called on component click
    def execute(self):
        self.logger.info( f"Executing action {self.name}")

