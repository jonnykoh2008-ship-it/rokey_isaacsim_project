# ROS 2 인터페이스

이 문서는 노드 간 데이터 계약의 기준이다.

## 공통 규칙

- custom interface 패키지는 `appleproj_interfaces`를 사용한다.
- 모든 header timestamp는 `/clock` 기준이다.
- 모든 ROS 2 노드는 `use_sim_time:=true`를 사용한다.
- `apple_id`와 `inspection_id`는 한 처리 주기 동안 변경하지 않는다.
- 센서 스트림에는 Sensor Data QoS를 기본 후보로 사용한다.
- 상태·결과 메시지는 신뢰성 우선 QoS를 사용한다. 정확한 QoS는 TBD다.

## 인터페이스 목록

| 종류 | 이름 | 타입 | 송신/서버 | 수신/클라이언트 |
|---|---|---|---|---|
| Topic | `/harvest/target_pose` | `geometry_msgs/msg/PoseStamped` | GPU PC 1 | 개인 PC 1 |
| Topic | `/simulation/state` | `appleproj_interfaces/msg/SimulationState` | GPU PC 1 | 개인 PC 1 |
| Topic | `/planning_scene` | `appleproj_interfaces/msg/PlanningScene` | GPU PC 1 | 개인 PC 1 |
| Service | `/planning_scene/get_snapshot` | `appleproj_interfaces/srv/GetPlanningScene` | GPU PC 1 | 개인 PC 1 |
| Action | `/harvest/robot_motion` | `appleproj_interfaces/action/RobotMotion` | GPU PC 1 | 개인 PC 1 |
| Topic | `/harvest/motion_status` | `appleproj_interfaces/msg/MotionStatus` | 개인 PC 1 | GPU PC 1 |
| Topic | `/quality/inspection_images` | `appleproj_interfaces/msg/InspectionImage` | GPU PC 1 | GPU PC 2 |
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
토픽: /harvest/target_pose
타입: geometry_msgs/msg/PoseStamped
frame_id: world
의미: 사과 중심과 접근 orientation
```

MVP에서는 Isaac Sim ground-truth pose를 사용한다. 다중 사과 단계의 ID 포함 메시지 구조는 TBD다.

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

개인 PC 1은 `READY` 또는 `PLAYING`에서만 새 계획을 시작한다. `STOPPED` 또는
`INITIALIZING`을 받으면 실행 Goal을 취소하고 이전 계획을 폐기한다. `PAUSED`는
새 계획과 Goal 전송을 금지하되 현재 실행 문맥은 재개 가능하도록 유지한다.

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
snapshot에는 안전거리가 적용되기 전 형상 크기를 넣고 개인 PC 1이
`safety_margin`을 더한다. GPU PC 1도 같은 안전거리를 독립적으로 적용한다.

개인 PC 1이 snapshot을 받지 못했거나 version 누락을 감지하면
`/planning_scene/get_snapshot`을 호출한다. 성공 응답에는 최신 전체
`PlanningScene` 한 개가 포함된다.

## InspectionImage

GPU PC 1이 컨베이어 2의 대표 검사 이미지를 GPU PC 2로 전달한다.

```text
토픽: /quality/inspection_images
타입: appleproj_interfaces/msg/InspectionImage
```

필드:

- `header`: `/clock` 기준 촬영 시각과 카메라 frame
- `inspection_id`: 한 번의 품질검사 식별자
- `apple_id`: 검사 대상 사과 식별자
- `frame_index`: 해당 검사에서의 프레임 번호
- `total_frames`: 해당 검사에서 전송할 전체 대표 프레임 수
- `image`: 압축 RGB 이미지

depth 및 `CameraInfo` 전달 여부는 TBD다.

## QualityResult

GPU PC 2가 이미지별 품질 추론과 사과 단위 통합을 완료한 뒤 개인 PC 2로 전달한다.

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

개인 PC 1이 단계별 로봇 동작 Goal을 GPU PC 1에 요청한다.

```text
액션: /harvest/robot_motion
타입: appleproj_interfaces/action/RobotMotion
```

Goal:

- `motion_type`: `APPROACH`, `GRASP`, `TWIST`, `PULL`, `TRANSPORT`, `PLACE`, `RETRACT`, `RELEASE`
- `target_pose`: 동작 목표 pose
- `reset_id`, `scene_version`: 계획에 사용한 planning scene 세대
- `waypoints`: 개인 PC 1이 계획한 world 기준 TCP waypoint 배열. MVP에서는
  `APPROACH`에 필수이며 다른 단계에서는 빈 배열이다.

Result:

- `success`
- `error_code`
- `message`

Feedback:

- `current_state`
- `progress`: `0.0`에서 `1.0` 범위의 단계 진행률

각 모션 단계는 별도 Goal로 요청한다. 단계 순서와 실패 복구는 개인 PC 1의 수확 상태 머신이 관리한다.
GPU PC 1은 scene 세대가 현재 값과 다르거나 `APPROACH.waypoints`가 비어 있으면
Goal을 거부한다. Goal 승인 후 scene 세대가 바뀌면 `SCENE_MISMATCH`, 실제
로봇-나무 접촉이 발생하면 `UNEXPECTED_CONTACT`로 중단한다.

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

개인 PC 1이 RobotMotion Goal을 보내기 전 발생한 계획·검증 결과를 GPU PC 1에 전달한다.

```text
토픽: /harvest/motion_status
타입: appleproj_interfaces/msg/MotionStatus
송신: 개인 PC 1
수신: GPU PC 1
```

필드:

- `header`: `/clock` 기준 상태 발생 시각
- `current_state`: 수확 상태 머신의 현재 상태
- `success`: 상태 또는 계획 성공 여부
- `progress`: `0.0`에서 `1.0` 범위
- `error_code`: 기존 300번대 오류 코드 문자열. 성공 시 빈 문자열
- `message`: 사람이 읽을 수 있는 상세 설명

개인 PC 1은 Goal 전 `IK_FAILED`, `APPROACH_UNREACHABLE`, `COLLISION_RISK`,
`SINGULARITY_RISK`, `INVALID_TARGET_POSE`, `TF_UNAVAILABLE`,
`JOINT_STATE_UNAVAILABLE` 등의 실패가 발생하면 `success=false`와 기존 오류 코드를
발행한다. GPU PC 1은 이 메시지를 수신하면 해당 수확 실행을 실패 상태로
기록·로그한다. `MotionStatus` 실패 기록은 RobotMotion Goal admission을
차단하지 않으며, Goal 허용은 현재 `SimulationState`, `reset_id`,
`scene_version`, busy 상태로 판정한다.

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
