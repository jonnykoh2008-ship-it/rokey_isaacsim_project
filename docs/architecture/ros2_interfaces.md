# ROS 2 인터페이스

이 문서는 노드 간 데이터 계약의 기준이다.

## 공통 규칙

- custom interface 패키지는 `appleproj_interfaces`를 사용한다.
- 모든 header timestamp는 `/clock` 기준이다.
- 모든 ROS 2 노드는 `use_sim_time:=true`를 사용한다.
- `apple_id`와 `inspection_id`는 한 처리 주기 동안 변경하지 않는다.
- 센서 스트림에는 Sensor Data QoS를 기본 후보로 사용한다.
- 상태·결과 메시지는 신뢰성 우선 QoS를 사용한다. 정확한 QoS는 TBD다.
- v2.0에서 영상의 송신·센서 권위자는 GPU PC 1이고, 영상 수신·사과 3D 좌표
  계산·target 발행 주체는 개인 PC 1이다.
- `/harvest/target`은 개인 PC 1에서 GPU PC 1으로 전달하는 수확 전용 target
  계약이며, `/harvest/perception_status`는 target 생성 전후의 인식 상태 계약이다.
- v2.0에서 경로 계획·궤적 생성·로봇 실행의 권위자는 GPU PC 1이다. 개인 PC 1은
  최종 waypoint를 발행하지 않는다.

## 인터페이스 목록

| 종류 | 이름 | 타입 | 송신/서버 | 수신/클라이언트 |
|---|---|---|---|---|
| Topic | `/base_camera/color/image_raw` | `sensor_msgs/msg/Image` (raw) | GPU PC 1 | 개인 PC 1 |
| Topic | `/base_camera/depth/image_raw` | `sensor_msgs/msg/Image` (raw) | GPU PC 1 | 개인 PC 1 |
| Topic | `/base_camera/camera_info` | `sensor_msgs/msg/CameraInfo` | GPU PC 1 | 개인 PC 1 |
| Topic | `/harvest/target` | `appleproj_interfaces/msg/HarvestTarget` | 개인 PC 1 | GPU PC 1 |
| Topic | `/harvest/perception_status` | `appleproj_interfaces/msg/HarvestPerceptionStatus` | 개인 PC 1 | GPU PC 1·모니터링 |
| Topic | `/simulation/state` | `appleproj_interfaces/msg/SimulationState` | GPU PC 1 | 개인 PC 1 |
| Topic | `/planning_scene` | `appleproj_interfaces/msg/PlanningScene` | GPU PC 1 | 개인 PC 1 |
| Service | `/planning_scene/get_snapshot` | `appleproj_interfaces/srv/GetPlanningScene` | GPU PC 1 | 개인 PC 1 (debug/RViz) |
| Action | `/harvest/robot_motion` | `appleproj_interfaces/action/RobotMotion` | GPU PC 1 | GPU PC 1 내부 supervisor |
| Topic | `/harvest/motion_status` | `appleproj_interfaces/msg/MotionStatus` | GPU PC 1 | 개인 PC 1·개인 PC 2 |
| Topic | `/harvest/planning_markers` | `visualization_msgs/msg/MarkerArray` (`TBD`) | GPU PC 1 | 개인 PC 1 RViz |
| Topic | `/harvest/planned_path` | `nav_msgs/msg/Path` (`TBD`) | GPU PC 1 | 개인 PC 1 RViz |
| Topic | 컨베이어 raw RGB/depth/CameraInfo 토픽 (`TBD`) | `sensor_msgs/msg/Image`, `sensor_msgs/msg/CameraInfo` | GPU PC 1 | GPU PC 2 |
| Topic | `/quality/results` | `appleproj_interfaces/msg/QualityResult` | GPU PC 2 | 개인 PC 2 |
| Service | `/quality/retry_inspection` | `appleproj_interfaces/srv/RetryInspection` | GPU PC 1 | 개인 PC 2 |
| Topic | `/conveyor/checkpoint_events` | `appleproj_interfaces/msg/CheckpointEvent` | GPU PC 1 | 개인 PC 2 |

