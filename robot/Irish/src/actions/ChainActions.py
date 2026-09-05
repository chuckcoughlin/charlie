# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Chain: Execute countin, jig and bow in succession."""
from chuckcoughlin_charlie.actions.IrishAction import IrishAction
from typing import cast
from booster_agent_framework import (
    AgentFeatures,
    Component,
    ComponentStatePageProxy,
    DefaultStateIconComponent,
    LocaleString,
)
NAME    = "chain"
COMPONENT_NAME = "chain_action"

class ChainActions(IrishAction):
    """Within the IrishAgent, perform a count. jig, bow sequence"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Chain", "zh": "Chain"}),
            "res/chainlink.png",
            False,
            self.on_component_click
        )

    # Called on component click
    def execute(self):
        self.logger.info( f"Executing action {self.name}")

