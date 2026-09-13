# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Countin - perform a count down before dancing."""
from .IrishAction import IrishAction
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)

# Storage manager requires that files be relative paths
NAME    = "countin"
BEAT    = 0.75  # seconds
COMPONENT_NAME = "count_action"
ONE = "one"
ONE_PATH = "cache/data/one.mp3"
TWO = "two"
TWO_PATH = "cache/data/two.mp3"
THREE = "three"
THREE_PATH = "cache/data/three.mp3"


class Countin(IrishAction):
    """Within the IrishAgent, perform a count down before dancing"""

    def __init__(self, agent):
        super().__init__(NAME, agent)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Count", "zh": "Count down"}),
            "res/countdown.png",
            False,
            self.on_component_click
        )

    # Called on component click
    def execute(self):
        self.logger.info(f"Executing action {self.name}")
        self.wait(BEAT)
        self.utter(ONE, ONE_PATH)
        self.wait(BEAT)
        self.utter(TWO, TWO_PATH)
        self.wait(BEAT)
        self.utter(THREE, THREE_PATH)
        self.wait(BEAT)
        self.wait(BEAT)
        self.logger.info(f"Completed {self.name}")