Action과 Service 표에서 서버는 요청을 실행하는 쪽이고 클라이언트는 요청을 보내는 쪽이다.

## 공통 표준 인터페이스

| 토픽 | 타입 | 의미 |
|---|---|---|
| `/clock` | `rosgraph_msgs/msg/Clock` | Isaac Sim simulation time |
| `/joint_states` | `sensor_msgs/msg/JointState` | 로봇 관절 상태 |
| `/tf` | `tf2_msgs/msg/TFMessage` | 동적 TF |
| `/tf_static` | `tf2_msgs/msg/TFMessage` | 고정 TF |

## 사과 목표

```text
토픽: /harvest/target
타입: appleproj_interfaces/msg/HarvestTarget
송신: 개인 PC 1
수신: GPU PC 1
QoS: Reliable, Volatile, Keep Last 10
frame_id: world
```

동일 토픽에 여러 `target_id`가 연속 발행되므로 publisher와 subscriber 모두
위 QoS를 사용한다.

필드:

- `header`: RGB-D 촬영 시각, `/clock` 기준, `frame_id=world`
- `target_id`: 동일 `reset_id` 내 수확 대상 식별자
- `reset_id`, `scene_version`: 개인 PC 1이 마지막으로 확인한 SimulationState 세대
- `position`: world 좌표계 사과 중심
- `source_point`: world 변환 전 카메라 좌표 검출점
- `confidence`: 0.0~1.0 검출 신뢰도
- `valid_depth_ratio`: 검출 영역 내 유효 depth 픽셀 비율
- `tf_time_error_sec`: 영상 timestamp와 사용 TF timestamp의 절대 차이

GPU PC 1은 다음 조건을 모두 확인한 뒤 target을 계획에 사용한다.

- `SimulationState`가 `READY` 또는 `PLAYING`
- `header.frame_id == "world"`
- target timestamp가 stale하지 않음
- 현재 `reset_id`, `scene_version`과 일치
- confidence, valid depth ratio, TF 시간 오차가 각 threshold를 만족

confidence·depth·TF 시간 threshold 값은 `TBD`다. 개인 PC 1은 orientation과
pre-grasp pose를 발행하지 않으며, GPU PC 1이 현재 로봇 상태와 planning scene을
기준으로 계산한다. 동일 `(reset_id, target_id)`에서는 최신 timestamp만 사용하고,
Action 실행이 시작된 target의 후속 갱신은 새 Goal로 실행하지 않는다. 실패한 target은
`/harvest/motion_status`로 거부 사유를 반환한다. `/harvest/target`에는 Transient
Local을 사용하지 않는다.

GPU PC 1은 아직 시작하지 않은 target을 ID별 대기열에 보관하고 robot base에서
가까운 순서로 실행한다. 접촉 전 첫 실패는 일반 대기열 뒤의 재시도 대기열로
이동하며 다른 target을 모두 처리한 뒤 1회만 재시도한다. 접촉 이후 실패는 다음
Goal을 보내지 않고 안전 정지한다. 이 정책은 메시지 필드를 추가하지 않으며 모든
lifecycle key는 `(reset_id, target_id)`를 사용한다.

## HarvestPerceptionStatus

```text
토픽: /harvest/perception_status
타입: appleproj_interfaces/msg/HarvestPerceptionStatus
송신: 개인 PC 1
수신: GPU PC 1·모니터링 노드
QoS: Reliable, Volatile, Keep Last 10
```

