"""Example that plays an action together with background audio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from boosteros.robots.booster import BoosterRobot
from boosteros.types import TaskHandle


def _print_actions(robot: BoosterRobot) -> None:
    actions = robot.list_actions()
    print("\n当前支持的动作:")
    for idx, action in enumerate(actions):
        duration = "unknown" if action.duration < 0 else f"{action.duration:.2f}s"
        print(
            f"[{idx:2d}] {action.id:24s} | type={action.type:12s} | duration={duration}"
        )


def _resolve_action_id(robot: BoosterRobot, user_input: str) -> str | None:
    action_infos = robot.list_actions()
    target = user_input.strip()
    if not target:
        return None

    if target.isdigit():
        index = int(target)
        if 0 <= index < len(action_infos):
            return action_infos[index].id
        return None

    return next((action.id for action in action_infos if action.id == target), None)


def _wait_task(handle: TaskHandle[Any], *, title: str) -> None:
    status = handle.wait()
    print(f"{title}已结束，最终状态: {status}")


def _cancel_if_running(handle: TaskHandle[Any] | None, *, title: str) -> None:
    if handle is None or handle.done():
        return
    try:
        if handle.cancel():
            print(f"已请求停止{title}，等待任务结束...")
            handle.wait()
    except Exception as exc:
        print(f"停止{title}失败: {type(exc).__name__}: {exc}")


def play_action_with_bgm(
    action_id: str,
    audio_path: str,
) -> None:
    """Start action and audio playback together, then stop the action after audio."""
    action_handle: TaskHandle[Any] | None = None
    audio_handle: TaskHandle[Any] | None = None

    robot = BoosterRobot()
    try:
        action_handle = robot.do_action(action_id)
        print(
            f"已启动动作: {action_id}, "
            f"trace_id={action_handle.trace_id}, status={action_handle.status}"
        )

        audio_handle = robot.play_sound(audio_path)
        print(
            f"已启动声音: {audio_path}, "
            f"trace_id={audio_handle.trace_id}, status={audio_handle.status}"
        )

        _wait_task(audio_handle, title="声音")
        _cancel_if_running(action_handle, title="动作")
        print("声音已结束，动作已停止")
    finally:
        _cancel_if_running(action_handle, title="动作")
        _cancel_if_running(audio_handle, title="声音")


def main() -> None:
    """Interactive entry point for playing an action with background audio."""
    try:
        robot = BoosterRobot()
        print("机器人连接就绪")
    except Exception as exc:
        print(f"无法初始化机器人客户端: {type(exc).__name__}: {exc}")
        return

    _print_actions(robot)

    action_input = input("\n请输入动作 ID 或列表索引: ").strip()
    action_id = _resolve_action_id(robot, action_input)
    if action_id is None:
        print(f"未找到动作: {action_input}")
        return

    audio_path = input("请输入声音文件路径: ").strip()
    if not audio_path:
        print("未提供声音文件路径，退出。")
        return

    audio_file = Path(audio_path).expanduser()
    if not audio_file.exists():
        print(f"声音文件不存在: {audio_file}")
        return
    if not audio_file.is_file():
        print(f"声音路径不是文件: {audio_file}")
        return

    action_handle: TaskHandle[Any] | None = None
    audio_handle: TaskHandle[Any] | None = None

    try:
        action_handle = robot.do_action(action_id)
        audio_handle = robot.play_sound(str(audio_file))

        print(
            f"\n已同时启动:\n  动作: {action_id} ({action_handle.trace_id})"
            f"\n  声音: {audio_file} ({audio_handle.trace_id})"
        )

        _wait_task(audio_handle, title="声音")
        input("按任意键停止动作...")
        _cancel_if_running(action_handle, title="动作")
        print("示例完成")
    except KeyboardInterrupt:
        print("\n检测到用户中断")
    except Exception as exc:
        print(f"执行失败: {type(exc).__name__}: {exc}")
    finally:
        _cancel_if_running(action_handle, title="动作")
        _cancel_if_running(audio_handle, title="声音")


if __name__ == "__main__":
    main()
