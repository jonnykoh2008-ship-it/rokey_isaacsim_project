# TF 및 시뮬레이션 시간

## 기준

모든 PC는 ROS 2 Jazzy/Fast DDS와 Isaac Sim 5.1.0을 사용하고
`use_sim_time:=true`를 설정한다. TF의 권위자는 GPU PC 1의 Isaac Sim이다.
개인 PC 1은 영상 timestamp에 맞는 TF를 조회해 사과 좌표를 계산하지만 TF를
재발행하지 않는다. 동일한 TF를 두 노드가 중복 발행하지 않는다.

## TF 발행

GPU PC 1의 Isaac Sim Action Graph가 다음을 발행한다.

- `world → odom`: MVP 항등 변환, `/tf_static`
- `odom → base_link`: MVP 고정 설치 자세, `/tf_static`; 3차 레일에서 동적
  변환으로 확장
- `base_link → robot links`: 선택한 로봇 articulation 상태 기반 동적 변환, `/tf`
- `base_link → palm` 및 그리퍼 링크: articulation 상태 기반 동적 변환, `/tf`
- 고정 카메라 TF: `/tf_static`
- 카메라가 이동하는 경우 해당 articulation 상태 기반 TF: `/tf`
- `/joint_states`: M0617 articulation 관절 상태

`robot_state_publisher`는 사용하지 않는다. 현재 USD 멀티로봇 실행은
`m0617_rail/root_joint`를 Articulation root로 사용하고, TF link 범위는 각
`m0617_01`·`m0617_02` 본체와 그리퍼로 제한한다. 로봇별 `odom → base_link`
frame과 최종 ROS namespace는 통합 계약에서 `TBD`다.

## 좌표계

- `world`
- `odom`
- `base_link` (`robot_base`의 표준 ROS 링크 프레임)
- M0617의 각 joint/link frame
- `palm` (USD 그리퍼 palm 링크. 물리 수확 TCP의 기준 frame)
- `gripper_frame`
- `base_camera` (v2.0 호환 이름)
- `arm_camera`
- `base_rsd455_01` (robot_01의 USD camera 이름)
- `base_rsd455_02` (robot_02의 USD camera 이름)
- `quality_camera_top_optical_frame`
- `quality_camera_left_optical_frame`
- `quality_camera_right_optical_frame`
- `conveyor_inspection_roi`
- `tree_<id>`
- `apple_<id>`
- `conveyor_<id>`

컨베이어 2의 품질검사 카메라는 3대이며 각각 고유한 optical frame을 가진다. 세
frame 모두 `world`를 부모로 `/tf_static`에 발행한다. 하나의 `InspectionImage`는
한 카메라에서 나오므로 그 메시지의 여섯 header는 모두 같은 optical frame을
사용한다. GPU PC 2는 세 frame 중 하나가 아니면 프레임을 거부한다.

`conveyor_inspection_roi`는 검사 ROI 자체의 frame이다. ROI 이탈은 카메라 사건이
아니라 컨베이어의 물리 사건이므로 `InspectionCompleted`는 카메라 optical frame이
아니라 이 frame을 사용한다.

영상 target의 최종 `header.frame_id`는 `world`다. 개인 PC 1은 원본
camera-frame 검출점과 촬영 timestamp를 보존한 뒤, 해당 timestamp에 가장 가까운
TF로 `world` 변환을 수행한다. 허용 시간 차이와 보간 정책은 `TBD`다.

멀티로봇 USD 매핑은 `robot_01 → /World/base_rsd455_01` 및
`robot_02 → /World/base_rsd455_02`다. 카메라의 ROS frame/topic namespace를
USD Prim 이름과 동일하게 확정할지는 `TBD`이며, GPU PC 1 코드는 현재 선택한
camera Prim의 월드 pose를 사용한다.

## 수확 TCP와 Lula 제어 프레임

- 물리 수확 TCP는 USD `palm` 원점에서 palm 로컬 `+Y` 방향 `0.0908 m`에
  위치한다. 이 값은 palm collision mesh 앞면 `0.0508 m`과 명목 사과 반지름
  `0.040 m`의 합이며 접촉 여유를 포함하지 않는다.
- GPU PC 1은 동적 TF의 `palm` frame과 `/joint_states`를 사용해 현재 물리
  TCP pose를 계산한다.
- 개인 PC 1은 `world → palm`을 조회해 로봇을 제어하지 않는다. 개인 PC 1은
  영상 timestamp 기준의 target pose 계산에만 TF를 사용한다.
- Lula IK/RRT/RMPflow의 제어 frame은 URDF `link_6`를 사용한다. GPU PC 1은
  외부 target/TCP 목표를 `link_6` 제어 목표로 변환한다.
- URDF의 보조 `gripper_frame`을 TCP 목표로 직접 사용하지 않는다. USD 조립
  자세와 보조 frame의 RPY가 다르면 실제 TCP와 Lula 목표가 서로 다른 위치에
  수렴할 수 있기 때문이다.
- 개인 PC 1에서 카메라 target 변환에 필요한 TF를 조회할 수 없으면 target을
  발행하지 않고 `TF_UNAVAILABLE` 상태를 기록한다.
- GPU PC 1에서 실행에 필요한 `palm`, `base_link`, `link_6` TF가 없으면
  RobotMotion을 실행하지 않고 `TF_UNAVAILABLE`로 실패한다.

## 사과 pose 규약

- v2.0 입력: 개인 PC 1이 RGB-D에서 계산한 target 메시지 (`TBD`)
- 최종 `header.frame_id`: `world`
- position: 사과 중심
- orientation: 개인 PC 1은 발행하지 않는다. GPU PC 1이 현재 로봇 상태와 planning
  scene을 기준으로 접근 orientation과 pre-grasp pose를 결정한다. MVP 기본 접근은
  world `+Z` 방향이며, 다른 접근 방향 탐색 정책은 해당 planner가 관리한다.
- 다중 사과 단계에서 ID와 target 세대를 포함한다.

## 분산 planning 및 시각화 좌표계

- `/planning_scene`의 `header.frame_id`, 모든 obstacle pose,
  `robot_base_pose`, `robot_tcp_pose`는 `world`를 사용한다.
- GPU PC 1 내부 Lula RRT의 시작/목표 configuration과 모든 계획 pose는
  `world` 기준 target에서 생성한다.
- GPU PC 1이 발행하는 RViz `MarkerArray`, `Path` 및 상태 시각화의 frame도
  `world`를 기본으로 한다.
- 개인 PC 1은 frame이 다르거나 target의 `reset_id`가 현재 simulation 상태와
  다른 target을 사용하지 않는다.
- GPU PC 1은 외부 target을 물리 TCP 목표로 해석한 뒤 `link_6` 제어 목표로
  변환하고, RRT/trajectory/RMPflow에 동일한 planning scene을 적용한다.

## 시간

- Isaac Sim이 `/clock`을 발행한다.
- 모든 ROS 2 노드는 `use_sim_time:=true`를 사용한다.
- 동적 TF, 센서 메시지, target timestamp 및 계획 상태는 simulation time을
  사용한다.
- 일시정지 시 검사, 이송 및 시뮬레이션 timeout도 정지한다.
- 네트워크 노드 생존 확인은 필요 시 wall time watchdog을 별도로 사용한다.
- 영상 timestamp와 TF timestamp의 허용 차이, clock jump 처리 및 stale target
  수명은 통합 시험 전까지 `TBD`다.
