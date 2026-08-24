"""Half-duplex voice echo example for Booster robots."""

from __future__ import annotations

import select
import sys
import threading
import time

from boosteros.robots.booster import BoosterRobot
from boosteros.types.audio_data import AudioData

AUDIO_SESSION_SWITCH_DELAY_SEC = 2.0
PLAYBACK_VOLUME = 0.1


def _wait_for_enter(prompt: str) -> None:
    print(prompt, flush=True)
    while True:
        readable, _, _ = select.select([sys.stdin], [], [], 0.1)
        if readable:
            sys.stdin.readline()
            return


def _signal_on_enter(prompt: str, event: threading.Event) -> None:
    _wait_for_enter(prompt)
    event.set()


def _record_utterance(robot: BoosterRobot) -> AudioData | None:
    input("按回车开始说话...")
    chunks: list[AudioData] = []
    stop_requested = threading.Event()
    threading.Thread(
        target=_signal_on_enter,
        args=("录音中，按回车停止...", stop_requested),
        daemon=True,
    ).start()

    for chunk in robot.audio_manager.record_stream(stop_event=stop_requested):
        chunks.append(chunk)

    if not chunks:
        print("没有采集到有效音频")
        return None
    return AudioData.concat(chunks)


def _play_audio(robot: BoosterRobot, audio: AudioData) -> None:
    handle = robot.play_sound(audio, volume=PLAYBACK_VOLUME)
    status = handle.wait(timeout=audio.duration.seconds + 10.0)
    print(f"播放结束: status={status}")


def echo_chat_example() -> None:
    """Record one utterance from the user and play it back through the robot."""
    robot = BoosterRobot()
    print("机器人连接就绪")

    while True:
        audio = _record_utterance(robot)
        if audio is not None:
            print(
                "录音完成:",
                f"bytes={len(audio.data)}, ",
                f"duration={audio.duration.seconds:.2f}s, ",
                f"format={audio.sample_rate}/{audio.channels}/{audio.bit_depth}",
            )
            time.sleep(AUDIO_SESSION_SWITCH_DELAY_SEC)
            _play_audio(robot, audio)
            time.sleep(0.2)

        again = input("继续下一轮？[Y/n]: ").strip().lower()
        if again in {"n", "no", "q", "quit", "exit"}:
            break

    print("示例结束")


def main() -> None:
    try:
        echo_chat_example()
    except KeyboardInterrupt:
        print("\n检测到用户中断")
    except Exception as exc:
        print(f"chat 示例出错: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
