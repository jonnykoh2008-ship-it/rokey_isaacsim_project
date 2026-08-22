"""GPU PC 1용 통합 Isaac Sim 수확 서버.

카메라 발행과 M0617 제어는 반드시 같은 Isaac Sim World에서 실행해야 한다.
이 파일은 기존 ``apple_pick.py``의 검증된 물리·IK 함수를 재사용하고,
``/harvest/robot_motion`` Action Goal 단위로 동작을 나눈다.

실행 전 ``APPLEPROJ_INTERFACES_PREFIX``에는 Isaac Python 3.11로 빌드한
appleproj_interfaces의 install prefix를 지정해야 한다.
"""

import os
import queue
import sys
import threading
from dataclasses import dataclass
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
BRIDGE_ROOT = Path("/home/rokey/isaacsim/exts/isaacsim.ros2.bridge/jazzy")
INTERFACE_PREFIX_TEXT = os.environ.get("APPLEPROJ_INTERFACES_PREFIX", "")
INTERFACE_PREFIX = Path(INTERFACE_PREFIX_TEXT) if INTERFACE_PREFIX_TEXT else None
os.environ.setdefault("ROS_DOMAIN_ID", "102")


def prepare_isaac_ros_environment():
    """Isaac Python 3.11용 rclpy와 custom Action을 import할 환경을 만든다."""
    if INTERFACE_PREFIX is None or not INTERFACE_PREFIX.is_dir():
        raise RuntimeError(
            "APPLEPROJ_INTERFACES_PREFIX에 Isaac Python 3.11용 "
            "appleproj_interfaces install 경로를 지정하세요."
        )
    python_path = INTERFACE_PREFIX / "lib/python3.11/site-packages"
    required_paths = [BRIDGE_ROOT / "lib", INTERFACE_PREFIX / "lib"]
    current = [p for p in os.environ.get("LD_LIBRARY_PATH", "").split(":") if p]
    missing = [str(p) for p in required_paths if str(p) not in current]
    if missing and os.environ.get("VISION_PICK_ENV_READY") != "1":
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = ":".join([*missing, *current])
        env["VISION_PICK_ENV_READY"] = "1"
        os.execve(sys.executable, [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]], env)
    sys.path[:0] = [str(BRIDGE_ROOT / "rclpy"), str(python_path)]


prepare_isaac_ros_environment()

# import 시 SimulationApp을 한 번만 생성하며 main()은 실행하지 않는다.
import apple_pick as harvest
import omni.graph.core as og
import rclpy
import usdrt.Sdf
from appleproj_interfaces.action import RobotMotion
from isaacsim.core.utils.extensions import enable_extension
from pxr import Usd, UsdGeom
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node


MOTION_SEQUENCE = [
    RobotMotion.Goal.APPROACH,
    RobotMotion.Goal.GRASP,
    RobotMotion.Goal.TWIST,
    RobotMotion.Goal.PULL,
    RobotMotion.Goal.TRANSPORT,
    RobotMotion.Goal.PLACE,
    RobotMotion.Goal.RETRACT,
]
STOP_STATE = {
    RobotMotion.Goal.GRASP: "TWIST",
    RobotMotion.Goal.TWIST: "PULL",
    RobotMotion.Goal.PULL: "RETREAT",
    RobotMotion.Goal.TRANSPORT: "RELEASE",
    RobotMotion.Goal.PLACE: "LIFT",
    RobotMotion.Goal.RETRACT: "DONE",
}

CAMERA_PATH = "/World/base_rsd455/RSD455/Camera_OmniVision_OV9782_Color"
CAMERA_GRAPH_PATH = "/BaseCameraRosGraph"


def _multiply_xyzw(a, b):
    x1, y1, z1, w1 = a
    x2, y2, z2, w2 = b
    value = harvest.np.array([
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
    ])
    return value / harvest.np.linalg.norm(value)


