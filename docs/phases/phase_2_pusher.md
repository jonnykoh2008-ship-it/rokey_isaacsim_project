# 2차 개발: 푸셔 분류

## 목표

MVP의 컨베이어 3 뒤에 푸셔 전용 컨베이어 4를 추가하고, prismatic joint 기반 푸셔 3개로 `QualityResult`에 따라 사과를 물리적으로 분류한다.

## 구성

- 푸셔 수: 3개
- 컨베이어 4: 길이 0.5m 평벨트. 추가 후 전체 라인은 4개 모듈, 총 2.0m다.
- 위치 1: 컨베이어 4 진입점에서 0.10m, 상
- 위치 2: 진입점에서 0.25m, 중
- 위치 3: 진입점에서 0.40m, 하
- 작동 방식: 직선 운동 prismatic joint
- 사과: rigid body + collider
- 푸셔: collider 적용

## 작동 조건

다음 조건이 모두 맞을 때만 작동한다.

- `apple_id`
- 품질 등급
- 선택된 `pusher_id`
- 해당 푸셔 위치 trigger
- 푸셔 원점 복귀 확인
- 동일 trigger 체류 중 중복 동작이 아닌 신규 동작 요청

컨베이어 4 진입 trigger의 simulation time과 고정 속도로 예상 도착 시각을 계산하고, 푸셔 위치 trigger에서 최종 존재를 확인한다.

구현 전에는 stroke, 전진·복귀 속도, 최대 force, plate 크기, home position tolerance, trigger 크기와 debounce 시간, 푸셔별 최소 동작 간격을 확정해야 한다. 분류 방향의 exit trigger로 사과가 실제 분류 영역에 진입했는지 확인하고, 체류 중 중복 동작과 jam을 별도 상태로 판정한다.

## 상태 흐름

```text
WAITING
  → ARMED
  → APPLE_CONFIRMED
  → EXTENDING
  → PUSH_CONFIRMED
  → RETRACTING
  → HOME_CONFIRMED
  → COMPLETED
```

- 원점 복귀가 확인되기 전에는 다음 사과의 푸셔 동작을 허용하지 않는다.
- 미분류, `RECHECK`, timeout 및 놓친 사과는 라인 끝으로 통과시킨다.
- 상자 용량과 상자 교체는 구현하지 않는다.
- 시뮬레이션 로직 timeout은 `/clock`을 사용하고, 네트워크 노드 장애 감지는 wall time으로 분리한다.

## 통신

- 개인 PC 2가 `QualityResult`를 받아 푸셔를 선택한다.
- `SortCommand`를 GPU PC 1의 Isaac Sim으로 보낸다.
- GPU PC 1이 trigger와 명령을 검증한 후 joint를 구동한다.
- 수확 target, Lula RRT 계획 및 로봇 Action은 GPU PC 1의 수확 supervisor가
  담당하며 푸셔 명령과 별도의 상태 머신으로 유지한다.
- 개인 PC 1의 RViz는 GPU PC 1이 발행하는 수확·푸셔 상태 visualization을
  원격 표시할 수 있으나 푸셔 동작을 승인하지 않는다.

### SortCommand 계약

```text
Service: /conveyor/sort_command
Type: appleproj_interfaces/srv/SortCommand

Topic: /conveyor/sort_status
Type: appleproj_interfaces/msg/SortStatus
QoS: Reliable, Transient Local, Keep Last 10
```

등급·푸셔·checkpoint 매핑은 다음으로 고정한다.

| 등급 | 푸셔 | trigger checkpoint |
|---|---|---|
| `HIGH` | `PUSHER_1` | `CONVEYOR_4_PUSHER_1_TRIGGER` |
| `MEDIUM` | `PUSHER_2` | `CONVEYOR_4_PUSHER_2_TRIGGER` |
| `LOW` | `PUSHER_3` | `CONVEYOR_4_PUSHER_3_TRIGGER` |

GPU PC 1은 `/conveyor/checkpoint_events`에도 같은 checkpoint 이름을 발행한다.
서비스의 `accepted=true`는 명령 접수 완료이며 푸셔 작동 완료를 뜻하지 않는다.
상세 request/response, 중복 처리, 상태 흐름, 오류 코드 및 reset 규칙은
`docs/architecture/ros2_interfaces.md`의 `SortCommand`와 `SortStatus` 계약을 따른다.

## 미확정 사항

푸셔의 stroke, 전진·복귀 속도, 가속도, 최대 force, plate 크기와 home position tolerance는 사과의 질량·속도 및 컨베이어 폭을 반영한 동역학 시험 후 확정한다. 각 trigger의 크기·debounce·위치, 푸셔별 최소 동작 간격과 세 번째 푸셔에서 컨베이어 4 출구까지의 안전거리도 레이아웃 검증 전까지 TBD로 둔다. 푸셔 실패·jam·ID mismatch 복구, 다중 사과 queue, `RECHECK` 사과의 보관 방식, exit trigger 판정 기준, 완료 기준과 반복 시험 횟수는 통합 시험 계획과 함께 결정한다.
