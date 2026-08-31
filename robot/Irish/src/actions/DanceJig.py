# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Irish Agent - includes 4 custom actions."""

from typing import cast
from booster_agent_framework import (
    AgentFeatures,
    Component,
    ComponentStatePageProxy,
    DefaultStateIconComponent,
    LocaleString,
)
class DanceJig(IrishAction):
    """Within the IrishAgent, voice a countin"""