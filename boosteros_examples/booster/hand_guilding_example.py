"""Example usage of Booster hand guiding and trajectory replay.

This module demonstrates recording a hand-guided trajectory and replaying
a saved trajectory file using the Booster robot API.
"""

from boosteros.robots.booster import BoosterRobot
from boosteros.types import TrajectoryData


def _print_trajectory_info(trajectory: TrajectoryData) -> None:
    frame_count = len(trajectory.points)
    joint_count = len(trajectory.points[0].joints) if frame_count > 0 else 0
    print(
        f"轨迹元信息: id={trajectory.meta.id}, "
        f"model={trajectory.meta.model}, "
        f"sample_interval={trajectory.meta.sample_interval:.6f}s, "
        f"duration={trajectory.meta.duration:.3f}s"
    )
    print(
        f"轨迹数据: frames={frame_count}, joints={joint_count}, "
        f"duration={trajectory.duration.seconds:.3f}s"
    )


def _save_trajectory_if_requested(trajectory: TrajectoryData) -> None:
    save_path = input("请输入轨迹保存路径（.btraj，直接回车则不保存）: ").strip()
    if not save_path:
        print("未保存轨迹文件")
        return
    trajectory.save(save_path)
    print(f"轨迹已保存: {save_path}")


def _replay_trajectory(robot: BoosterRobot, trajectory: TrajectoryData) -> None:
    input("按回车开始回放轨迹...\n")
    print(
        f"回放轨迹: {trajectory.meta.id}, 预计回放时长: {trajectory.meta.duration:.3f}s"
    )
    handle = robot.execute_trajectory(trajectory)

    input("按回车停止回放...\n")
    cancelled = handle.cancel()
    print(f"停止请求已发送: {cancelled}")
    status = handle.wait(timeout=5.0)
    if handle.done():
        print(f"轨迹回放任务结束: {status}")
    else:
        print(f"等待回放停止超时，当前状态: {status}")


def hand_guiding_example():
    """Record a hand-guided trajectory with a Booster robot and replay it."""
    try:
        robot = BoosterRobot()
        robot.set_mode("walk")
        trajectory = None
        with robot.hand_guiding_manager:
            input("按回车开始录制...\n")
            robot.hand_guiding_manager.start_recording()
            input("示教录制中，手动引导机器人运动；按回车结束录制...\n")
            trajectory = robot.hand_guiding_manager.stop_recording()

        if trajectory is None:
            print("未生成有效轨迹，跳过回放")
            return

        _print_trajectory_info(trajectory)
        _save_trajectory_if_requested(trajectory)
        _replay_trajectory(robot, trajectory)
    except Exception as e:
        print(f"示教模式示例运行出错: {e}")


def replay_example():
    """Replay a saved hand-guided trajectory file on the K1 robot."""
    try:
        robot = BoosterRobot()
        robot.set_mode("walk")
        trajectory_path = input("请输入要回放的轨迹文件路径: ").strip()
        if not trajectory_path:
            print("未输入有效路径，退出示例")
            return
        print(f"读取轨迹文件: {trajectory_path}")
        trajectory = TrajectoryData.load(trajectory_path)
        _print_trajectory_info(trajectory)
        _replay_trajectory(robot, trajectory)
    except Exception as e:
        print(f"示教模式示例运行出错: {e}")


def main():
    """Interactive entry point for hand guiding examples."""
    actions = {
        "1": ("录制示教轨迹并回放", hand_guiding_example),
        "2": ("回放已有轨迹文件", replay_example),
    }

    print("\n请选择要执行的功能:")
    for key, (title, _) in actions.items():
        print(f"  {key}. {title}")
    print("  q. 退出")

    choice = input("请输入选项: ").strip().lower()
    if choice in {"q", "quit", "exit"}:
        print("已退出")
        return

    action = actions.get(choice)
    if action is None:
        print("无效选项，退出")
        return

    _, handler = action
    handler()


if __name__ == "__main__":
    main()
