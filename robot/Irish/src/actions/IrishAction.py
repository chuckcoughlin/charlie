# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
from abc import ABC, abstractmethod
from typing import cast
from booster_agent_framework import (
    Component,
    DefaultStateIconComponent,
    LocaleString
)

class IrishAction(ABC):
    """Abstract Base class for actions with the IrishAgent."""
    def __init__(self,name,agent):
        self.name  = name
        self.agent = agent
        self.logger= agent.logger

    def on_component_click(self,component: Component) -> LocaleString | None:
            """Handle click event by starting or stopping the associated action."""
    
            # Read the icon state to decide whether to start or stop the action.
            state_icon = cast(DefaultStateIconComponent, component)
    
            self.logger.info(
                f"Component clicked: {component.id}, "
                + f"action: {self.name}, state: {state_icon.state}"
            )
    
            if not state_icon.state:
                try:
                    # Start the action when the component is currently inactive.
                    #_ = self.robot.do_action(ROBOT_WAVE_ACTION_ID)
                    self.execute()
                except Exception as e:
                    self.logger.warn(
                        f"Action start skipped: component_id={component.id}, "
                        + f"action_id={self.name}, "
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
                active_tasks = self.agent.robot.get_active_tasks(
                    filter=lambda info: (
                        info.type == "action" and info.task_id == self.name
                    )
                )
                if active_tasks:
                    active_tasks[0].cancel()
                else:
                    self.logger.warn(
                        f"No active action task to cancel: component_id={component.id}, "
                        + f"action_id={self.name}"
                    )
    
            # Keep the component state in sync with the action state shown in the UI.
            state_icon.state = not state_icon.state
            self.agent.component_manager.update_component(state_icon)
    
            return None

    @abstractmethod
    def execute(self):
        # Must be implemented in every subclass
        pass