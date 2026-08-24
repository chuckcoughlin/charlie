from __future__ import annotations

import logging
from typing import Any

from boosteros.base.logger import ROOT_LOGGER_NAME
from boosteros.robots.booster import BoosterRobot
from boosteros.types import TaskHandle


def _quiet_logging() -> None:
    """Raise this example process log level to WARNING for cleaner interaction."""
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger(ROOT_LOGGER_NAME).setLevel(logging.WARNING)


def _print_actions(robot: BoosterRobot) -> None:
    actions = robot.list_actions()
    print("\n当前支持的动作:")
    for idx, action in enumerate(actions):
        duration = "unknown" if action.duration < 0 else f"{action.duration:.2f}s"
        print(
            f"[{idx:2d}] {action.id:24s} | type={action.type:12s} "
            f"| interruptible={str(action.interruptible):5s} | duration={duration}"
        )


def _print_handle_status(handle: TaskHandle[Any] | None) -> None:
    if handle is None:
        print("当前没有活动动作任务")
        return

    action_id = getattr(handle, "action_id", "<unknown>")
    print(
        "当前任务:"
        + f" trace_id={handle.trace_id}"
        + f", type={handle.type}"
        + f", action_id={action_id}"
        + f", status={handle.status}"
    )


def _wait_for_task_finish(handle: TaskHandle[Any], *, reason: str) -> None:
    action_id = getattr(handle, "action_id", "<unknown>")
    print(f"{reason}，等待动作 {action_id} 真正结束...")
    status = handle.wait()
    print(f"动作 {action_id} 已结束，最终状态: {status}")


def run_action_control_demo() -> None:
    """Interactive action debugging example.

    Supports listing actions, starting an action, stopping an action, and
    blocking until the stopped action has actually finished.
    """
    _quiet_logging()

    try:
        robot = BoosterRobot()
        print("机器人连接就绪")
    except Exception as exc:
        print(f"无法初始化机器人客户端: {exc}")
        return

    active_handle: TaskHandle[Any] | None = None

    try:
        print("\n" + "=" * 68)
        print(" do_action 交互调试器")
        print(" 支持命令:")
        print("   list                    查看动作列表")
        print("   start [动作ID/索引]      启动动作")
        print("   stop                    停止当前动作，并阻塞到真正结束")
        print("   status                  查看当前任务状态")
        print("   exit                    退出程序")
        print("=" * 68)

        _print_actions(robot)

        while True:
            try:
                line = input("\n[Action] 请输入指令 > ").strip()
                if not line:
                    continue

                parts = line.split()
                command = parts[0].lower()

                if command in {"exit", "quit"}:
                    break

                if command == "list":
                    _print_actions(robot)
                    continue

                if command == "status":
                    if active_handle is not None and active_handle.done():
                        _print_handle_status(active_handle)
                        active_handle = None
                    else:
                        _print_handle_status(active_handle)
                    continue

                if command == "stop":
                    if active_handle is None:
                        print("当前没有可停止的动作")
                        continue

                    if active_handle.done():
                        print(f"动作已结束，最终状态: {active_handle.status}")
                        active_handle = None
                        continue

                    cancelled = active_handle.cancel()
                    if not cancelled:
                        print("当前动作不支持停止或已进入终态")
                        continue

                    _wait_for_task_finish(active_handle, reason="已发送停止请求")
                    active_handle = None
                    continue

                if command == "start":
                    if len(parts) != 2:
                        print("格式错误。用法: start [动作ID/索引]")
                        continue

                    action_infos = robot.list_actions()
                    action_id: str | None = None
                    target = parts[1]
                    if target.isdigit():
                        index = int(target)
                        if 0 <= index < len(action_infos):
                            action_id = action_infos[index].id
                    else:
                        action_id = next(
                            (
                                action.id
                                for action in action_infos
                                if action.id == target
                            ),
                            None,
                        )

                    if action_id is None:
                        print(f"未找到动作: {target}")
                        continue

                    if active_handle is not None and not active_handle.done():
                        print("已有动作在执行中，请先 stop 再启动新动作")
                        continue

                    active_handle = robot.do_action(action_id)
                    print(
                        f"已启动动作: {action_id}, "
                        + f"trace_id={active_handle.trace_id}, "
                        + f"status={active_handle.status}"
                    )
                    continue

                print("未知命令。可用命令: list, start, stop, status, exit")

            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f"操作失败: {exc}")

    except KeyboardInterrupt:
        print("\n检测到用户中断")
    finally:
        if active_handle is not None and not active_handle.done():
            try:
                cancelled = active_handle.cancel()
                if cancelled:
                    _wait_for_task_finish(
                        active_handle, reason="程序退出，自动停止当前动作"
                    )
            except Exception as exc:
                print(f"退出时停止动作失败: {exc}")

        print("示例结束")


if __name__ == "__main__":
    run_action_control_demo()
