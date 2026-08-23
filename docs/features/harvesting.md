# 수확 및 파지

## 구성

- 로봇: Doosan M0617
- 그리퍼: AGS-001-MTCP
- solver: LulaKinematicsSolver
- end-effector frame: `gripper_frame`

## 상태 흐름

```text
TARGET_RECEIVED
  → PRE_GRASP_PLANNING
  → SINGULARITY_CHECK
  → COLLISION_CHECK
  → APPROACH
  → GRASP
  → TWIST
  → LINEAR_PULL
  → STEM_BREAK_CHECK
  → TRANSPORT
  → PLACE_ON_CONVEYOR
  → RETRACT
```

## 접근

- MVP 기본 접근은 사과 아래에서 world `+Z` 방향으로 이동한다.
- 직전 joint configuration과 가까운 IK 해를 우선한다.
- 급격한 joint angle 변화와 singularity에 가까운 해를 제외한다.
- 굵은 가지와 로봇 전체 링크의 충돌을 방지한다.
- 기본 접근이 불가능하면 MVP에서는 `APPROACH_UNREACHABLE`로 실패한다.
- 2차부터 가지와 충돌하지 않는 다른 접근 각도를 탐색한다.

singularity 기준과 joint step 제한은 시뮬레이션 시험 후 튜닝한다. 안전거리는
아래 수확 경로 및 충돌 회피 규약을 따른다.

## 수확 경로 및 충돌 회피

- 홈 자세에서 pre-grasp까지의 transit은 단순 관절 보간을 사용하지 않고
  Lula/RMPflow의 로봇 collision sphere와 planning obstacle을 사용한다.
- M0617 전체 링크는 굵은 가지 planning proxy와 충돌하지 않아야 한다.
- 그리퍼와 손목은 작은 가지 planning proxy와 충돌하지 않아야 한다.
- 몸통 mesh가 여러 개인 경우 각 mesh를 별도 planning obstacle로 유지한다.
  로봇 collision sphere는 URDF의 관절 간 링크 구간과 collision mesh 범위를
  빠짐없이 덮어야 한다.
- 목표 사과는 transit 중 planning obstacle로 유지하고, 사과 중심에서 world
  `+Z` 반대 방향으로 `0.30 m` 떨어진 staging pose에 도달한 뒤 해제한다.
- 목표 사과 obstacle 해제 후 같은 접근축을 따라 `0.15 m` pre-grasp pose로
  이동하고, 이어서 의도된 `+Z` grasp 접근을 수행한다.
- pre-grasp → grasp → twist → pull → retract 구간에도 나무 obstacle을
  유지하며 매 simulation step에서 RMPflow world를 갱신한다.
- 작은 가지는 물리 collision이 비활성화되어도 planning obstacle에서 제외하지
  않는다. 잎은 visual-only로 유지하고 PhysX 및 RMPflow obstacle에서 제외한다.
- 경로 corridor 내부 proxy는 경로와 가까운 순서로 선별하되, 시작 TCP와 이미
  겹치는 proxy는 초기 자세를 가두지 않도록 제외한다. 현재 시뮬레이션 튜닝
  임시값은 corridor `0.25 m`, 시작점 제외 반경 `0.18 m`, 가지 최대 48개이다.
- transit은 로봇 쪽 몸통 전체 bounding box 바깥 `0.45 m`의 안전 waypoint에
  먼저 도달해 자세를 정렬한 다음 staging으로 진입한다. 좌우 재계획 방향은
  로봇-사과 방사축이 아니라 그에 수직인 수평 lateral 축을 사용한다. `0.45 m`는
  시뮬레이션 시험 후 조정할 임시값이다.

최소 안전거리의 초기값은 다음과 같다.

- 로봇 링크 ↔ 굵은 가지: 50mm
- 그리퍼·손목 ↔ 작은 가지: 20mm

직접 transit이 수렴하지 않으면 먼저 나무 바깥 안전 waypoint로 후퇴한 뒤 목표
사과 양옆의 우회 waypoint를 순서대로 사용해 재계획한다. 위치와 회전 오차가
연속 120 simulation step 동안 유의미하게 개선되지 않으면 경로 정체로 판정한다.
후퇴에 실패하거나 모든 후보가 실패하면 `APPROACH_UNREACHABLE`로 해당 사과의
수확을 중단한다. 실행 중 목표 사과가 pre-grasp 전에 이동하거나 stem joint가
파손되면 즉시 명령을 중지하고 실패를 보고한다. 안전한 후퇴 경로가 검증된
경우에만 후퇴하며, 그렇지 않으면 현재 자세에서 정지한다.

RMPflow gain, proxy voxel 크기, proxy 수 제한 및 영향 반경은 시뮬레이션 충돌
시험 후 조정한다. 조정값은 물리 collider 크기와 planning proxy 크기를 구분해
기록한다. proxy를 선별하더라도 위 최소 안전거리 자체는 축소하지 않는다.

## Twist & Pull

파지는 세 손가락 끝으로만 누르는 방식이 아니라 사과 뒷면이 palm 지지면에
약 2mm 이내로 접근하고 세 손가락이 사과를 감싸는 포위 파지를 사용한다. 명목
지름 80mm 사과의 중심 목표는 palm 로컬 `+Y 0.093 m`이다. 이 접촉 형상으로
손목 TWIST 토크가 손가락 미끄럼 대신 사과와 줄기에 전달되도록 한다.

1. 그리퍼를 폐합한다.
2. end-effector 손목만 사용해 45°를 1초 동안 회전한다.
3. 회전 자세를 유지한다.
4. M0617이 줄기 반대 방향으로 일직선 당김을 수행한다.
5. 당김 기본 속도는 50mm/s다.
6. 최대 당김 거리는 100mm다.
7. timeout은 simulation time 기준 3초다.
8. stem joint가 break되면 수확 성공으로 판정한다.

Stem joint:

- break force: 15N
- break torque: 1Nm

회전 중 1Nm을 초과해 조기 분리되는지 시험하고 필요 시 별도 승인 후 조정한다.

## 컨베이어 배치

- 컨베이어 1 상면 30mm 이하까지 사과를 낮춘다.
- 사과를 높은 곳에서 떨어뜨리지 않고 벨트에 거의 닿은 상태에서 그리퍼를 연다.
- 중심선 기준 좌우 배치 오차 목표는 ±30mm다.

## 실패 처리

- IK/경로 실패: 정지 후 실패 상태 보고
- 예상치 못한 충돌: 정지 또는 안전 후퇴
- stem 미분리: timeout 후 실패
- 사과가 작업영역 밖으로 이탈: 비활성화
