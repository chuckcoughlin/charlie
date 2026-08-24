"""Product-style realtime speech chat example."""

from __future__ import annotations

from boosteros import brain
from boosteros.brain.speech import ChatConfig
from boosteros.robots.booster import BoosterRobot


def main() -> None:
    """Start a Booster robot realtime speech chat session."""
    robot = BoosterRobot()
    handle = None
    try:
        speech = brain.Speech(robot)
        handle = speech.chat(
            config=ChatConfig(
                system_prompt="你是一个天气预报助手，可以查询全国各地的天气预报，信息来源要靠谱。",
                volume=0.1,
                welcome_msg="你好，我是天气预报助手，请问你想查询哪个城市的天气？",
                voice="bright_sisi",
            ),
            enable_subtitle_log=True,
        )
        print("语音对话已启动，按 Ctrl+C 退出")
        status = handle.wait()
        print(f"语音对话已结束: status={status}")
    except KeyboardInterrupt:
        print("\n正在停止语音对话...")
        if handle is not None:
            handle.cancel()
            handle.wait(timeout=5.0)


if __name__ == "__main__":
    main()
