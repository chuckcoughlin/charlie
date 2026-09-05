# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Bow - perform a stage bow."""
from chuckcoughlin_charlie.actions.IrishAction import IrishAction
from typing import cast
from booster_agent_framework import (
    Component,
    DefaultStateIconComponent,
    LocaleString
)

NAME    = "bow"
COMPONENT_NAME = "bow_action"

class Bow(IrishAction):
    """Within the IrishAgent, perform a bow"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Bow", "zh": "Bow"}),
            "res/bow.png",
            False,
            self.on_component_click
        )


    # Called on component click
    def execute(self):
        self.logger.info( f"Executing action {self.name}")