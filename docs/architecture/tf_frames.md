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

## 사과 pose 규약

- 메시지: `geometry_msgs/msg/PoseStamped`
- `header.frame_id`: `world`
- position: 사과 중심
- orientation: MVP에서는 월드 좌표축과 동일
- 다중 사과 단계에서 ID를 도입한다.

## 시간

- Isaac Sim이 `/clock`을 발행한다.
- 모든 ROS 2 노드는 `use_sim_time:=true`를 사용한다.
- 동적 TF와 센서 메시지는 현재 simulation time을 사용한다.
- 일시정지 시 검사, 이송 및 시뮬레이션 timeout도 정지한다.
- 네트워크 노드 생존 확인은 필요 시 wall time watchdog을 별도로 사용한다.

