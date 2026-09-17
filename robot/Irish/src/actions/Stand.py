# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Stand - stand at attention."""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)

NAME    = "stand"
COMPONENT_NAME = "stand_action"

class Stand(IrishAction):
    """Within the IrishAgent, stand at attention"""

    def __init__(self,agent):
        super().__init__(NAME,agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Stand", "zh": "Stand Attention"}),
            "res/stand.png",
            False,
            self.on_component_click
        )

    # Called on component click
    def execute(self):
        self.logger.info( f"Executing action {self.name}")