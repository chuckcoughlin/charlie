# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Irish Agent - includes 4 custom actions."""

from typing import cast
from booster_agent_framework import (
    AgentFeatures,
    Component,
    ComponentStatePageProxy,
    DefaultStateIconComponent,
    LocaleString,
)
from chuckcoughlin_charlie.actions.IrishAction import IrishAction

NAME    = "jig"
COMPONENT_NAME = "jg_action"

class DanceJig(IrishAction):
    """Within the IrishAgent, dance a jig"""

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