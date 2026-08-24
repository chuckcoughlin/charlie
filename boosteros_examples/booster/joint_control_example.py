from __future__ import annotations

import logging
import time

from boosteros.robots.booster import BoosterRobot
from boosteros.types import JointCommand

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("JointDebugger")


def run_joint_control_demo():
    """Interactive joint debugging example.

    1. Smoothly takes over the current pose from prepare mode.
    2. Supports changing individual joint angles from the command line.
    """
    # 1. 初始化机器人客户端
    try:
        robot = BoosterRobot()
        logger.info("机器人连接就绪")
    except Exception as e:
        logger.error(f"无法初始化机器人客户端: {e}")
        return

    try:
        # 2. 准备阶段：先让机器人站稳
        logger.info("正在进入 prepare 模式，请等待姿态稳定...")
        robot.set_mode("prepare")
        time.sleep(2.0)  # 等待机械臂和身体回正

        # 3. 获取初始状态
        joint_names = [joint.name for joint in robot.list_joints()]
        num_joints = len(joint_names)

        # 读取当前 prepare 状态下的实时关节角度
        current_state = robot.get_joint_states()
        # 建立名称到实时角度的映射
        state_map = {js.name: js.position for js in current_state.joints}

        # 预设增益 (全机平衡增益：低刚度、强阻尼，提升动态稳定性)
        # TODO: Replace these example gains with firmware-provided recommended
        # Booster K1/T1 gain tables once the lower-level control team publishes
        # validated per-joint kp/kd values.
        kp_values = [
            40.0,
            40.0,  # neck (0-1)
            20.0,
            30.0,
            10.0,
            10.0,  # left arm (2-5)
            20.0,
            30.0,
            10.0,
            10.0,  # right arm (6-9)
            # 腿部：降低刚度避免脆性振动，维持支撑力的同时增加吸震
            250.0,
            250.0,
            150.0,
            250.0,
            120.0,
            120.0,  # left leg (10-15)
            250.0,
            250.0,
            150.0,
            250.0,
            120.0,
            120.0,  # right leg (16-21)
        ]
        kd_values = [
            2.0,
            2.0,  # neck
            1.5,
            2.0,
            0.5,
            0.5,  # left arm
            1.5,
            2.0,
            0.5,
            0.5,  # right arm
            # 腿部阻尼：显著提升踝关节和膝关节阻尼，过滤地面冲击
            15.0,
            15.0,
            8.0,
            12.0,
            8.0,
            8.0,  # left leg
            15.0,
            15.0,
            8.0,
            12.0,
            8.0,
            8.0,  # right leg
        ]

        # T1 机型适配 (腰部需要更大的阻尼来消散上身动量)
        if num_joints == 23:
            kp_values.insert(10, 100.0)
            kd_values.insert(10, 8.0)

        # 4. 初始化全量指令缓存 (以实时位姿为起点)
        cmd_cache: dict[str, JointCommand] = {}
        for i, name in enumerate(joint_names):
            pos = state_map.get(name, 0.0)
            cmd_cache[name] = JointCommand(
                name=name, position=pos, kp=kp_values[i], kd=kd_values[i]
            )

        # 5. 原子切换：模式切换后立即下发指令，保证机器人不倒地
        logger.info("正在切换到 custom 模式并接管控制...")
        robot.set_mode("custom")
        # 立即使用从 prepare 读取到的角度进行锁存
        robot.set_joints(list(cmd_cache.values()))
        logger.info("已成功接管，机器人当前维持在 prepare 姿态")

        # 6. 交互式控制循环
        print("\n" + "=" * 60)
        print(" 关节交互调试器已启动")
        print(" 使用格式: [关节名或索引] [目标弧度]")
        print(" 例如: Left_Knee_Pitch -0.5  或  10 -0.5")
        print(" 输入 'list' 查看所有关节及其当前值")
        print(" 输入 'exit' 退出并切回 prepare 模式")
        print("=" * 60)

        while True:
            try:
                line = input("\n请输入指令 > ").strip()
                if not line:
                    continue

                parts = line.lower().split()
                cmd_type = parts[0]

                if cmd_type in ["exit", "quit"]:
                    break
                elif cmd_type == "list":
                    print("\n当前全量关节状态:")
                    for idx, name in enumerate(joint_names):
                        cur_p = cmd_cache[name].position
                        print(
                            f"[{idx:2d}] {name:25s} | Pos: {cur_p:8.4f} | KP: {cmd_cache[name].kp:5.1f}"
                        )
                    continue

                if len(parts) != 2:
                    print("格式错误。用法: [名称/索引] [角度]")
                    continue

                # 匹配关节
                target_name = None
                if cmd_type.isdigit():
                    idx = int(cmd_type)
                    if 0 <= idx < num_joints:
                        target_name = joint_names[idx]
                else:
                    target_name = next(
                        (n for n in joint_names if n.lower() == cmd_type), None
                    )

                if not target_name:
                    print(f"未找到关节: {parts[0]}")
                    continue

                # 更新角度
                target_pos = float(parts[1])
                cmd_cache[target_name].position = target_pos

                # 下发全量指令（填充未修改的关节）
                robot.set_joints(list(cmd_cache.values()))
                print(f"✅ 已发送: {target_name} -> {target_pos:.4f}")

            except ValueError:
                print("角度必须为有效数字")
            except Exception as e:
                print(f"操作失败: {e}")

    except KeyboardInterrupt:
        logger.info("\n检测到用户中断")
    except Exception as e:
        logger.error(f"运行异常: {e}")
    finally:
        # 7. 安全机制：切回 prepare 模式保持站立支撑
        logger.info("切换回 prepare 模式保持站立支撑")
        try:
            robot.set_mode("prepare")
        except Exception as e:
            logger.error(f"安全模式设置失败: {e}")


if __name__ == "__main__":
    run_joint_control_demo()