`status` 값은 `OK`, `NO_DETECTION`, `DEPTH_INVALID`, `TF_UNAVAILABLE`,
`STALE_FRAME`, `LOW_CONFIDENCE`, `RESET_MISMATCH`, `SIMULATION_NOT_READY`,
`INPUT_NOT_SYNCHRONIZED`, `INTERNAL_ERROR` 중 하나다. target 생성 전 실패한 경우
`target_id`는 빈 문자열이며, 계산할 수 없는 수치 필드는 NaN으로 채운다. `header`는
검사 대상 RGB-D 프레임의 촬영 시각과 원본 카메라 frame을 사용한다.

## SimulationState

GPU PC 1이 `/clock`만으로 구별할 수 없는 Timeline 상태와 scene 세대를
명시적으로 전달한다.

```text
토픽: /simulation/state
타입: appleproj_interfaces/msg/SimulationState
QoS: Reliable, Transient Local, Keep Last 1
```

필드:

- `header`: `/clock` 기준 시각, `frame_id=world`
- `state`: `STOPPED`, `INITIALIZING`, `READY`, `PLAYING`, `PAUSED`
- `reset_id`: Timeline Stop 후 물리 재초기화마다 증가
- `scene_version`: 새 obstacle snapshot마다 증가
- `message`: 상태 전환 원인

GPU PC 1은 `READY` 또는 `PLAYING`에서만 target을 계획·실행한다. `STOPPED` 또는
`INITIALIZING`을 받으면 실행 Goal, RRT tree 및 trajectory를 폐기하고 개인 PC 1에
새 target 발행을 중지하도록 알린다. `PAUSED`는 새 계획과 Goal 전송을 금지하되
현재 실행 문맥은 재개 가능하도록 유지한다. 개인 PC 1은 `READY/PLAYING`이 아니면
영상 검출을 계속할 수 있지만 target을 발행하지 않는다.

## PlanningScene 및 ObstacleProxy

```text
토픽: /planning_scene
타입: appleproj_interfaces/msg/PlanningScene
QoS: Reliable, Transient Local, Keep Last 1
```

`PlanningScene` 필드:

- `header`: snapshot 생성 simulation time, `frame_id=world`
- `reset_id`, `scene_version`
- `robot_base_pose`: 계획 시점 M0617 base pose
- `robot_tcp_pose`: 계획 시작점의 물리 수확 TCP pose
- `obstacles`: 전체 정적 나무 proxy 배열

`ObstacleProxy` 필드:

- `obstacle_id`
- `shape`: `SHAPE_SPHERE`, `SHAPE_BOX`, `SHAPE_CAPSULE`
- `obstacle_class`: `CLASS_TRUNK`, `CLASS_BRANCH`
- `pose`: world 기준 proxy 중심과 자세
- `dimensions`: box는 전체 XYZ 크기, sphere는 X에 반지름, capsule은 X에
  반지름과 Y에 중심선 길이
- `safety_margin`: 형상 크기와 별도로 적용할 최소 안전거리

MVP snapshot은 몸통 box와 가지 sphere만 사용한다. 잎은 포함하지 않는다.
snapshot에는 안전거리가 적용되기 전 형상 크기와 `safety_margin`을 넣는다. GPU
PC 1의 RRT와 RMPflow가 동일한 safety margin을 적용한다. 개인 PC 1은 이를
시각화할 뿐 실행용 obstacle을 재구성하지 않는다.

개인 PC 1은 snapshot을 RViz 표시 또는 디버그 검증에 사용할 수 있다. snapshot을
받지 못했거나 version 누락을 감지하면 `/planning_scene/get_snapshot`을 호출할 수
있다. 성공 응답에는 최신 전체 `PlanningScene` 한 개가 포함된다. 경로 계획과
안전거리 적용의 최종 권위자는 GPU PC 1이며, 개인 PC 1의 snapshot 처리는 실행
admission에 영향을 주지 않는다.

## InspectionImage

