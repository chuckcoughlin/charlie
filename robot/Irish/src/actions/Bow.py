# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Irish Agent - includes 4 custom actions."""

from typing import cast
from booster_agent_framework import (
    Component,
    DefaultStateIconComponent,
    LocaleString,
)
import IrishAction

COMPONENT_NAME = "bow_action"

class Bow(IrishAction):
    """Within the IrishAgent, perform a bow"""

    def __init__(self,robot):
        super().__init__(self,robot)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Bow", "zh": "Bow"}),
            "res/bow.png",
            False,
            self.on_action_component_click,
        )

    def on_action_component_click(self) -> LocaleString | None:
        """Bow button callback."""
    
        # self.robot is the BoosterRobot instance and can be used directly here.
            # Example: uncomment the following lines to run the wave action on click.
            # self.robot.do_action(ROBOT_WAVE_ACTION_ID)
            # return LocaleString(
            #     {"en": "Wave action started.", "zh": "已开始挥手动作"}
            # )
    
        self.logger.info(f"Custom component clicked: {component.id}")
        return LocaleString(
                {
                    "en": "Custom button clicked. Add your robot logic here.",
                    "zh": "已点击自定义按钮，可在此处添加机器人逻辑",
                }
            )

