from __future__ import annotations

import logging
import time

from boosteros.robots.booster import BoosterRobot
from boosteros.types import JointCommand

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("UpperBodyDebugger")


def run_upper_body_control_demo():
    """Interactive upper-body joint debugging example.

    Takes over arms and head in walk mode and supports dynamic pose adjustment.
    """
    # 1. 初始化机器人客户端
    try:
        robot = BoosterRobot()
        logger.info("机器人连接就绪")
    except Exception as e:
        logger.error(f"无法初始化机器人客户端: {e}")
        return

    upper_body_enabled = False

    try:
        # 2. 模式准备
        # 上身自定义控制只能在 walk 模式下启用
        logger.info("正在切换到 walk 模式...")
        robot.set_mode("walk")

        # 3. 获取上身 10 关节名称 (Head + Arms)
        joint_names = [joint.name for joint in robot.list_joints()]
        upper_names = joint_names[:10]

        # 获取当前实时位姿作为接管起点
        current_state = robot.get_joint_states()
        state_map = {js.name: js.position for js in current_state.joints}

        # 4. 准备控制参数（上身优化增益：低刚度、高阻尼）
        # TODO: Replace these example gains with firmware-provided recommended
        # Booster K1/T1 gain tables once the lower-level control team publishes
        # validated per-joint kp/kd values.
        kp_upper = [40.0, 40.0, 20.0, 30.0, 10.0, 10.0, 20.0, 30.0, 10.0, 10.0]
        kd_upper = [2.0, 2.0, 1.5, 2.0, 0.5, 0.5, 1.5, 2.0, 0.5, 0.5]

        # 构造并初始化缓存
        cmd_cache: dict[str, JointCommand] = {}
        for i, name in enumerate(upper_names):
            pos = state_map.get(name, 0.0)
            cmd_cache[name] = JointCommand(
                name=name, position=pos, kp=kp_upper[i], kd=kd_upper[i]
            )

        # 5. 开启上身自定义控制权限并立即锁存位姿
        # 此操作会使双臂脱离自动摆动逻辑，交由用户接管
        logger.info("开启上身自定义控制使能...")
        robot.upper_body_control(True)
        upper_body_enabled = True

        # 上身控制模式要等待5秒才能起效，再下发控制指令
        time.sleep(5)

        robot.set_joints(list(cmd_cache.values()))
        logger.info("已成功接管上身控制。")

        # 6. 交互式调试循环
        print("\n" + "=" * 60)
        print(" 上身关节交互调试器 (索引 0-9)")
        print(" 使用格式: [名称或索引] [目标弧度]")
        print(" 例如: Left_Elbow_Pitch -0.5  或  4 -0.5")
        print(" 输入 'list' 查看上身状态, 输入 'exit' 退出")
        print("=" * 60)

        while True:
            try:
                line = input("\n[UpperBody] 请输入指令 > ").strip()
                if not line:
                    continue

                parts = line.lower().split()
                cmd_type = parts[0]

                if cmd_type in ["exit", "quit"]:
                    break
                elif cmd_type == "list":
                    print("\n当前上身关节状态:")
                    for idx, name in enumerate(upper_names):
                        cur_p = cmd_cache[name].position
                        print(f"[{idx:d}] {name:25s} | Pos: {cur_p:8.4f}")
                    continue

                if len(parts) != 2:
                    print("格式错误。用法: [名称/索引] [角度]")
                    continue

                # 匹配关节
                target_name = None
                if cmd_type.isdigit():
                    idx = int(cmd_type)
                    if 0 <= idx < 10:
                        target_name = upper_names[idx]
                else:
                    target_name = next(
                        (n for n in upper_names if n.lower() == cmd_type), None
                    )

                if not target_name:
                    print(f"未找到对应的上身关节: {parts[0]}")
                    continue

                # 更新缓存并下发
                target_pos = float(parts[1])
                cmd_cache[target_name].position = target_pos

                # 下发前 10 个关节指令
                robot.set_joints(list(cmd_cache.values()))
                print(f"✅ 已发送: {target_name} -> {target_pos:.4f}")

            except ValueError:
                print("角度值必须为有效数字")
            except Exception as e:
                print(f"操作失败: {e}")

    except KeyboardInterrupt:
        logger.info("\n检测到用户中断")
    except Exception as e:
        logger.error(f"运行异常: {e}")
    finally:
        # 7. 安全清理：务必关闭上身控制，否则手臂将无法恢复行走摆动
        if upper_body_enabled:
            logger.info("正在关闭上身自定义控制，恢复手臂自动摆动姿态...")
            try:
                robot.upper_body_control(False)
            except Exception as e:
                logger.error(f"关闭上身控制失败: {e}")

        logger.info("流程结束")


if __name__ == "__main__":
    run_upper_body_control_demo()
