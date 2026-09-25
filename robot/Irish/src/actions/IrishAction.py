# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
import json
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
        self.trajectory = []
        self.worker: threading.Thread | None = None
        self.stop_requested = threading.Event()

    @abstractmethod
    def execute(self):
        # Must be implemented in every subclass
        pass

    def load_trajectory(self,file_string):
        """Load an Easy Teach trajectory from the supplied path."""
        path = Path("data/"+file_string)
        try:
            self.logger.info(f"Root directory = {self.agent.storage_manager.node_config_path}") 
            self.logger.info(f"Loading {self.name} trajectory at {path}")
            content = self.agent.storage_manager.read_text_file(path)
            self.trajectory = json.loads(content)
            self.logger.info(f"Loaded {self.name} trajectory: {len(self.trajectory)} frames")
        except Exception as e:
            self.logger.error(f"Failed to load {self.name} trajectory: {e}")
            self.trajectory = []
    
    def on_component_click(self, component: Component) -> LocaleString | None:
        """Handle click event by starting or stopping the associated action."""

        # Read the icon state to decide whether to start or stop the action.
        state_icon = cast(DefaultStateIconComponent, component)

        self.logger.info(
            f"Component clicked: {component.id}, "
            + f"action: {self.name}, running = {state_icon.state}"
        )

        if state_icon.state:
            # Already running — stop it
            if self.worker is not None and self.worker.is_alive():
                self.stop_requested.set()
                self.worker.join(timeout=2.0)
                self.worker = None
                self.stop_requested.clear()
        else:
            # Not running — start it on a background thread
            state_icon.state = True
            self.agent.component_manager.update_component(state_icon)
            
            # Run in a worker thread   
            def _run():
                try:
                    self.stop_requested.clear()
                    self.execute()
                except Exception as e:
                    self.logger.warn(f"Exception executing {self.name}: "
                        + f"{e.__class__.__name__}: {e}")
                finally:
                    state_icon.state = False
                    self.agent.component_manager.update_component(state_icon)
                    self.worker = None
                    self.stop_requested.clear()

            self._worker = threading.Thread(target=_run, daemon=True)
            self.logger.warn("STARTING WORKER")
            self._worker.start()
            return None

        # Reset UI state when action finishes
        state_icon.state = False
        self.agent.component_manager.update_component(state_icon)
        return None

    def playback_trajectory(self):
        if not self.trajectory:
            self.logger.error(f"No trajectory data available for {self.name} action")
            return

        # Play back the recorded joint positions
        prev_ts = None
        for frame in self.trajectory:
            # Check for stop
            if self.stop_requested.is_set():
                self.logger.info(f"{self.name} trajectory stopped")
                return

            joint_positions = frame["a"]
            ts = frame["ts"]  # milliseconds

            # Send joint positions to the robot
            try:
                self.logger.error(f"Joint Positions: {joint_positions}")
                self.agent.robot.set_joints(joint_positions)
            except Exception as e:
                self.logger.error(f"Failed to set joint positions: {e}")

            # Wait for the appropriate interval
            if prev_ts is not None:
                interval = (ts - prev_ts) / 1000.0  # convert ms to seconds
                if interval > 0:
                    self.wait(interval)
            prev_ts = ts

        self.logger.info(f"{self.name} trajectory completed")

    # Speak the supplied text. Files are written to "cache/audio"
    def utter(self,text,file_string):
        smgr = self.agent.storage_manager
        root = smgr.node_config_path
        self.logger.info(f"Root directory = {root}")
        self.logger.info( f"Utter {text}")
        path = Path(file_string)
        if not smgr.file_exists(path):
            self.logger.info( f"Utter : generationg ...")
            speech = gTTS(text=text,lang="en",slow=False)
            self.logger.info( f"Utter : saving ...")
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
        if self.stop_requested.wait(timeout=duration):
            self.logger.info(f"Wait interrupted by stop request")