def create_base_camera_graph(stage):
    """같은 Isaac World에서 RGB-D, CameraInfo, clock과 고정 TF를 발행한다."""
    camera = harvest.require_prim(stage, CAMERA_PATH)
    if not camera.IsA(UsdGeom.Camera):
        raise RuntimeError(f"Color Camera Prim이 아닙니다: {CAMERA_PATH}")
    if stage.GetPrimAtPath(CAMERA_GRAPH_PATH).IsValid():
        raise RuntimeError(f"카메라 ROS 그래프가 이미 존재합니다: {CAMERA_GRAPH_PATH}")
    enable_extension("isaacsim.ros2.bridge")
    harvest.simulation_app.update()
    matrix = UsdGeom.XformCache().GetLocalToWorldTransform(camera)
    position = list(matrix.ExtractTranslation())
    q = matrix.ExtractRotationQuat()
    i = q.GetImaginary()
    rotation = _multiply_xyzw(
        [float(i[0]), float(i[1]), float(i[2]), float(q.GetReal())],
        [1.0, 0.0, 0.0, 0.0],
    ).tolist()
    k = og.Controller.Keys
    with Usd.EditContext(stage, stage.GetSessionLayer()):
        og.Controller.edit(
            {"graph_path": CAMERA_GRAPH_PATH, "evaluator_name": "execution",
             "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION},
            {
                k.CREATE_NODES: [
                    ("Tick", "omni.graph.action.OnPlaybackTick"),
                    ("Time", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                    ("Clock", "isaacsim.ros2.bridge.ROS2PublishClock"),
                    ("Render", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
                    ("Rgb", "isaacsim.ros2.bridge.ROS2CameraHelper"),
                    ("Depth", "isaacsim.ros2.bridge.ROS2CameraHelper"),
                    ("Info", "isaacsim.ros2.bridge.ROS2CameraInfoHelper"),
                    ("Tf", "isaacsim.ros2.bridge.ROS2PublishRawTransformTree"),
                ],
                k.CONNECT: [
                    ("Tick.outputs:tick", "Clock.inputs:execIn"),
                    ("Time.outputs:simulationTime", "Clock.inputs:timeStamp"),
                    ("Tick.outputs:tick", "Render.inputs:execIn"),
                    ("Render.outputs:execOut", "Rgb.inputs:execIn"),
                    ("Render.outputs:execOut", "Depth.inputs:execIn"),
                    ("Render.outputs:execOut", "Info.inputs:execIn"),
                    ("Render.outputs:renderProductPath", "Rgb.inputs:renderProductPath"),
                    ("Render.outputs:renderProductPath", "Depth.inputs:renderProductPath"),
                    ("Render.outputs:renderProductPath", "Info.inputs:renderProductPath"),
                    ("Tick.outputs:tick", "Tf.inputs:execIn"),
                    ("Time.outputs:simulationTime", "Tf.inputs:timeStamp"),
                ],
                k.SET_VALUES: [
                    ("Render.inputs:cameraPrim", [usdrt.Sdf.Path(CAMERA_PATH)]),
                    ("Render.inputs:width", 1280), ("Render.inputs:height", 720),
                    ("Rgb.inputs:frameId", "base_camera"),
                    ("Rgb.inputs:topicName", "/base_camera/color/image_raw"),
                    ("Rgb.inputs:type", "rgb"), ("Rgb.inputs:frameSkipCount", 1),
                    ("Depth.inputs:frameId", "base_camera"),
                    ("Depth.inputs:topicName", "/base_camera/depth/image_raw"),
                    ("Depth.inputs:type", "depth"), ("Depth.inputs:frameSkipCount", 1),
                    ("Info.inputs:frameId", "base_camera"),
                    ("Info.inputs:topicName", "/base_camera/camera_info"),
                    ("Info.inputs:frameSkipCount", 1),
                    ("Tf.inputs:topicName", "/tf_static"),
                    ("Tf.inputs:parentFrameId", "world"),
                    ("Tf.inputs:childFrameId", "base_camera"),
                    ("Tf.inputs:staticPublisher", True),
                    ("Tf.inputs:translation", position), ("Tf.inputs:rotation", rotation),
                ],
            },
        )


@dataclass
class PendingGoal:
    handle: object
    finished: threading.Event
    result: object = None


class RobotMotionNode(Node):
    """ROS callback에서는 요청만 보관하고 Isaac API는 메인 스레드만 사용한다."""

    def __init__(self):
        super().__init__("isaac_robot_motion_server")
        self.requests = queue.Queue(maxsize=1)
        self.busy = False
        self.lock = threading.Lock()
        self.server = ActionServer(
            self,
            RobotMotion,
            "/harvest/robot_motion",
            execute_callback=self.execute,
            goal_callback=self.accept_goal,
            cancel_callback=lambda _goal: CancelResponse.ACCEPT,
        )

    def accept_goal(self, request):
        with self.lock:
            if self.busy or request.motion_type not in MOTION_SEQUENCE:
                return GoalResponse.REJECT
            self.busy = True
        return GoalResponse.ACCEPT

    def execute(self, goal_handle):
        pending = PendingGoal(goal_handle, threading.Event())
        self.requests.put(pending)
        pending.finished.wait()
        with self.lock:
            self.busy = False
        return pending.result


class MotionEngine:
    """기존 FSM을 Action 단계 경계에서 정지시키는 메인 스레드 실행기."""

    def __init__(self, world, robot, stage):
        self.world, self.robot, self.stage = world, robot, stage
        self.ik, self.lula = harvest.create_ik_solver(robot, stage)
        self.gripper_indices = [robot.get_dof_index(n) for n in harvest.GRIPPER_JOINTS]
        self.link_t, self.link_r = harvest.compute_link6_to_palm(stage)
        robot_position, _ = harvest.get_prim_world_pose(stage, harvest.ROBOT_BASE_PATH)
        _, apple_size = harvest.compute_apple_center(stage)
        self.conveyor = harvest.compute_conveyor_start(stage, robot_position, apple_size)
        self.expected_index = 0
        self.fsm = None

    @staticmethod
    def result(success, code="", message=""):
        value = RobotMotion.Result()
        value.success, value.error_code, value.message = success, code, message
        return value

    def feedback(self, handle, state, progress):
        value = RobotMotion.Feedback()
        value.current_state, value.progress = state, float(progress)
        handle.publish_feedback(value)

    def execute(self, handle):
        request = handle.request
        if request.motion_type != MOTION_SEQUENCE[self.expected_index]:
            handle.abort()
            return self.result(False, "INVALID_SEQUENCE", "Action 단계 순서가 잘못되었습니다.")
        if request.target_pose.header.frame_id != "world":
            handle.abort()
            return self.result(False, "INVALID_FRAME", "target_pose frame_id는 world여야 합니다.")
        try:
            if request.motion_type == RobotMotion.Goal.APPROACH:
                self._approach(handle, request.target_pose)
            else:
                self._run_fsm(handle, STOP_STATE[request.motion_type])
        except Exception as error:
            handle.abort()
            return self.result(False, "MOTION_FAILED", str(error))
        if handle.is_cancel_requested:
            handle.canceled()
            return self.result(False, "CANCELED", "사용자가 동작을 취소했습니다.")
        self.expected_index += 1
        handle.succeed()
        return self.result(True, "", "동작 완료")

    def _approach(self, handle, pose):
        apple = pose.pose.position
        center = harvest.np.array([apple.x, apple.y, apple.z], dtype=float)
        if not harvest.np.all(harvest.np.isfinite(center)):
            raise RuntimeError("사과 좌표에 NaN 또는 Inf가 있습니다.")
        robot_position, _ = harvest.get_prim_world_pose(self.stage, harvest.ROBOT_BASE_PATH)
        rotation, direction = harvest.make_approach_rotation(robot_position, center)
        pregrasp = center - direction * harvest.PREGRASP_DISTANCE_M
        planned = harvest.AppleHarvestFSM(
            pregrasp, rotation, center, rotation, direction, *self.conveyor,
            start_at_pregrasp=True,
        )
        initial = harvest.np.asarray(self.ik.get_joints_subset().get_joint_positions())
        if not harvest.validate_planned_ik(
            planned, self.lula, initial, pregrasp, rotation, self.link_t, self.link_r
        ):
            raise RuntimeError("비전 목표의 전체 수확 경로 IK 검사에 실패했습니다.")
        self.feedback(handle, "APPROACH", 0.1)
        _steps, complete = harvest.move_arm_to_pregrasp(
            self.world, self.robot, self.ik, self.gripper_indices,
            pregrasp, rotation, self.link_t, self.link_r, 0,
        )
        if not complete:
            raise RuntimeError("pregrasp 이동을 완료하지 못했습니다.")
        tcp, palm_rotation = harvest.current_tcp_pose(self.robot)
        self.fsm = harvest.AppleHarvestFSM(
            tcp, palm_rotation, center, rotation, direction, *self.conveyor,
            start_at_pregrasp=True,
        )
        self.feedback(handle, "APPROACH", 1.0)

    def _run_fsm(self, handle, stop_state):
        if self.fsm is None:
            raise RuntimeError("APPROACH가 먼저 완료되지 않았습니다.")
        failures = 0
        while not self.fsm.done and self.fsm.NAMES[self.fsm.state] != stop_state:
            if handle.is_cancel_requested:
                return
            target, rotation, grip = self.fsm.sample()
            link_position, link_orientation = harvest.tcp_target_to_link6(
                target, rotation, self.link_t, self.link_r
            )
            action, solved = self.ik.compute_inverse_kinematics(
                target_position=link_position,
                target_orientation=link_orientation,
                position_tolerance=0.003,
                orientation_tolerance=harvest.np.deg2rad(3.0),
            )
            if solved:
                self.robot.apply_action(action)
                failures = 0
                actual, actual_rotation = harvest.current_tcp_pose(self.robot)
                if self.fsm.advance(actual, actual_rotation) == "timeout":
                    raise RuntimeError("TCP가 목표를 제한 시간 안에 추종하지 못했습니다.")
            else:
                failures += 1
                if failures >= harvest.MAX_CONSECUTIVE_IK_FAILURES:
                    raise RuntimeError("IK가 연속 실패했습니다.")
            harvest.apply_gripper_target(self.robot, self.gripper_indices, grip)
            state = self.fsm.NAMES[min(self.fsm.state, len(self.fsm.NAMES) - 1)]
            self.feedback(handle, state, 0.5)
            self.world.step(render=not harvest.args.headless)
        self.feedback(handle, stop_state, 1.0)


def main():
    stage = harvest.open_project_stage()
    create_base_camera_graph(stage)
    harvest.configure_breakable_joint(stage)
    harvest.configure_contact_colliders(stage)
    harvest.configure_joint_drives(stage)
    world = harvest.World(
        stage_units_in_meters=1.0, physics_prim_path="/physicsScene",
        physics_dt=1.0 / 60.0, rendering_dt=1.0 / 60.0,
    )
    robot = harvest.create_robot(world)
    engine = MotionEngine(world, robot, stage)
    rclpy.init()
    node = RobotMotionNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()
    world.play()
    try:
        while harvest.simulation_app.is_running():
            try:
                pending = node.requests.get_nowait()
            except queue.Empty:
                world.step(render=not harvest.args.headless)
                continue
            pending.result = engine.execute(pending.handle)
            pending.finished.set()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()
        world.stop()
        harvest.simulation_app.close()


if __name__ == "__main__":
    main()
