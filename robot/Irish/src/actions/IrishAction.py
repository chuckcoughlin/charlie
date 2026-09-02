# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

class IrishAction:
    """Base class for actions with the IrishAgent."""
    def __init__(self,robot,logger):
        self.robot = robot
        self.logger= logger