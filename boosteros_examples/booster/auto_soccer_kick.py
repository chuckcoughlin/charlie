"""Automatically approach the ball using soccer truth topics, then kick."""

from __future__ import annotations

import argparse
import logging
import math
import threading
import time
from dataclasses import dataclass
from typing import Sequence

import rclpy
from geometry_msgs.msg import Pose2D
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from vision_msgs.msg import Detection2DArray

from boosteros.robots.booster import BoosterRobot, SoccerKickManager

BALL_CLASS_ID = "Ball"
DEFAULT_POSE_TOPIC = "soccer/sim/localization/robot_pose"
DEFAULT_DETECTION_TOPIC = "soccer/sim/vision/detections"

HEAD_PITCH = 0.45
SEARCH_VYAW = 0.35
UPDATE_RATE_HZ = 30.0
BALL_TIMEOUT_S = 2.0

FIELD_LENGTH_M = 14.0
GOAL_Y_M = 0.0
KICK_START_MAX_RANGE_M = 3.0

MAX_VX = 0.8
MIN_VX = 0.5
MAX_VY = 0.25
MAX_VYAW = 0.8
KP_XY = 0.8
KP_YAW = 1.4
YAW_COMMAND_SIGN = 1.0

DEFAULT_KICK_POWER = 1.5
MAX_KICK_POWER = 1.5
POWER_DISTANCE_SCALE_M = 10.0

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RobotPose2D:
    x: float
    y: float
    theta: float
    stamp: float


@dataclass(frozen=True)
class _TrackedBall:
    rel_x: float
    rel_y: float
    field_x: float | None
    field_y: float | None
    confidence: float
    stamp: float


@dataclass(frozen=True)
class BallEstimate:
    rel_x: float
    rel_y: float
    range_m: float
    confidence: float
    age_s: float
    field_x: float | None
    field_y: float | None
    robot_pose: RobotPose2D | None


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _normalize_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


def _rel_to_field(
    rel_x: float,
    rel_y: float,
    robot_pose: RobotPose2D,
) -> tuple[float, float]:
    cos_theta = math.cos(robot_pose.theta)
    sin_theta = math.sin(robot_pose.theta)
    field_x = robot_pose.x + rel_x * cos_theta - rel_y * sin_theta
    field_y = robot_pose.y + rel_x * sin_theta + rel_y * cos_theta
    return field_x, field_y


def _field_to_rel(
    field_x: float,
    field_y: float,
    robot_pose: RobotPose2D,
) -> tuple[float, float]:
    dx = field_x - robot_pose.x
    dy = field_y - robot_pose.y
    cos_theta = math.cos(robot_pose.theta)
    sin_theta = math.sin(robot_pose.theta)
    rel_x = dx * cos_theta + dy * sin_theta
    rel_y = -dx * sin_theta + dy * cos_theta
    return rel_x, rel_y