현재 OpenCV 크기 단일 단계 A는 저장된 RGB 파일을 직접 처리하므로
`InspectionImage`를 사용하지 않는다. 단계 A 합격 후 GPU PC 2가 컨베이어 raw
스트림에서 후보 프레임을 수집하고 대표 프레임을 선택해 RGB-D 직경 측정에
전달할 때 이 메시지를 사용한다. GPU PC 2 내부 토픽 이름/QoS와 별도 cross-PC
발행 여부는 `TBD`다.

필드:

- `header`: `/clock` 기준 촬영 시각과 카메라 frame
- `inspection_id`: 한 번의 품질검사 식별자
- `apple_id`: 검사 대상 사과 식별자
- `frame_index`: 해당 검사에서의 프레임 번호
- `total_frames`: 해당 검사에서 전송할 전체 대표 프레임 수
- `image`: 압축 RGB 이미지
- `apple_mask`: lossless mono8 PNG 사과 mask
- `ignore_mask`: lossless mono8 PNG 평가 제외 mask. 크기 단일 MVP에서는
  직경 계산에 사용하지 않지만 후속 착색·손상 확장을 위해 유지한다.
- `aligned_depth`: RGB에 정렬된 16UC1 millimetre compressedDepth PNG
- `camera_info`: 해당 raw 프레임과 동일한 CameraInfo

모든 구성요소의 timestamp와 frame_id는 동일해야 한다.

## QualityResult

GPU PC 2가 이미지별 크기 측정과 사과 단위 통합을 완료한 뒤 개인 PC 2로
전달한다. 현재 MVP 등급은 `diameter_mm`만 사용한다.

```text
토픽: /quality/results
타입: appleproj_interfaces/msg/QualityResult
```

필드:

- `header`: `/clock` 기준 메시지 생성 시각
- `inspection_id`
- `apple_id`
- `grade`: `HIGH`, `MEDIUM`, `LOW`
- `confidence`
- `color_ratio`
- `diameter_mm`
- `damage_area_cm2`
- `frames_used`
- `frame_indices`
- `result_timestamp`
- `status`: `VALID`, `RECHECK`, `UNCLASSIFIED`, `TIMEOUT`, `LATE_RESULT`, `ID_MISMATCH`, `INSUFFICIENT_VIEWS`

현재 크기 단일 MVP에서 `color_ratio`와 `damage_area_cm2`는 NaN이다.
화면 검증용 픽셀 직경은 `diameter_mm`에 넣지 않는다. 단계 A의 파일 기반
OpenCV 도구는 ROS 결과를 발행하지 않고 오버레이 이미지와 CSV만 생성한다.

카메라 ROI 이탈 후 simulation time 0.5초를 결과 deadline으로 사용한다. deadline까지 결과가 없으면 `TIMEOUT`, 이후 도착한 결과는 `LATE_RESULT`로 기록한다. 컨베이어 2의 tracker ID와 컨베이어 3 checkpoint의 rigid body prim이 일치하지 않으면 `ID_MISMATCH`로 처리한다.

## CheckpointEvent

GPU PC 1의 Isaac Sim 컨베이어 I/O 상태를 개인 PC 2로 전달한다.

```text
토픽: /conveyor/checkpoint_events
타입: appleproj_interfaces/msg/CheckpointEvent
```

필드:

- `header`: `/clock` 기준 I/O 발생 시각과 checkpoint frame
- `apple_id`: checkpoint를 통과한 사과
- `checkpoint_id`: 컨베이어 I/O 지점 식별자
- `event`: `ENTER` 또는 `EXIT`

카메라 ROI는 품질검사 프레임 수집의 시작과 종료를 판단한다. CheckpointEvent는 컨베이어 진입·이탈 시각, 점유시간 및 공정 상태 전환 검증에 사용하며 프레임 선택에는 직접 사용하지 않는다.

## RobotMotion

GPU PC 1의 수확 supervisor가 planner와 executor를 연결하는 내부 Action으로
사용한다. v2.0에서 개인 PC 1은 RobotMotion Goal을 보내지 않고 `/harvest/target`
만 발행한다.

