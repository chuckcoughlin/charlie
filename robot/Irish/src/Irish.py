# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.
"""Irish Agent - includes 4 custom actions."""

from booster_agent_framework import (
    AgentBase,
    AgentFeatures,
    ComponentStatePageProxy
)
from boosteros.robots.booster import BoosterRobot

from .actions.Bow import Bow
from .actions.ChainActions import ChainActions
from .actions.Countin import Countin
from .actions.DanceJig import DanceJig
from .actions.Stand import Stand
from .actions.Wave import Wave

IRISH_PAGE_ID: str = "IrishAgentMode"

class IrishAgent(AgentBase):
    """Irish Agent - includes Countin, DanceJig, Bow and Chain actions."""

    def __init__(self):
        super().__init__(AgentFeatures(enable_auto_getup=True))
        self.robot = BoosterRobot()
        self.bow_action   = Bow(self)
        self.chain_action = ChainActions(self)
        self.count_action = Countin(self)
        self.jig_action   = DanceJig(self)
        self.stand_action = Stand(self)
        self.wave_action  = Wave(self)
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
        self.page_proxy.register_component(self.page_id, self.chain_action.component)
        self.page_proxy.register_component(self.page_id, self.count_action.component)
        self.page_proxy.register_component(self.page_id, self.jig_action.component)
        self.page_proxy.register_component(self.page_id, self.stand_action.component)
        self.page_proxy.register_component(self.page_id, self.wave_action.component)


