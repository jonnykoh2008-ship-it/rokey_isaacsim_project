# 3차 개발: 멀티로봇·레일 및 시스템 통합

## 목표

하나의 Isaac Sim world에서 컨베이어 양쪽의 M0617 두 대가 각각 담당 나무 한
그루에서 사과를 수확하고, 공용 컨베이어에 투입한 뒤 검사·분류까지 하나의
연속 파이프라인으로 통합한다.

이번 단계의 기본 작업 매핑은 다음과 같다.

```text
robot_01 ↔ tree_01 ↔ conveyor place station 01
robot_02 ↔ tree_02 ↔ conveyor place station 02
```

- 각 로봇은 자신의 나무만 담당한다.
- 한 로봇이 다른 나무의 사과를 수확하거나 두 로봇이 한 나무를 공동 수확하는
  시나리오는 이번 단계의 범위에서 제외한다.
- 두 로봇은 각자의 수확 구간에서 병렬 동작할 수 있다.
- 두 로봇이 공유하는 자원은 컨베이어 투입 구간, 컨베이어 위 사과 흐름 및
  후속 품질 검사다.
- 로봇 간 협조 planning은 수확 구간의 기본 요구사항이 아니다. 다만 전체
  Isaac Sim PhysX safety monitor는 두 로봇과 공용 설비를 모두 감시한다.

현재 저장된 USD의 구체적인 자산 매핑은 다음과 같다.

| robot ID | 로봇 Prim | 초기 관절 자세 (deg) | 담당 수확 자산 | 인식 카메라 |
|---|---|---|---|---|
| `robot_01` | `/World/Xform_01/m0617_01` | `[0, 0, -90, 0, 90, 0]` | `/World/Xform/tree`, `/World/Xform/apple_branch[_1/_2]` | `/World/base_rsd455_01` |
| `robot_02` | `/World/Xform_02/m0617_02` | `[0, 0, 90, 0, -90, 0]` | `/World/Xform_03/tree`, `/World/Xform_03/apple_branch[_1/_2]` | `/World/base_rsd455_02` |

각 사과의 fixed joint는 해당 `apple_branch_xx` 내부에 위치하며
`branchbody → applebody`를 연결한다. GPU PC 1은 이 구조를 실행 시 검증한다.
각 로봇의 Articulation root는 해당 `m0617_rail/root_joint`이고, M0617 본체는
본체 Prim 내부 `FixedJoint`로 rail mount에 연결된다.

## 배치 및 레일

- `robot_01`과 `robot_02`를 공용 컨베이어의 서로 반대편에 배치한다.
- 각 로봇의 base, camera, gripper 및 관절 상태는 고유한 robot namespace와
  TF frame을 사용한다.
- 레일을 사용하는 경우 각 로봇은 자신의 레일/base 이동 상태를 갖는다.
  동적 TF는 로봇별로 분리된 `odom → base_link` 체계로 확장한다.
- 레일 이동은 담당 나무의 작업영역 안에서만 수행한다. 다른 나무로 이동해
  작업을 넘기는 cross-tree reassignment는 사용하지 않는다.
- 하나의 Isaac Sim이 두 로봇, 두 나무, 컨베이어, 센서, `/clock` 및 PhysX를
  단일 권위로 관리한다.

## 다중 로봇·객체 동작

### 로봇별 수확

- 각 로봇은 자신의 카메라와 target 입력으로 담당 나무의 사과 대기열을
  관리한다.
- `robot_01`과 `robot_02`의 target queue, 현재 Goal, retry 기록 및 safety
  상태는 서로 분리한다.
- 각 로봇 내부에서는 기존 수확 순서와 접촉 후 안전 정지 규칙을 유지한다.
- 수확 target은 `tree_id`와 전역적으로 유일한 `apple_id` 또는 `target_id`로
  품질 검사까지 연결한다. 최종 ID 필드와 문자열 규칙은 공통 인터페이스에서
  확정한다.

### 컨베이어 투입 조정

수확은 병렬로 허용하되, 컨베이어 투입은 `Conveyor Place Coordinator`를 통해
조정한다.

```text
HARVEST_COMPLETE
  → PLACE_REQUEST(robot_id, apple_id)
  → place station·시간·사과 간격 예약
  → 충돌 및 컨베이어 점유 확인
  → 해당 로봇 PLACE / RELEASE
  → 사과 안착·checkpoint 확인
  → 예약 해제
```

- 초기 통합 시험에서는 Place 구간을 한 번에 한 로봇만 사용하는 lock을
  기본으로 한다.
