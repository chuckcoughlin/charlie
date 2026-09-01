# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
"""Irish Agent - includes 4 custom actions."""

from typing import cast

from booster_agent_framework import (
    AgentBase,
    AgentFeatures,
    Component,
    ComponentStatePageProxy,
    DefaultStateIconComponent,
    LocaleString,
)
from boosteros.robots.booster import BoosterRobot

import actions.IrishAction
import actions.Bow
import actions.ChainActions
import actions.Countin
import actions.DanceJig

IRISH_PAGE_ID: str = "IrishAgentMode"

#COMPONENT_WAVE_ACTION: str = "wave_action"
#COMPONENT_CUSTOM_ACTION: str = "custom_action"
#ROBOT_WAVE_ACTION_ID: str = "hand_wave"


class IrishAgent(AgentBase):
    """Irish Agent - includes Countin, DanceJig, Bow and Chain actions."""

    def __init__(self):
        super().__init__(AgentFeatures(enable_auto_getup=True))
        self.robot = BoosterRobot()
        self.bow_action   = Bow(self.robot)
        self.chain_action = ChainActions(elf.robot)
        self.count_action = Countin(self.robot)
        self.jig_action   = DanceJig(self.robot)
        self.page_id = IRISH_PAGE_ID
        self.setup_components()

    def on_agent_activated(self):
        self.logger.info("IrishAgent: activated")

    def on_agent_close(self):
        self.logger.info("IrishAgent is closing")

    # Configure conponents to show on the Android app
    def setup_components(self):

        self.page_proxy = ComponentStatePageProxy(self)
        self.page_proxy.register_page(
            self.page_id, lambda *_: self.robot.get_mode() == "walk"
        )

        # ---------------------------------------------------------------------
        # Register the action buttons
        # ---------------------------------------------------------------------

        self.page_proxy.register_component(self.page_id, self.bow_action.component)

        # ---------------------------------------------------------------------
        # Customization section
        # ---------------------------------------------------------------------
        # Instantiate the custom button component. Replace the component ID,
        # label, icon path, and callback with your own feature.
        custom_component = DefaultStateIconComponent(
            COMPONENT_CUSTOM_ACTION,
            LocaleString({"en": "Custom Action", "zh": "自定义动作"}),
            "",
            False,
            self.on_custom_component_click,
        )

        # Register the custom button component on the walk page.
        self.page_proxy.register_component(self,page_id, custom_component)

    def on_custom_component_click(self, component: Component) -> LocaleString | None:
        """Custom button callback."""

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

    def on_wave_action_component_click(
        self, component: Component
    ) -> LocaleString | None:
        """Handle wave component click events by starting or stopping the wave action."""

        # Read the icon state to decide whether to start or stop the action.
        state_icon = cast(DefaultStateIconComponent, component)

        self.logger.info(
            f"Wave component clicked: {component.id}, "
            + f"action: {ROBOT_WAVE_ACTION_ID}, state: {state_icon.state}"
        )

        if not state_icon.state:
            try:
                # Start the action when the component is currently inactive.
                _ = self.robot.do_action(ROBOT_WAVE_ACTION_ID)
            except Exception as e:
                self.logger.warn(
                    f"Action start skipped: component_id={component.id}, "
                    + f"action_id={ROBOT_WAVE_ACTION_ID}, "
                    + f"error={e.__class__.__name__}: {e}"
                )
                return LocaleString(
                    {
                        "en": "Action running, please wait.",
                        "zh": "动作进行中，请稍后再试",
                    }
                )
        else:
            # Cancel the active action task when the component is already active.
            active_tasks = self.robot.get_active_tasks(
                filter=lambda info: (
                    info.type == "action" and info.task_id == ROBOT_WAVE_ACTION_ID
                )
            )
            if active_tasks:
                active_tasks[0].cancel()
            else:
                self.logger.warn(
                    f"No active action task to cancel: component_id={component.id}, "
                    + f"action_id={ROBOT_WAVE_ACTION_ID}"
                )

        # Keep the component state in sync with the action state shown in the UI.
        state_icon.state = not state_icon.state
        self.component_manager.update_component(state_icon)

        return None