class TruthBallNode(Node):
    """Subscribe soccer truth topics and expose the ball in robot coordinates."""

    def __init__(
        self,
        *,
        namespace: str,
        pose_topic: str,
        detection_topic: str,
        min_confidence: float,
    ) -> None:
        super().__init__("auto_soccer_kick_node", namespace=namespace or None)
        self._min_confidence = min_confidence
        self._lock = threading.RLock()
        self._latest_pose: RobotPose2D | None = None
        self._latest_ball: _TrackedBall | None = None
        self._last_detection_msg_at: float | None = None
        self._pose_event = threading.Event()
        self._ball_event = threading.Event()

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )
        self._pose_sub = self.create_subscription(
            Pose2D,
            pose_topic,
            self._on_pose,
            qos,
        )
        self._detection_sub = self.create_subscription(
            Detection2DArray,
            detection_topic,
            self._on_detections,
            qos,
        )
        logger.info(
            "Truth ROS subscriptions ready: pose=%s detections=%s namespace=%s",
            pose_topic,
            detection_topic,
            self.get_namespace(),
        )

    def _on_pose(self, msg: Pose2D) -> None:
        pose = RobotPose2D(
            x=float(msg.x),
            y=float(msg.y),
            theta=_normalize_angle(float(msg.theta)),
            stamp=time.monotonic(),
        )
        with self._lock:
            self._latest_pose = pose
        self._pose_event.set()

    def _on_detections(self, msg: Detection2DArray) -> None:
        now = time.monotonic()
        best = self._extract_best_ball(msg)
        with self._lock:
            self._last_detection_msg_at = now
            pose = self._latest_pose

        if best is None:
            return

        rel_x, rel_y, confidence = best
        field_x = None
        field_y = None
        if pose is not None:
            field_x, field_y = _rel_to_field(rel_x, rel_y, pose)

        with self._lock:
            self._latest_ball = _TrackedBall(
                rel_x=rel_x,
                rel_y=rel_y,
                field_x=field_x,
                field_y=field_y,
                confidence=confidence,
                stamp=now,
            )
        self._ball_event.set()

    def _extract_best_ball(
        self,
        msg: Detection2DArray,
    ) -> tuple[float, float, float] | None:
        best: tuple[float, float, float] | None = None
        best_score = -math.inf

        for detection in msg.detections:
            for result in detection.results:
                hypothesis = getattr(result, "hypothesis", None)
                if hypothesis is None:
                    continue

                class_id = str(getattr(hypothesis, "class_id", ""))
                if class_id != BALL_CLASS_ID:
                    continue

                score = float(getattr(hypothesis, "score", 0.0) or 0.0)
                if score < self._min_confidence or score <= best_score:
                    continue

                position = result.pose.pose.position
                rel_x = float(position.x)
                rel_y = float(position.y)
                if not math.isfinite(rel_x) or not math.isfinite(rel_y):
                    continue

                best = (rel_x, rel_y, score)
                best_score = score

        return best

    def wait_for_initial_data(self, timeout: float) -> tuple[bool, bool]:
        pose_ready = self._pose_event.wait(timeout=timeout)
        ball_ready = self._ball_event.wait(timeout=timeout)
        return pose_ready, ball_ready

    def get_robot_pose(self) -> RobotPose2D | None:
        with self._lock:
            return self._latest_pose

    def get_ball_estimate(self, max_age_s: float | None) -> BallEstimate | None:
        now = time.monotonic()
        with self._lock:
            ball = self._latest_ball
            pose = self._latest_pose

        if ball is None:
            return None

        age_s = now - ball.stamp
        if max_age_s is not None and age_s > max_age_s:
            return None

        rel_x = ball.rel_x
        rel_y = ball.rel_y
        if pose is not None and ball.field_x is not None and ball.field_y is not None:
            rel_x, rel_y = _field_to_rel(ball.field_x, ball.field_y, pose)

        return BallEstimate(
            rel_x=rel_x,
            rel_y=rel_y,
            range_m=math.hypot(rel_x, rel_y),
            confidence=ball.confidence,
            age_s=age_s,
            field_x=ball.field_x,
            field_y=ball.field_y,
            robot_pose=pose,
        )