- 좌우 Place station의 로봇 swept volume과 투입된 사과의 이동 경로가
  충분히 분리된 것이 검증되면 두 Place를 병렬화할 수 있다.
- 두 로봇의 팔이 서로 닿지 않더라도 사과 간 충돌, 정체, 추월 및 투입 순서
  변경은 별도로 검사한다.
- 로봇별 수확시간, 컨베이어 점유시간, 품질 결과 생성시간을 사용해 최소
  투입 시간 간격과 중심 간격을 산정한다.

## 실행 구조 및 권위

GPU PC 1에는 다음 논리 계층을 둔다.

```text
Isaac Sim world
  ├─ robot_01 controller / planner / RobotMotion / safety
  ├─ robot_02 controller / planner / RobotMotion / safety
  ├─ global planning-scene publisher
  ├─ Conveyor Place Coordinator
  └─ global safety monitor
```

- 로봇별 controller는 동일한 수확 로직을 robot configuration으로 분리해
  실행한다.
- 각 planner는 담당 로봇의 현재 관절 상태와 담당 나무의 obstacle proxy를
  사용한다.
- GPU PC 1의 Fleet Supervisor는 작업 재할당보다 로봇별 실행 상태, Place
  lock, 컨베이어 투입 순서 및 전체 reset을 조정하는 역할을 우선한다.
- 로봇별 안전 정지와 전체 안전 정지를 구분한다. 한 로봇의 수확 실패는 해당
  로봇을 정지시키고 다른 로봇은 계속할 수 있지만, 컨베이어 jam, world reset,
  `/clock` 장애 또는 전체 PhysX 안전 문제는 두 로봇을 함께 정지시킨다.

## 시스템 통합

- **GPU PC 1**: 두 로봇·두 나무·공용 컨베이어를 포함한 Isaac Sim, 단일
  `/clock`, robot별 TF와 센서, planning scene, Lula RRT/trajectory/RMPflow,
  RobotMotion 실행, Place Coordinator, PhysX safety monitor 및 계획
  visualization을 담당한다.
- **개인 PC 1**: 로봇별 RGB-D 영상을 수신해 담당 나무의 사과 target을 만들고
  robot별 target namespace로 발행한다. 로봇별 계획 결과는 RViz에서 구분해
  표시한다. 개인 PC 1은 최종 경로를 승인하거나 로봇을 직접 구동하지 않는다.
- **GPU PC 2**: 공용 컨베이어 영상을 수신해 ROI/tracker, 대표 프레임 선택,
  품질 추론 및 전역 apple ID 기준 결과 통합을 수행한다.
- **개인 PC 2**: 두 로봇의 수확 상태, Place lock, 컨베이어 상태, 품질 결과,
  retry 및 알람을 한 화면에서 표시하는 운영 관제와 분류 제어를 담당한다.
- **ROS 2 Jazzy/Fast DDS**: 모든 PC가 동일 domain, RMW 및 interface version을
  사용한다. 하나의 Isaac Sim을 사용하므로 `/clock`과 global `SimulationState`는
  하나만 발행한다.

관제 명령의 경로는 다음과 같이 유지한다.

```text
개인 PC 2 운영 화면
  → GPU PC 1 Fleet Supervisor
  → robot_01/robot_02 controller 또는 Place Coordinator
```

개인 PC 2가 RobotMotion goal이나 joint waypoint를 직접 보내지 않는다. 최종
안전 정지와 실행 승인 권위는 GPU PC 1에 둔다.

## 식별자·인터페이스 요구사항

- TF, camera, joint state, motion action 및 motion status는 robot별 namespace로
  분리한다.
- 수확부터 품질·checkpoint까지 동일한 전역 사과 식별자를 사용한다. 최소한
  `tree_id`, `apple_id`, `robot_id`, `reset_id`와 현재 target/task 식별 관계를
  추적할 수 있어야 한다.
- `PlanningScene`은 두 robot pose와 두 tree obstacle을 일관되게 참조해야
  한다. 로봇별 snapshot을 사용할 경우 동일한 global `scene_version`으로
  동기화한다.
- 정확한 메시지 필드, topic/action/service 이름, QoS 및 namespace 표기는
  `docs/architecture/ros2_interfaces.md`와 함께 확정한다.

## 복구

- **robot별 수확 실패**: 실패한 로봇의 active target과 retry 정책만 처리하고,
  다른 로봇의 대기열은 유지한다.
- **Place 충돌 위험 또는 Place 실패**: 해당 로봇의 동작을 정지하고 Place
  reservation을 유지한 채 원인을 기록한다. 다른 로봇의 진행 여부는 global
  safety monitor가 판단한다.
