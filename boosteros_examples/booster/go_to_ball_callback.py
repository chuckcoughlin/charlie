"""Track a soccer ball with image subscription callbacks."""

import logging
import time

from boosteros.brain import Detection
from boosteros.robots.booster import BoosterRobot, current_debug_trace
from boosteros.types import CompressedImage

# --- 控制参数微调 ---
MAX_VX = 0.3  # 最大前进速度 (m/s)
MAX_VYAW = 0.8  # 最大旋转角速度 (rad/s)
CONFIDENCE_THRESHOLD = 0.4  # 检测置信度阈值

logger = logging.getLogger(__name__)


def go_to_ball_callback():
    """Run the callback-based ball tracking demo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    print("正在初始化机器人与目标检测器...")
    robot = BoosterRobot()
    detector = Detection(model="soccer", backend="local")

    if (cur_mode := robot.get_mode()) != "walk":
        print(f"Current mode is {cur_mode}, not walk")
        robot.set_mode("walk")

    def on_frame(frame):
        start_ns = time.monotonic_ns()
        trace = current_debug_trace()
        logger.info(
            "收到图像回调: trace_uid=%s size=%s encoding=%s compressed=%s",
            trace.uid if trace is not None else None,
            frame.size(),
            getattr(frame, "encoding", getattr(frame, "format", "unknown")),
            isinstance(frame, CompressedImage),
        )
        try:
            detections = detector.detect(
                frame.to_numpy(), confidence=CONFIDENCE_THRESHOLD
            )
            detect_ms = (time.monotonic_ns() - start_ns) / 1_000_000
            logger.info(
                "检测完成: detections=%d detect_ms=%.3f",
                len(detections),
                detect_ms,
            )
            ball = max(
                (d for d in detections if d.class_name == "Ball"),
                key=lambda d: d.confidence,
                default=None,
            )

            if ball is not None:
                error = (ball.bbox.center_x - frame.size()[0] / 2) / (
                    frame.size()[0] / 2
                )
                vyaw = -error * MAX_VYAW * 0.5
                robot.set_velocity(vx=MAX_VX, vy=0.0, vyaw=vyaw)
                logger.info(
                    "[TRACKING] Ball Found! confidence=%.2f error=%.2f "
                    "vx=%.2f vyaw=%.2f",
                    ball.confidence,
                    error,
                    MAX_VX,
                    vyaw,
                )
            else:
                vyaw = MAX_VYAW * 0.5
                robot.set_velocity(vx=0.0, vy=0.0, vyaw=vyaw)
                logger.info("[SEARCHING] Ball lost, vx=0.00 vyaw=%.2f", vyaw)
        except Exception:
            logger.exception("图像回调处理失败")

    sub = robot.subscribe_image(
        on_frame,
        img_type="rgb",
        queue_size=1,
        overflow="drop_oldest",
    )
    logger.info("已订阅 RGB 图像: queue_size=1 overflow=drop_oldest")

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n用户手动中断，正在清理资源...")
    finally:
        sub.unsubscribe()
        robot.set_velocity(0.0, 0.0, 0.0)
        print("机器人已停止，连接已关闭。")


if __name__ == "__main__":
    go_to_ball_callback()
