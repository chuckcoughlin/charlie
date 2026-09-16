# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
import os
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import cast
from booster_agent_framework import (
    Component,
    DefaultStateIconComponent,
    LocaleString
)
from gtts import gTTS

class IrishAction(ABC):
    """Abstract Base class for actions with the IrishAgent."""
    def __init__(self, name, agent):
        self.name = name
        self.agent = agent
        self.logger = agent.logger
        self._worker: threading.Thread | None = None
        self._stop_event = threading.Event()

    @abstractmethod
    def execute(self):
        # Must be implemented in every subclass
        pass

    def on_component_click(self, component: Component) -> LocaleString | None:
        """Handle click event by starting or stopping the associated action."""

        # Read the icon state to decide whether to start or stop the action.
        state_icon = cast(DefaultStateIconComponent, component)

        self.logger.info(
            f"Component clicked: {component.id}, "
            + f"action: {self.name}, state: {state_icon.state}"
        )

        if not state_icon.state:
            # Already running — stop it
            if self._worker is not None and self._worker.is_alive():
                self._stop_event.set()
                self._worker.join(timeout=2.0)
                self._worker = None
                self._stop_event.clear()
        else:
            # Not running — start it on a background thread
            state_icon.state = True
            self.agent.component_manager.update_component(state_icon)

            self._stop_event.clear()

            def _run():
                try:
                    self.execute()
                except Exception as e:
                    self.logger.warn(
                        f"Exception executing {self.name}: "
                        + f"{e.__class__.__name__}: {e}"
                    )
                finally:
                    # Reset UI state when action finishes
                    state_icon.state = False
                    self.agent.component_manager.update_component(state_icon)
                    self._worker = None

            self._worker = threading.Thread(target=_run, daemon=True)
            self._worker.start()
            return None

        # Toggle state for stop path
        state_icon.state = not state_icon.state
        self.agent.component_manager.update_component(state_icon)

        return None

    # Speak the supplied text. 
    def utter(self,text,path):
        self.logger.info( f"Utter {text}")
        smgr = self.agent.storage_manager
        if not smgr.file_exists(path):
            speech = gTTS(text=text,lang="en",slow=False)
            speech.save(path)
        if smgr.file_exists(path): 
            try: 
                self.agent.robot.play_sound(path).wait()
            except Exception as e:
                self.logger.warn(
                          f"Exception playing: {text} "
                        + f"{e.__class__.__name__}: {e}"
                    )

        else:
           self.logger.info( f"Failed to generate file for: {text}") 
           

    def wait(self, duration):
        """Sleep for the given duration, but return early if the action is stopped."""
        self.logger.info(f"WAIT: {duration} secs")
        # Poll the stop event in small increments so we can abort quickly
        elapsed = 0.0
        interval = 0.05  # 50 ms polling
        while elapsed < duration:
            if self._stop_event.is_set():
                self.logger.info(f"Wait interrupted by stop at {elapsed:.2f}s")
                return
            time.sleep(interval)
            elapsed += interval
