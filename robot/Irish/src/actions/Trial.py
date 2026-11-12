# Copyright 2026. Charles Coughlin. All Rights Reserved.
#     MIT License.

"""Trial - experiment with various interfaces"""
import math
import time
from .IrishAction import IrishAction
from ..utils.initializeJoints import initializeJoints
from booster_agent_framework import (
    DefaultStateIconComponent,
    LocaleString
)
from boosteros.robots.booster import BoosterRobot
from boosteros.types import JointCommand,JointInfo,JointState

NAME    = "trial"
COMPONENT_NAME = "trial_action"
kp_upper = [40.0, 40.0, 20.0, 30.0, 10.0, 10.0, 20.0, 30.0, 10.0, 10.0]
kd_upper = [2.0, 2.0, 1.5, 2.0, 0.5, 0.5, 1.5, 2.0, 0.5, 0.5]

class Trial(IrishAction):
    """Within the Irish agent, experiment with code"""

    def __init__(self, agent,robot):
        super().__init__(NAME, agent,robot)
        self.component = DefaultStateIconComponent(
            COMPONENT_NAME,
            LocaleString({"en": "Trial", "zh": "Trial Code"}),
            "res/menworking.png",
            False,
            self.on_component_click
        )

   
    # Called on component click
    def execute(self):
        self.logger.info(f"Executing action {self.name}")

        self.dump_joint_info()

        self.write_elbow_position()
        self.read_elbow_position()
        self.logger.info(f"{self.name} action completed")

    def dump_joint_info(self):
        info_list: list[JointInfo] = self.robot.list_joints()
        for info in info_list:
            if info is not None:
                torque   =  info.max_torque if info.max_torque is not None else 0.0
                velocity = info.max_velocity if info.max_velocity is not None else 0.0
                self.logger.info( f"{info.name}: {info.limits.min:.2f} to {info.limits.max:.2f} {velocity:.2f},{torque:.2f}" )

    def read_elbow_position(self):
        self.logger.info(f"{self.name} read_elbow_position")
        states: list[JointState] = self.robot.get_joint_states()
        for state in states:
            if "Elbow" in state.name:
                self.logger.info(f"{state.name} at {state.position:.2f} {state.effort:.2f}, {state.velocity:.2f}")

    # All upper body joints must be set.
    # Move right elbow
    # Note: Simple .... JointCommand(name="Head_Pitch",position=0.5)
    #       Advanced ... JointCommand(
    #                       name="leg_joint_1",
    #                       position=0.5,
    #                       velocity=0.0,
    #                       effort=2.1,   # feed-forward effort
    #                       kp=100.0,     # stiffness
    #                       kd=5.0,       # damping
    #          )

    # Note: Joint names differ between actual robot and simulation
    def write_elbow_position(self):
        self.logger.info(f"{self.name} write_elbow_position")
        joint_names = [joint.name for joint in self.robot.list_joints()]
        upper_names = joint_names[:10]

        try:
            self.robot.set_mode("prepare")
            time.sleep(2.0)

            commands:list[JointCommand] = []
            cmd = JointCommand( name=upper_names[0], position= 0.0, kp=kp_upper[0],kd=kd_upper[0])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[1], position= 0.01, kp=kp_upper[1],kd=kd_upper[1])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[2], position= 0.04, kp=kp_upper[2],kd=kd_upper[2])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[3], position=-1.18, kp=kp_upper[3],kd=kd_upper[3])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[4], position= -.04, kp=kp_upper[4],kd=kd_upper[4])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[5], position= -0.19, kp=kp_upper[5],kd=kd_upper[5])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[6], position= -0.04, kp=kp_upper[6],kd=kd_upper[6])
            commands.append(cmd)
            cmd = JointCommand( name=upper_names[7], position= 1.32, kp=kp_upper[7],kd=kd_upper[7])
            commands.append(cmd)
            velocity = 15.
            pitch = math.pi*0.5
            cmd = JointCommand( name=upper_names[8], position=pitch, velocity = velocity, kp=kp_upper[8],kd=kd_upper[8])  # -0.07
            commands.append(cmd)
            yaw = math.pi*0.25
            cmd = JointCommand( name=upper_names[9], position=yaw,  velocity = velocity, kp=kp_upper[9],kd=kd_upper[9])     # 0.15
            commands.append(cmd)
        
            self.robot.set_mode("walk")
            self.robot.set_joints(commands)
            self.logger.info(f"Set right elbow to {pitch:.2f} {yaw:.2f}")
            time.sleep(2.0)
        finally:
            self.robot.set_mode("prepare")