class AutoSoccerKickApp:
    """Go to the ball with truth data, then hand over to visual kick."""

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args
        self._goal_x, self._goal_y = self._resolve_goal_point(args)
        self._stop_event = threading.Event()
        self._closed = False
        self._kick_started = False
        self._last_status_log_at = 0.0
        self._last_missing_log_at = 0.0
        self._last_kick_update_at: float | None = None
        self._last_goal_direction: float | None = None

        self._robot: BoosterRobot | None = None
        self._soccer_kick_mgr: SoccerKickManager | None = None
        self._truth_node: TruthBallNode | None = None
        self._executor: MultiThreadedExecutor | None = None
        self._spin_thread: threading.Thread | None = None

    def run(self) -> None:
        self._start_ros_node()
        self._setup_robot()
        self._wait_for_truth_topics()

        try:
            self._main_loop()
        finally:
            self.close()

    def _start_ros_node(self) -> None:
        if not rclpy.ok():
            rclpy.init(args=[])

        self._truth_node = TruthBallNode(
            namespace=self._args.robot_name,
            pose_topic=self._args.pose_topic,
            detection_topic=self._args.detection_topic,
            min_confidence=self._args.min_confidence,
        )
        self._executor = MultiThreadedExecutor(num_threads=2)
        self._executor.add_node(self._truth_node)
        self._spin_thread = threading.Thread(target=self._spin_ros, daemon=True)
        self._spin_thread.start()

    def _spin_ros(self) -> None:
        assert self._executor is not None
        try:
            self._executor.spin()
        except Exception as exc:
            if not self._stop_event.is_set() and rclpy.ok():
                logger.warning("truth ROS executor stopped unexpectedly: %s", exc)

    def _setup_robot(self) -> None:
        logger.info("Initializing BoosterRobot...")
        self._robot = BoosterRobot(
            virtual_robot_name=self._args.robot_name,
            timeout=self._args.robot_timeout,
            use_sim_time=self._args.use_sim_time,
        )
        self._robot.set_gait("soccer")
        self._robot.set_mode("walk")
        self._soccer_kick_mgr = SoccerKickManager(self._robot)
        self._robot.set_head_angle(pitch=self._args.head_pitch, yaw=0.0)
        self._robot.set_velocity(vx=0.0, vy=0.0, vyaw=0.0)
        logger.info("Robot is in walk mode with soccer gait.")

    def _wait_for_truth_topics(self) -> None:
        assert self._truth_node is not None
        if self._args.startup_wait <= 0.0:
            return

        pose_ready, ball_ready = self._truth_node.wait_for_initial_data(
            timeout=self._args.startup_wait,
        )
        if not pose_ready:
            logger.warning("No robot pose received yet.")
        if not ball_ready:
            logger.warning("No ball detection received yet; entering search.")

    def _main_loop(self) -> None:
        period_s = 1.0 / max(1.0, self._args.update_rate)
        while not self._stop_event.is_set():
            try:
                self._tick()
            except Exception as exc:
                logger.warning("auto_soccer_kick tick failed: %s", exc)
            time.sleep(period_s)

    def _tick(self) -> None:
        assert self._robot is not None
        assert self._truth_node is not None

        pose = self._truth_node.get_robot_pose()
        ball = self._truth_node.get_ball_estimate(max_age_s=self._args.ball_timeout)

        if pose is None or ball is None or ball.field_x is None or ball.field_y is None:
            self._handle_missing_truth()
            return

        if self._kick_started:
            direction, power = self._update_kick_reference(pose, ball)
            self._log_kicking(ball, direction, power)
            return

        if ball.range_m <= self._args.kick_start_max_range:
            self._start_kick(pose, ball)
            return

        self._track_ball(ball)

    def _handle_missing_truth(self) -> None:
        assert self._robot is not None
        now = time.monotonic()

        if self._kick_started:
            if now - self._last_missing_log_at >= 1.0:
                logger.warning("Ball truth lost during visual kick; stopping kick.")
                self._last_missing_log_at = now
            self._stop_kick()
            return

        self._robot.set_velocity(vx=0.0, vy=0.0, vyaw=self._args.search_vyaw)
        if now - self._last_missing_log_at >= 1.0:
            logger.info("[SEARCH] waiting for fresh pose/ball truth")
            self._last_missing_log_at = now

    def _track_ball(self, ball: BallEstimate) -> None:
        assert self._robot is not None

        yaw_error = math.atan2(ball.rel_y, ball.rel_x)
        range_error = max(0.0, ball.range_m - self._args.kick_start_max_range)
        vx = _clamp(
            self._args.kp_xy * range_error, self._args.min_vx, self._args.max_vx
        )
        vy = _clamp(
            self._args.kp_xy * ball.rel_y, -self._args.max_vy, self._args.max_vy
        )
        vyaw = _clamp(
            self._args.yaw_command_sign * self._args.kp_yaw * yaw_error,
            -self._args.max_vyaw,
            self._args.max_vyaw,
        )
        self._robot.set_velocity(vx=vx, vy=vy, vyaw=vyaw)

        now = time.monotonic()
        if now - self._last_status_log_at >= 0.5:
            logger.info(
                "[GO_TO_BALL] ball_rel=(%.2f, %.2f) range=%.2f range_error=%.2f yaw_error=%.2f cmd=(%.2f, %.2f, %.2f)",
                ball.rel_x,
                ball.rel_y,
                ball.range_m,
                range_error,
                yaw_error,
                vx,
                vy,
                vyaw,
            )
            self._last_status_log_at = now

    def _start_kick(self, pose: RobotPose2D, ball: BallEstimate) -> None:
        assert self._robot is not None
        assert self._soccer_kick_mgr is not None
        assert ball.field_x is not None
        assert ball.field_y is not None

        self._robot.set_velocity(vx=0.0, vy=0.0, vyaw=0.0)
        self._soccer_kick_mgr.start()
        self._kick_started = True
        direction, power = self._update_kick_reference(pose, ball)

        logger.info(
            "[KICK START] goal=(%.2f, %.2f) direction=%.3f power=%.2f ball_rel=(%.2f, %.2f) ball_field=(%.2f, %.2f)",
            self._goal_x,
            self._goal_y,
            direction,
            power,
            ball.rel_x,
            ball.rel_y,
            ball.field_x,
            ball.field_y,
        )

    def _update_kick_reference(
        self,
        pose: RobotPose2D,
        ball: BallEstimate,
    ) -> tuple[float, float]:
        assert self._soccer_kick_mgr is not None

        direction = self._compute_goal_direction(pose, ball)
        power = self._compute_kick_power(ball)
        self._soccer_kick_mgr.update_command(direction=direction, power=power)
        self._soccer_kick_mgr.update_ball(ball.rel_x, ball.rel_y)
        self._last_kick_update_at = time.monotonic()
        self._last_goal_direction = direction
        return direction, power

    def _compute_goal_direction(self, pose: RobotPose2D, ball: BallEstimate) -> float:
        assert ball.field_x is not None
        assert ball.field_y is not None

        kick_heading = math.atan2(
            self._goal_y - ball.field_y,
            self._goal_x - ball.field_x,
        )
        return _normalize_angle(kick_heading - pose.theta)

    def _compute_kick_power(self, ball: BallEstimate) -> float:
        if not self._args.auto_power:
            return _clamp(self._args.power, 1.0, self._args.max_power)

        assert ball.field_x is not None
        assert ball.field_y is not None
        distance_to_goal = math.hypot(
            self._goal_x - ball.field_x, self._goal_y - ball.field_y
        )
        power = 1.0 + (distance_to_goal / self._args.power_distance_scale) * 9.0
        return _clamp(power, 1.0, self._args.max_power)

    def _log_kicking(
        self,
        ball: BallEstimate,
        direction: float,
        power: float,
    ) -> None:
        now = time.monotonic()
        if now - self._last_status_log_at < 0.5:
            return
        logger.info(
            "[KICKING] ball_rel=(%.2f, %.2f) range=%.2f direction=%.3f power=%.2f conf=%.2f update_age=%.2f",
            ball.rel_x,
            ball.rel_y,
            ball.range_m,
            direction,
            power,
            ball.confidence,
            0.0
            if self._last_kick_update_at is None
            else now - self._last_kick_update_at,
        )
        self._last_status_log_at = now

    def _stop_kick(self) -> None:
        assert self._robot is not None
        if self._kick_started:
            try:
                if self._soccer_kick_mgr is not None:
                    self._soccer_kick_mgr.stop()
            finally:
                self._kick_started = False
        self._robot.set_velocity(vx=0.0, vy=0.0, vyaw=0.0)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._stop_event.set()

        if self._robot is not None:
            try:
                self._stop_kick()
            except Exception:
                try:
                    self._robot.set_velocity(vx=0.0, vy=0.0, vyaw=0.0)
                except Exception:
                    pass

        if self._executor is not None:
            if self._truth_node is not None:
                try:
                    self._executor.remove_node(self._truth_node)
                except Exception:
                    pass
            self._executor.shutdown()

        if self._spin_thread is not None and self._spin_thread.is_alive():
            self._spin_thread.join(timeout=2.0)

        if self._truth_node is not None:
            self._truth_node.destroy_node()

    @staticmethod
    def _resolve_goal_point(args: argparse.Namespace) -> tuple[float, float]:
        goal_x = args.field_length / 2.0
        if args.attack_direction == "-x":
            goal_x = -goal_x
        return goal_x, args.goal_y


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use soccer truth topics to approach the ball, then start visual kick toward the goal."
    )
    parser.add_argument(
        "--robot-name",
        default="",
        help="Virtual robot name / ROS namespace, for example robot1.",
    )
    parser.add_argument(
        "--pose-topic",
        default=DEFAULT_POSE_TOPIC,
        help="Robot Pose2D truth topic. Relative topics use --robot-name namespace.",
    )
    parser.add_argument(
        "--detection-topic",
        default=DEFAULT_DETECTION_TOPIC,
        help="Detection2DArray topic. Relative topics use --robot-name namespace.",
    )
    parser.add_argument(
        "--field-length",
        type=float,
        default=FIELD_LENGTH_M,
        help="Field length in meters. Goal x is +/- field_length / 2.",
    )
    parser.add_argument(
        "--attack-direction",
        choices=["+x", "-x"],
        default="+x",
        help="Which field x direction contains the opponent goal.",
    )
    parser.add_argument(
        "--goal-y",
        type=float,
        default=GOAL_Y_M,
        help="Goal target y in field coordinates.",
    )
    parser.add_argument(
        "--kick-start-max-range",
        type=float,
        default=KICK_START_MAX_RANGE_M,
        help="Start visual kick when the ball is no farther than this range.",
    )
    parser.add_argument("--max-vx", type=float, default=MAX_VX)
    parser.add_argument("--min-vx", type=float, default=MIN_VX)
    parser.add_argument("--max-vy", type=float, default=MAX_VY)
    parser.add_argument("--max-vyaw", type=float, default=MAX_VYAW)
    parser.add_argument("--kp-xy", type=float, default=KP_XY)
    parser.add_argument("--kp-yaw", type=float, default=KP_YAW)
    parser.add_argument(
        "--yaw-command-sign",
        type=float,
        choices=[-1.0, 1.0],
        default=YAW_COMMAND_SIGN,
        help="Sign applied to approach vyaw command. Standard Booster convention is 1.0: left turn is positive.",
    )
    parser.add_argument("--head-pitch", type=float, default=HEAD_PITCH)
    parser.add_argument("--search-vyaw", type=float, default=SEARCH_VYAW)
    parser.add_argument(
        "--power",
        type=float,
        default=DEFAULT_KICK_POWER,
        help="Fixed kick power when --no-auto-power is used.",
    )
    parser.add_argument(
        "--max-power",
        type=float,
        default=MAX_KICK_POWER,
        help="Clamp kick power to this value.",
    )
    parser.add_argument(
        "--auto-power",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Compute kick power from ball-to-goal distance.",
    )
    parser.add_argument(
        "--power-distance-scale",
        type=float,
        default=POWER_DISTANCE_SCALE_M,
        help="Distance that maps near max power when --auto-power is enabled.",
    )
    parser.add_argument(
        "--ball-timeout",
        type=float,
        default=BALL_TIMEOUT_S,
        help="Max age in seconds for a ball estimate.",
    )
    parser.add_argument(
        "--update-rate",
        type=float,
        default=UPDATE_RATE_HZ,
        help="Main control loop rate in Hz.",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.0,
        help="Minimum Detection2D score accepted as a ball.",
    )
    parser.add_argument(
        "--startup-wait",
        type=float,
        default=2.0,
        help="Seconds to wait for initial pose and ball messages.",
    )
    parser.add_argument(
        "--robot-timeout",
        type=float,
        default=5.0,
        help="BoosterRobot initialization timeout.",
    )
    parser.add_argument(
        "--use-sim-time",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Forward use_sim_time to BoosterRobot ROS adapter.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level.",
    )
    return parser


def auto_soccer_kick(argv: Sequence[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    app = AutoSoccerKickApp(args)
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user, cleaning up...")
    finally:
        app.close()


if __name__ == "__main__":
    auto_soccer_kick()
