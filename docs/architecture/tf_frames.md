# TF 및 시뮬레이션 시간

## 좌표계

- `world`
- `odom`
- `base_link` (`robot_base`의 표준 ROS 링크 프레임)
- M0617의 각 joint/link frame
- `gripper_frame`
- `base_camera`
- `arm_camera`
- `tree_<id>`
- `apple_<id>`
- `conveyor_<id>`

## TF 발행

- `odom → base_link`: Isaac Sim ROS 2 Bridge의 Odometry Publisher
- `base_link → robot links`: `robot_state_publisher`, `/joint_states` 기반
- 카메라 고정 TF: Isaac Sim Action Graph
- 동일한 TF를 두 노드가 중복 발행하지 않는다.

M0617이 고정 설치된 MVP에서는 `odom → base_link`가 변하지 않는다. 3차 레일 도입 시 동적 변환으로 확장한다.

## 수확 TCP와 Lula 제어 프레임

- 물리 수확 TCP는 USD `palm` 원점에서 palm 로컬 `+Y` 방향 `0.093 m`에
  위치한다. 이 값은 palm collision mesh 앞면 `0.0508 m`, 명목 사과 반지름
  `0.040 m`, 접촉 여유 `0.0022 m`를 합한 포위 파지 중심이다.
- Lula IK와 RMPflow의 제어 frame은 URDF `link_6`를 사용한다.
- 원하는 TCP pose는 실행 시 USD에서 읽은 `link_6 → palm` 고정변환과 위 TCP
  offset을 사용해 `link_6` 목표 pose로 변환한다.
- URDF의 보조 `gripper_frame`을 TCP 목표로 직접 사용하지 않는다. USD 조립
  자세와 보조 frame의 RPY가 다르면 실제 TCP와 Lula 목표가 서로 다른 위치에
  수렴할 수 있기 때문이다.
- 시작 시 `link_6 → palm` translation을 로그로 출력하며, 이 변환을 얻지
  못하면 로봇을 움직이지 않고 실패한다.

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
