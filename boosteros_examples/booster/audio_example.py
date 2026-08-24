"""Audio example module for BoosterOS."""

import select
import sys
import time
from pathlib import Path

from boosteros.robots.booster import BoosterRobot
from boosteros.types.audio_data import AudioData

SAVE_FORMATS = ("wav", "pcm", "mp3")
CANCEL_DELAY_SEC = 1.0
MIN_REGRESSION_AUDIO_SEC = 5.0
PLAYBACK_VOLUME = 0.1


def _wait_for_enter(prompt: str) -> None:
    print(prompt, flush=True)
    while True:
        readable, _, _ = select.select([sys.stdin], [], [], 0.1)
        if readable:
            sys.stdin.readline()
            return


def _record_audio(robot: BoosterRobot) -> AudioData:
    audio_manager = robot.audio_manager
    audio_manager.start_recording()
    print(f"录音状态: is_recording={audio_manager.is_recording()}")
    _wait_for_enter("录音开始，按回车停止...")
    print(f"停止前录音时长: {audio_manager.get_recording_duration():.2f}s")
    audio = audio_manager.stop_recording()
    print(f"停止后录音状态: is_recording={audio_manager.is_recording()}")
    return audio


def _print_audio_info(audio: AudioData) -> None:
    print(
        "录音完成:",
        f"bytes={len(audio.data)}",
        f"duration={audio.duration.seconds:.2f}s",
        f"format={audio.sample_rate}/{audio.channels}/{audio.bit_depth}",
    )


def _repeat_audio_for_regression(audio: AudioData) -> AudioData:
    """Repeat short recordings so playback regression checks have time to run."""
    duration = audio.duration.seconds
    if duration <= 0 or duration >= MIN_REGRESSION_AUDIO_SEC:
        return audio
    repeat_count = int(MIN_REGRESSION_AUDIO_SEC / duration) + 1
    return audio.with_data(audio.data * repeat_count)


def record_and_compare_play_example() -> None:
    """Record once and compare in-memory playback with wav playback."""
    try:
        robot = BoosterRobot()
        audio = _record_audio(robot)
        _print_audio_info(audio)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = Path.cwd() / f"recorded_compare_{timestamp}.wav"
        audio.save(str(output_path))
        print(f"已保存 wav 对照文件: {output_path}")

        print("\n请选择播放方式:")
        print("  1. 只播放内存音频")
        print("  2. 只播放 wav 文件")
        print("  3. 先播放内存音频，按回车后再播放 wav 文件")
        choice = input("请输入选项: ").strip()

        if choice in {"1", "3"}:
            print("开始内存播放...")
            handle = robot.play_sound(audio, volume=PLAYBACK_VOLUME)
            status = handle.wait(timeout=audio.duration.seconds + 10.0)
            print(f"内存播放结束: status={status}")

        if choice == "3":
            input("按回车继续播放 wav 文件...")

        if choice in {"2", "3"}:
            print("开始 wav 文件播放...")
            handle = robot.play_sound(str(output_path), volume=PLAYBACK_VOLUME)
            status = handle.wait(timeout=audio.duration.seconds + 10.0)
            print(f"wav 文件播放结束: status={status}")

        if choice not in {"1", "2", "3"}:
            print(f"未知选项: {choice}")
    except Exception as exc:
        print(f"录音播放对照示例出错: {type(exc).__name__}: {exc}")


def record_save_and_play_example() -> None:
    """Record audio, save it as wav, pcm, and mp3, then play each file."""
    try:
        robot = BoosterRobot()
        audio = _record_audio(robot)
        _print_audio_info(audio)
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        for suffix in SAVE_FORMATS:
            output_path = Path.cwd() / f"recorded_{timestamp}.{suffix}"
            try:
                audio.save(str(output_path))
                print(f"已保存: {output_path}")
                # PCM 文件没有 header；当前播放默认按 16kHz/mono/S16LE 解释。
                handle = robot.play_sound(str(output_path), volume=PLAYBACK_VOLUME)
                status = handle.wait(timeout=audio.duration.seconds + 10.0)
                print(f"{suffix} 播放结束: status={status}")
            except Exception as exc:
                print(f"{suffix} 保存或播放失败: {type(exc).__name__}: {exc}")
    except Exception as exc:
        print(f"录音保存播放示例出错: {type(exc).__name__}: {exc}")


