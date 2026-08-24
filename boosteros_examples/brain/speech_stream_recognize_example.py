"""Realtime speech recognition from the robot microphone."""

from __future__ import annotations

from boosteros import brain
from boosteros.robots.booster import BoosterRobot


def main() -> None:
    """Start streaming ASR and print recognized text."""
    robot = BoosterRobot()
    handle = None
    try:
        speech = brain.Speech(robot)
        handle = speech.recognize_stream(
            on_result=lambda text: print(f"识别结果: {text}", flush=True),
        )
        print("流式语音识别已启动，按 Ctrl+C 退出")
        status = handle.wait()
        print(f"流式语音识别已结束: status={status}")
    except KeyboardInterrupt:
        print("\n正在停止流式语音识别...")
        if handle is not None:
            handle.cancel()
            handle.wait(timeout=5.0)


if __name__ == "__main__":
    main()
