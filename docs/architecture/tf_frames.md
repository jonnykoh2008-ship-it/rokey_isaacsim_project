# TF 및 시뮬레이션 시간

## TF 발행

- `world → odom`: GPU PC 1이 static identity transform으로 발행한다.
- `odom → base_link`: GPU PC 1이 Isaac Sim transform으로 `/tf`에 발행한다.
  MVP에서는 고정값이지만, 3차 레일 도입 시 동적 변환으로 확장한다.
- `base_link → robot links`: GPU PC 1의 Isaac Sim
  `ROS2PublishTransformTree`가 `/tf`에 발행한다.
  `robot_state_publisher`는 사용하지 않아 중복 TF를 방지한다.
- 카메라 고정 TF: Isaac Sim Action Graph가 `/tf_static`으로 발행한다.
- 동일한 TF를 두 노드가 중복 발행하지 않는다.

## 좌표계

- `world`
- `odom`
- `base_link` (`robot_base`의 표준 ROS 링크 프레임)
- M0617의 각 joint/link frame
- `palm` (USD 그리퍼 palm 링크. 물리 수확 TCP의 기준 frame)
- `gripper_frame`
- `base_camera`
- `arm_camera`
- `tree_<id>`
- `apple_<id>`
- `conveyor_<id>`

<<<<<<< Updated upstream
=======
## TF 발행

GPU PC 1의 `vision_apple_pick.py`가 Isaac Sim Action Graph로 모두 발행하며,
timestamp는 `/clock` simulation time을 사용한다.

- `world → odom`: 항등 변환, `/tf_static`
- `odom → base_link`: USD 조립 자세에서 읽은 고정 변환, `/tf_static`
- `base_link → robot links`: articulation 상태 기반 동적 변환, `/tf`
- `/joint_states`: M0617 articulation 관절 상태
- 카메라 고정 TF: `world → base_camera`, `/tf_static`
- 동일한 TF를 두 노드가 중복 발행하지 않는다. `robot_state_publisher`는
  사용하지 않는다.

M0617이 고정 설치된 MVP에서는 `odom → base_link`가 변하지 않는다. 3차 레일 도입 시 동적 변환으로 확장한다.

### 레일 링크를 TF에서 제외하는 이유

레일(`m0617_rail`)은 M0617과 같은 articulation이지만 TF 대상에서 제외한다.
레일 URDF의 베이스 링크 이름이 `world`여서 ROS의 `world` 프레임과 충돌하기
때문이다. 이 prim은 `Assets/Robot_Rail/` 참조 에셋에서 들어오고
articulation root joint와 `rail_joint`가 경로로 참조하고 있어 rename할 수
없다. 따라서 Action Graph는 `/World/Xform_01/m0617` 아래 rigid body 링크만
대상으로 지정한다. MVP에서 레일은 고정이므로 TF에서 빠져도 무방하며, 3차
레일 도입 시 이 제약을 다시 설계한다.

>>>>>>> Stashed changes
## 수확 TCP와 Lula 제어 프레임

- 물리 수확 TCP는 USD `palm` 원점에서 palm 로컬 `+Y` 방향 `0.0908 m`에
  위치한다. 이 값은 palm collision mesh 앞면 `0.0508 m`과 명목 사과 반지름
  `0.040 m`의 합이며 접촉 여유를 포함하지 않는다.
- GPU PC 1은 Isaac Sim 동적 TF에 `palm` frame을 발행한다. 개인 PC 1은
  `world → palm`을 조회한 뒤 palm 로컬 `+Y` offset을 적용해 TCP pose를
  계산한다.
- Lula IK와 RMPflow의 제어 frame은 URDF `link_6`를 사용한다. GPU PC 1은
  외부 TCP 목표를 `link_6` 제어 목표로 변환한다.
- URDF의 보조 `gripper_frame`을 TCP 목표로 직접 사용하지 않는다. USD 조립
  자세와 보조 frame의 RPY가 다르면 실제 TCP와 Lula 목표가 서로 다른 위치에
  수렴할 수 있기 때문이다.
- `palm` TF를 조회할 수 없으면 개인 PC 1은 로봇을 움직이지 않고
  `TF_UNAVAILABLE`로 실패한다.

## 사과 pose 규약

- 메시지: `geometry_msgs/msg/PoseStamped`
- `header.frame_id`: `world`
- position: 사과 중심
- orientation: MVP에서는 월드 좌표축과 동일
- 다중 사과 단계에서 ID를 도입한다.

## 분산 planning scene 좌표계

- `/planning_scene`의 `header.frame_id`, 모든 obstacle pose,
  `robot_base_pose`, `robot_tcp_pose`는 `world`를 사용한다.
- `RobotMotion`의 `target_pose`와 `waypoints`도 모두 `world`를 사용한다.
- 개인 PC 1은 frame이 다르거나 `reset_id/scene_version`이 현재 simulation
  상태와 다른 scene 및 waypoint를 사용하지 않는다.
- GPU PC 1은 외부 waypoint를 물리 TCP 목표로 해석한 뒤 `link_6` 제어 목표로
  변환한다.

## 시간

- Isaac Sim이 `/clock`을 발행한다.
- 모든 ROS 2 노드는 `use_sim_time:=true`를 사용한다.
- 동적 TF와 센서 메시지는 현재 simulation time을 사용한다.
- 일시정지 시 검사, 이송 및 시뮬레이션 timeout도 정지한다.
- 네트워크 노드 생존 확인은 필요 시 wall time watchdog을 별도로 사용한다.
