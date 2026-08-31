# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Chain: Execute countin, jog and bow in succession."""

from typing import cast
from booster_agent_framework import (
    AgentFeatures,
    Component,
    ComponentStatePageProxy,
    DefaultStateIconComponent,
    LocaleString,
)
class ChainActions(IrishAction):
    """Within the IrishAgent, execute 3 actions in sequence: Countin, DanceJig and Bow"""