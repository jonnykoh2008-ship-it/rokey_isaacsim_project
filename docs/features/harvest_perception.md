# 수확용 인식

## 목적

개인 PC 1이 GPU PC 1에서 수신한 RGB-D 영상과 `CameraInfo`로 수확 대상 사과의
중심 position과 검출 메타데이터를 계산해 GPU PC 1에 전달한다. GPU PC 1의 planning
scene 및 로봇 동작, 컨베이어 품질검사는 이 문서의 범위가 아니다.

## v2.0 MVP

- 개인 PC 1은 GPU PC 1의 base camera raw RGB/depth 및 `CameraInfo`를 네트워크로
  수신한다.
- 개인 PC 1에서 OpenCV/기하 기반 검출을 수행한다. 검출 모델 사용 여부와 모델
  버전은 `TBD`다.
- depth projection으로 camera frame의 사과 중심을 계산한 뒤 TF timestamp를
  기준으로 `world` frame으로 변환한다.
- 유효 target은 사과 중심 position, 검출 timestamp, `reset_id`, confidence 및
  target ID를 포함해 GPU PC 1에 발행한다. 최종 메시지 타입과 필드는 `TBD`이며
  기존 `PoseStamped` 호환 계층을 둘 수 있다.
- 개인 PC 1은 접근 orientation을 결정하지 않는다. GPU PC 1이 현재 로봇 상태와
  planning scene을 기준으로 접근 orientation과 pre-grasp pose를 결정한다.
- 장애물 proxy의 생성·분류·안전거리 적용은 GPU PC 1이 담당한다.

## 멀티로봇 카메라 매핑

저장된 USD에서 각 로봇의 수확 인식 카메라는 다음 D455 Prim을 사용한다.

| 로봇 | 카메라 Prim | 담당 수확 영역 |
|---|---|---|
| `robot_01` | `/World/base_rsd455_01` | `/World/Xform`의 `tree`·`apple_branch[_1/_2]` |
| `robot_02` | `/World/base_rsd455_02` | `/World/Xform_03`의 `tree`·`apple_branch[_1/_2]` |

GPU PC 1의 카메라 발행 코드는 `--robot-id`로 위 Prim을 선택한다. 현재 공통
RGB-D topic 이름과 robot별 ROS namespace는 `TBD`로 유지하며, 개인 PC 1
인식 노드는 카메라별 입력·TF frame을 선택할 수 있도록 별도 modification
request를 따른다.

## v2.0 인식 흐름

```text
GPU PC 1 D455 RGB + Depth + CameraInfo + TF
  → 개인 PC 1 영상 동기화 및 사과 검출
  → depth 유효성·outlier 검사
  → camera frame 3D 중심 계산
  → timestamp에 맞는 TF로 world 변환
  → target 세대·confidence 검증
  → GPU PC 1의 planner에 전달
```

영상 timestamp와 TF timestamp의 허용 차이, depth 유효 픽셀 비율, confidence
threshold 및 재검출 정책은 통합 시험 전까지 `TBD`다. 조건을 만족하지 못한
검출은 target으로 발행하지 않고 오류 상태를 기록한다.

## 장애물 인식 및 소유권

- 굵은 가지: 로봇 전체 링크의 회피 대상
- 작은 가지: 그리퍼와 손목의 회피 대상
- 잎: visual-only로 유지하고 PhysX collision과 planning obstacle에서 모두
  제외한다. `leaf occlusion` 모델링·보정 및 잎 가림 기반 confidence 판단은
  사용하지 않는다.
- v2.0 MVP에서는 GPU PC 1이 ground-truth collider 또는 proxy로 planning scene을
  생성한다. 개인 PC 1은 장애물의 최종 판정을 하지 않는다.
- 실무 비전 단계에서 개인 PC 1이 굵은 가지 segmentation 또는 depth 기반
  obstacle 후보를 계산할 수 있지만, GPU PC 1이 수신 후 `world` 좌표·세대·안전
  거리를 검증하고 planner 입력으로 채택한다. 해당 보조 obstacle 메시지는
  `TBD`다.
- 잎은 인식·계획·물리 안전 판단의 입력으로 사용하지 않는다. 개인 PC 1은 잎
  가림을 보정하거나 잎 전용 confidence를 계산하지 않으며, GPU PC 1 planner는
  잎을 충돌 형상으로 받지 않는다.
- 개인 PC 1은 접근 방향 주변의 관측 신뢰도가 낮거나 depth가 부족한 후보를
  발행하지 않는다. free-space의 최종 판정과 대체 접근 탐색은 GPU PC 1의
  planner가 수행한다.

작은 가지의 물리 collision 사용 여부는 perception 결과를 planning obstacle에
포함할지와 독립적으로 결정한다. 잎은 PhysX, planning obstacle 및 leaf occlusion
처리에서 제외한다. MVP의 몸통·가지 obstacle은 USD visual mesh에서 생성한 ground-truth
proxy를 사용하고, D455 obstacle point cloud 전환 시에도 동일한 안전거리와
실패 규약을 유지한다.

## 다중 사과

- 같은 `reset_id`에서 최초로 모든 유효 후보가 확보된 프레임의 world 위치를
  기준으로 `apple_001`, `apple_002`, ... ID를 부여한다. ID 부여 순서는 world
  XYZ 오름차순으로 고정한다.
- 이후 프레임은 기존 track의 마지막 world 위치에서 100mm 이내인 최근접 후보만
  같은 ID로 연결한다. 이 100mm는 명목 지름 80mm 사과의 시뮬레이션용 임시값이다.
- 최초 ID 집합이 만들어진 뒤 같은 `reset_id`에서는 새 ID를 추가하지 않는다.
  따라서 수확되어 컨베이어로 이동한 사과가 새 target으로 재등록되지 않는다.
- 개인 PC 1은 한 프레임의 유효 track을 모두 `/harvest/target`으로 발행한다.
  GPU PC 1은 ID별 최신 표본을 보관하므로 발행 순서는 수확 우선순위를 결정하지
  않는다.
- GPU PC 1은 로봇 base에서 가까운 target부터 실행하고, 실행 중 수신한 다른
  target은 대기열에 저장한다.
- 같은 `reset_id`에서 target timestamp가 오래되거나 ID가 재사용되면 GPU PC 1은
  해당 target을 거부하고 개인 PC 1에 상태를 반환한다.

## 결과 계약

인식 노드는 유효한 target만 발행하고 다음 실패를 구분한다: `NO_DETECTION`,
`DEPTH_INVALID`, `TF_UNAVAILABLE`, `STALE_FRAME`, `LOW_CONFIDENCE`,
`RESET_MISMATCH`. 오류 코드의 정식 문자열과 전달 토픽은
`docs/architecture/ros2_interfaces.md`에서 관리하며 미확정 값은 `TBD`로 둔다.