- **ID 유실·변경**: 해당 사과의 수확·품질 lifecycle을 확정하지 않고 재검사
  또는 미분류 상태로 보낸다.
- **품질 결과 timeout**: 해당 전역 apple ID에 `TIMEOUT`을 기록하고 컨베이어
  분류 정책에 따른다.
- **컨베이어 jam 또는 사과 간 충돌**: 신규 Place를 차단하고 두 로봇의
  conveyor 접근을 정지한다. 수확 중인 로봇을 계속 운전할 수 있는 조건은
  별도 안전 시험으로 확정한다.
- **노드·네트워크 장애**: stale target을 재사용하지 않는다. target 입력,
  Place 승인 또는 품질 결과 연결이 끊기면 해당 단계의 실행을 중지한다.
- **Timeline Stop/Reset**: 두 로봇의 active Goal, Place reservation, target
  queue 및 lifecycle cache를 폐기하고 global `reset_id`를 갱신한다.
- RViz 장애는 표시만 중단하며 GPU PC 1의 실행 승인과 safety monitor는 계속
  독립적으로 동작한다.

## 통합 검증 시나리오

1. 두 로봇이 서로 다른 나무의 사과를 동시에 수확한다.
2. 한 로봇이 Place 중일 때 다른 로봇의 Place 요청이 올바르게 대기 또는
   거절된다.
3. 두 Place station을 병렬로 사용할 수 있는지 swept volume과 PhysX contact
   report로 검증한다.
4. 한 로봇의 수확 실패가 다른 로봇의 정상 수확을 불필요하게 중단하지 않는지
   확인한다.
5. 두 로봇의 사과가 공용 컨베이어에서 전역 ID로 품질 결과와 연결되는지
   확인한다.
6. reset, 네트워크 단절, ID 유실, 품질 timeout 및 컨베이어 jam을 시험한다.
7. robot별 수확시간 P95, Place 대기시간, 컨베이어 throughput, 품질 latency,
   target/message loss 및 visualization latency를 측정한다.

## TBD 정리

| 구분 | TBD 항목 | 확정 기준 또는 담당 |
|---|---|---|
| 배치 | 두 robot/tree의 정확한 world pose, 컨베이어 양쪽 Place station pose, 레일 사용 여부와 rail limit | GPU PC 1 자산·배치 시험 |
| ID | `robot_id`, `tree_id`, `apple_id`, `target_id`/`task_id`의 필드와 전역 문자열 규칙 | 네 PC 공동 interface 승인 |
| ROS | robot별 namespace, topic/action/service 이름, QoS, `PlanningScene` global/per-robot 표현 | `ros2_interfaces.md`와 연동해 확정 |
| Target | 카메라별 target 입력 방식과 담당 나무 판정, stale age, confidence/depth/TF threshold | 개인 PC 1·GPU PC 1 통합 시험 |
| Place | Place lock/lease 계약, reservation timeout, 안착 확인 방법, Place 실패 후 재시작 조건 | GPU PC 1 안전 시험 |
| 충돌 | 두 Place station의 swept-volume 최소 여유, 로봇-로봇 및 로봇-컨베이어 접촉 판정 | GPU PC 1 PhysX 시험 |
| 병렬성 | 초기 단일 Place lock 유지 여부와 좌우 Place 병렬 허용 조건 | 충돌·사과 간격 시험 후 결정 |
| 컨베이어 | 최소 투입 시간 간격, 최소 중심 간격, buffer 용량, jam/추월 처리 및 checkpoint debounce | GPU PC 1·GPU PC 2 통합 시험 |
| 장애 격리 | robot별 fault가 다른 로봇에 미치는 영향, conveyor fault의 전체 정지 조건 | safety review 후 확정 |
| 관제 | Fleet Supervisor의 high-level command, operator 권한, 알람 acknowledgement 및 이력 보존 | 개인 PC 2·GPU PC 1 운영 설계 |
| 성능 | robot별 수확시간 P95, Place 대기시간, 전체 throughput, target-to-plan 및 품질 latency 목표 | 통합 측정 후 확정 |
| 복구 | ID 유실, 네트워크 단절, Place 실패, jam, reset 이후 재개/폐기 정책 | 연속 운용 시험 후 확정 |
| 완료 기준 | 멀티로봇 연속 운용 시간, 허용 message loss, 충돌 0건 및 품질 연결 성공률 | 통합 검증 결과와 사용자 승인 |

위 항목은 통합 시험 전까지 `TBD`로 유지하며, 임시 시험값을 정식 요구사항으로
승격하지 않는다.