```text
액션: /harvest/robot_motion
타입: appleproj_interfaces/action/RobotMotion
```

Goal:

- `motion_type`: `APPROACH`, `GRASP`, `TWIST`, `PULL`, `TRANSPORT`, `PLACE`, `RETRACT`, `RELEASE`
- `target_pose`: 동작 목표 pose
- `reset_id`, `scene_version`: GPU PC 1이 계획에 사용한 planning scene 세대
- `waypoints`: GPU PC 1의 Lula RRT/trajectory 단계가 생성한 내부 world 기준
  TCP waypoint 배열. 외부 PC가 주입하지 않는다.
- planner seed 및 재계획 정책은 구현 파라미터로 두고 정식 인터페이스에는
  노출하지 않는 것을 기본으로 한다 (`TBD`).

Result:

- `success`
- `error_code`
- `message`

Feedback:

- `current_state`
- `progress`: `0.0`에서 `1.0` 범위의 단계 진행률

각 모션 단계는 별도 Goal로 실행할 수 있다. 단계 순서, RRT 재계획 및 실패
복구는 GPU PC 1의 수확 supervisor가 관리한다. GPU PC 1은 target과 scene 세대가
현재 값과 다르거나 내부 RRT/trajectory 검증이 끝나지 않으면 Goal을 실행하지
않는다. Goal 승인 후 scene 세대가 바뀌면 `SCENE_MISMATCH`, 실제 로봇-나무
접촉이 발생하면 `UNEXPECTED_CONTACT`로 중단한다.

### 모션 의미

- `GRASP`: Goal을 보내는 시점의 현재 pose를 `target_pose`에 채우고, 해당 pose를 유지하며 그리퍼만 폐합한다.
- `PULL`: 당김 동작과 stem joint 분리 확인을 포함한다. stem이 분리되지 않으면 성공으로 판정하지 않는다.
- `PLACE`: 목표 pose까지 이동만 수행하고 그리퍼를 개방하지 않는다.
- `RELEASE`: Goal을 보내는 시점의 현재 pose를 `target_pose`에 채우고, 해당 pose를 유지하며 그리퍼만 개방한다.

### 실행 규칙

- 각 단계에서 유의미한 TCP 위치 또는 자세 진전이 `/clock`
  기준 simulation time 3초 동안 없으면 timeout으로 판정한다.
  Timeline Pause 중에는 이 watchdog도 정지한다.
- Action을 실행하는 동안에는 새 Goal을 거부하고 cancel만 허용한다.
- cancel, timeout, 충돌 또는 모션 실패가 발생하면 GPU PC 1의 Action Server는 로봇 동작을 즉시 멈추고 실패 Result를 반환한다.
- 실패 후 자동 후퇴는 수행하지 않는다.
- 성공 Result의 `error_code`는 빈 문자열이다.

### MotionStatus

GPU PC 1이 target 수신, RRT 계획, trajectory 변환, RMPflow 실행 및 PhysX 안전
감시 결과를 개인 PC 1과 개인 PC 2에 전달한다. 개인 PC 1의 인식 실패는 별도의
target 상태 계약(`TBD`)으로 전달한다.

```text
토픽: /harvest/motion_status
타입: appleproj_interfaces/msg/MotionStatus
송신: GPU PC 1
수신: 개인 PC 1·개인 PC 2
```

필드:

- `header`: `/clock` 기준 상태 발생 시각
- `current_state`: 수확 상태 머신의 현재 상태
- `success`: 상태 또는 계획 성공 여부
- `progress`: `0.0`에서 `1.0` 범위
- `error_code`: 기존 300번대 오류 코드 문자열. 성공 시 빈 문자열
- `message`: 사람이 읽을 수 있는 상세 설명

