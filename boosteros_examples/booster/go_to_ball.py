import time

from boosteros.brain import Detection
from boosteros.robots.booster import BoosterRobot

# --- 控制参数微调 ---
MAX_VX = 0.3  # 最大前进速度 (m/s)
KP_YAW = 1.0  # 转向角速度增益 (P-Control)
MAX_VYAW = 0.8  # 最大旋转角速度 (rad/s)
CONFIDENCE_THRESHOLD = 0.4  # 检测置信度阈值


def go_to_ball():
    # 1. 初始化机器人与目标检测器
    print("正在初始化机器人与检测模型...")
    robot = BoosterRobot()
    # 使用本地模式加载 Robocup (soccer) 模型
    detector = Detection(model="soccer", backend="local")

    # 切换行走状态
    if (cur_mode := robot.get_mode()) != "walk":
        print(f"Current mode is {cur_mode}, not walk")
        robot.set_mode("walk")

    try:
        while True:
            # 获取图像并检测
            frame = robot.get_image()
            detections = detector.detect(
                frame.to_numpy(), confidence=CONFIDENCE_THRESHOLD
            )

            # 3. 寻找置信度最高的 "Ball" (球)
            if ball := max(
                (d for d in detections if d.class_name == "Ball"),
                key=lambda d: d.confidence,
                default=None,
            ):
                # --- [逻辑A] 发现球：追踪模式 ---
                error = (ball.bbox.center_x - frame.size()[0] / 2) / (
                    frame.size()[0] / 2
                )
                vyaw = -error * MAX_VYAW * 0.5
                robot.set_velocity(vx=MAX_VX, vy=0.0, vyaw=vyaw)
                print(
                    f"[TRACKING] Ball Found! Error: {error:.2f}, VX: {MAX_VX:.2f}, VYAW: {vyaw:.2f}"
                )

            else:
                # --- [逻辑B] 球消失：寻球模式 ---
                # 原地按照最后记录的方向旋转寻球
                robot.set_velocity(vx=0.0, vy=0.0, vyaw=MAX_VYAW * 0.5)
                print(
                    f"[SEARCHING] Ball lost, rotating at {MAX_VYAW:.2f} to find it..."
                )

            # 适当休眠，降低 CPU 负载并匹配检测频率
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n用户手动中断，正在清理资源...")
    finally:
        # 4. 安全退出：停止运动并释放连接
        robot.set_velocity(0.0, 0.0, 0.0)
        print("机器人已停止，连接已关闭。")


if __name__ == "__main__":
    go_to_ball()
