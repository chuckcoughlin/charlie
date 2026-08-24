"""Example showing how to move the robot by a specified distance."""

import time
from datetime import datetime

from boosteros.robots.booster import BoosterRobot


def move_by_distance(dist: float, speed: float, step: float = 0.5):
    k1 = BoosterRobot()
    cur_mode = k1.get_mode()
    print("current mode", cur_mode)
    if cur_mode != "walk":
        k1.set_mode("walk")

    k1.reset_odom()
    print("reset odom")
    time.sleep(0.5)

    # 设置速度，x为前进速度，y为横移速度，z为旋转速度，之后机器人会一直以该速度移动，直到收到新的速度指令或进入其他模式
    k1.set_velocity(speed, 0, 0)

    while True:
        odom = k1.get_odom()
        print(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} pose_2d({odom.pose_2d[0]:.3f}, {odom.pose_2d[1]:.3f}, {odom.pose_2d[2]:.3f})"
        )

        if odom.pose_2d[0] > dist:
            k1.set_velocity(0.0, 0.0, 0.0)
            print("到达目标位置，停止运动")
            break

        time.sleep(step)


if __name__ == "__main__":
    move_by_distance(2.0, 0.5, 0.1)