GPU PC 1은 `IK_FAILED`, `APPROACH_UNREACHABLE`, `COLLISION_RISK`,
`SINGULARITY_RISK`, `INVALID_TARGET_POSE`, `TF_UNAVAILABLE`,
`JOINT_STATE_UNAVAILABLE`, `SCENE_MISMATCH`, `UNEXPECTED_CONTACT` 등의 실패가
발생하면 `success=false`와 기존 오류 코드를 발행한다. 개인 PC 1은 이 메시지를
RViz 또는 모니터링에 사용한다. Goal admission은 현재 `SimulationState`, target의
`reset_id`, `scene_version`, timestamp, busy 상태 및 내부 계획 검증으로 판정한다.

이 토픽은 상태·결과 전달용으로 Reliable QoS를 사용하며, 기본 history depth는 10으로
한다. 상태 메시지의 timestamp는 simulation time을 사용한다.

### 오류 코드

| 코드 | `error_code` |
|---:|---|
| 300 | `IK_FAILED` |
| 301 | `APPROACH_UNREACHABLE` |
| 302 | `COLLISION_RISK` |
| 303 | `SINGULARITY_RISK` |
| 304 | `MOTION_TIMEOUT` |
| 305 | `STEM_NOT_BROKEN` |
| 306 | `GOAL_REJECTED` |
| 307 | `CANCELLED` |
| 308 | `SIMULATION_RESET` |
| 309 | `INVALID_TARGET_POSE` |
| 310 | `TF_UNAVAILABLE` |
| 311 | `JOINT_STATE_UNAVAILABLE` |
| 312 | `INTERNAL_ERROR` |

`error_code`는 `"300:IK_FAILED"`처럼 숫자 코드와 심볼을 함께 포함하는 문자열로 전송한다.
v2.0의 RRT 실패, trajectory 변환 실패, stale target, scene mismatch 및
unexpected contact의 숫자 코드 배정은 기존 300번대 체계와 조정 후 `TBD`로 확정한다.

## Motion planning 시각화

GPU PC 1은 실행과 독립된 시각화 publisher를 제공한다. 후보 인터페이스는 다음과
같으며 최종 토픽 이름과 QoS는 `TBD`다.

| 토픽 | 타입 | 의미 |
|---|---|---|
| `/harvest/planning_markers` | `visualization_msgs/msg/MarkerArray` | target, pre-grasp, obstacle, clearance, RRT node/path, 실패 지점 |
| `/harvest/planned_path` | `nav_msgs/msg/Path` | world 기준 TCP 경로 |
| `/harvest/planned_joint_trajectory` | `trajectory_msgs/msg/JointTrajectory` | 시간 매개화된 RRT 결과 미리보기 |
| `/harvest/motion_status` | `appleproj_interfaces/msg/MotionStatus` | planning/execution 상태와 오류 |

개인 PC 1은 위 토픽을 원격으로 구독해 RViz에서 표시한다. RViz가 종료되거나
네트워크에서 시각화 토픽이 유실되어도 GPU PC 1의 planner와 safety monitor는
계속 실행할 수 있어야 한다.

## RetryInspection

개인 PC 2가 GPU PC 1에 품질검사 재시도를 요청한다.

```text
서비스: /quality/retry_inspection
타입: appleproj_interfaces/srv/RetryInspection
```

Request:

- `inspection_id`
- `apple_id`
- `reason`

Response:

- `accepted`
- `new_inspection_id`
- `message`

`accepted=false`이면 `new_inspection_id`는 빈 문자열로 반환한다.

## SortCommand

개인 PC 2에서 GPU PC 1로 전달한다. MVP에서는 사용하지 않으며, 2차 개발의 컨베이어 4 실제 푸셔 제어부터 사용한다.

필수 후보 필드:

- `apple_id`
- `grade`
- `pusher_id`
- trigger 조건 또는 목표 simulation time

토픽·서비스·액션 선택과 QoS는 TBD다.
