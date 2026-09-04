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
ACTION_NAME    = "countin"
COMPONENT_NAME = "count_action"

class Countin(IrishAction):
    """Within the IrishAgent, perform a count down before dancing"""

    def __init__(self,robot,logger):
        super().__init__(robot,logger)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Count", "zh": "Count down"}),
            "res/countdown.png",
            False,
            self.on_component_click
        )

    def on_component_click(self, component: Component) -> LocaleString | None:
        """Handle bow click events by starting or stopping the associated action."""

        # Read the icon state to decide whether to start or stop the action.
        state_icon = cast(DefaultStateIconComponent, component)

        self.logger.info(
            f"Count in component clicked: {component.id}, "
            + f"action: {ACTION_NAME}, state: {state_icon.state}"
        )

        if not state_icon.state:
            try:
                # Start the action when the component is currently inactive.
                #_ = self.robot.do_action(ROBOT_WAVE_ACTION_ID)
                self.logger.info("Start action ...")
            except Exception as e:
                self.logger.warn(
                    f"Action start skipped: component_id={self.component.id}, "
                    + f"action_id={ACTION_NAME}, "
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
                    info.type == "action" and info.task_id == ACTION_NAME
                )
            )
            if active_tasks:
                active_tasks[0].cancel()
            else:
                self.logger.warn(
                    f"No active action task to cancel: component_id={component.id}, "
                    + f"action_id={ACTION_NAME}"
                )

        # Keep the component state in sync with the action state shown in the UI.
        state_icon.state = not state_icon.state
        self.robot.component_manager.update_component(state_icon)

        return None