def cancel_playback_example() -> None:
    """Record audio, start async playback, then cancel it before completion."""
    try:
        robot = BoosterRobot()
        audio = _repeat_audio_for_regression(_record_audio(robot))
        _print_audio_info(audio)

        print("开始内存播放，将在约 1 秒后取消...")
        handle = robot.play_sound(audio, volume=PLAYBACK_VOLUME)
        time.sleep(CANCEL_DELAY_SEC)
        accepted = handle.cancel()
        print(f"取消请求已发送: {accepted}")

        status = handle.wait(timeout=5.0)
        print(f"播放任务结束: status={status}")
    except Exception as exc:
        print(f"取消播放示例出错: {type(exc).__name__}: {exc}")


def audio_task_exclusive_example() -> None:
    """Verify in-memory playback and file playback cannot run at the same time."""
    try:
        robot = BoosterRobot()
        audio = _repeat_audio_for_regression(_record_audio(robot))
        _print_audio_info(audio)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = Path.cwd() / f"exclusive_check_{timestamp}.wav"
        audio.save(str(output_path))
        print(f"已保存互斥检查文件: {output_path}")

        print("启动内存播放...")
        handle = robot.play_sound(audio, volume=PLAYBACK_VOLUME)
        time.sleep(0.2)

        try:
            print("尝试在内存播放未结束时启动 wav 文件播放...")
            robot.play_sound(str(output_path), volume=PLAYBACK_VOLUME)
        except RuntimeError as exc:
            print(f"互斥检查通过，第二个音频任务被拒绝: {exc}")
        else:
            print("互斥检查未通过：第二个音频任务被启动了")
        finally:
            if not handle.done():
                handle.cancel()
            status = handle.wait(timeout=5.0)
            print(f"已清理内存播放任务: status={status}")
    except Exception as exc:
        print(f"音频任务互斥示例出错: {type(exc).__name__}: {exc}")


def system_volume_round_trip_example() -> None:
    """Read the system volume and write the same value back."""
    try:
        robot = BoosterRobot()
        audio_manager = robot.audio_manager
        current_volume = audio_manager.get_system_volume()
        print(f"当前系统音量: {current_volume:.2f}")
        audio_manager.set_system_volume(current_volume)
        print(f"已写回相同系统音量: {current_volume:.2f}")
    except Exception as exc:
        print(f"系统音量读写示例出错: {type(exc).__name__}: {exc}")


def main() -> None:
    """Interactive entry point for audio examples."""
    actions = {
        "1": "录音并对照播放（内存播放 vs wav 文件）",
        "2": "录音保存到文件并播放（wav/pcm/mp3）",
        "3": "异步内存播放取消回归",
        "4": "音频任务互斥回归（内存播放 vs 文件播放）",
        "5": "系统音量读写回环",
    }

    print("\n请选择要执行的功能:")
    for key, title in actions.items():
        print(f"  {key}. {title}")
    print("  q. 退出")

    choice = input("请输入选项: ").strip().lower()
    if choice in {"q", "quit", "exit"}:
        print("已退出")
        return

    if choice == "1":
        record_and_compare_play_example()
        return

    if choice == "2":
        record_save_and_play_example()
        return

    if choice == "3":
        cancel_playback_example()
        return

    if choice == "4":
        audio_task_exclusive_example()
        return

    if choice == "5":
        system_volume_round_trip_example()
        return

    print(f"未知选项: {choice}")


if __name__ == "__main__":
    main()
