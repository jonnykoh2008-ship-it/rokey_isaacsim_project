# 수확 및 파지

## 구성

- 로봇: Doosan M0617
- 그리퍼: AGS-001-MTCP
- solver: LulaKinematicsSolver
- 물리 수확 TCP: USD `palm` 원점에서 palm 로컬 `+Y 0.0908 m`
- GPU PC 1은 Isaac Sim 동적 TF에 `palm` frame을 발행한다.
- 개인 PC 1은 `world → palm`을 조회하고 palm 로컬 `+Y` offset을 적용해
  현재 TCP pose를 계산한다.
- Lula/RMPflow 제어 frame: `link_6`

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
  → RELEASE
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

- GPU PC 1은 reset마다 전체 몸통 box와 가지 sphere planning proxy snapshot을
  `world` 좌표로 발행한다. 잎과 목표 사과는 정적 snapshot에서 제외한다.
- 개인 PC 1은 현재 `reset_id/scene_version`의 snapshot만 사용해 홈 자세에서
  pre-grasp까지 direct, 좌우, 추가 외측 전역 waypoint 후보를 계획한다.
- 개인 PC 1의 APPROACH 경로 마지막 waypoint는 사과 중심에서 world `-Z`
  방향 `0.15 m`의 pre-grasp pose여야 한다.
- GPU PC 1은 외부 waypoint의 frame, scene version, 순차 IK와 자체 planning
  proxy 여유를 다시 검사한다. 검사를 통과하지 못하면 로봇을 움직이지 않는다.
- GPU PC 1의 transit 실행은 단순 관절 보간을 사용하지 않고 Lula/RMPflow의
  로봇 collision sphere와 planning obstacle을 사용한다.
- M0617 전체 링크는 굵은 가지 planning proxy와 충돌하지 않아야 한다.
- 그리퍼와 손목은 작은 가지 planning proxy와 충돌하지 않아야 한다.
- 몸통 mesh가 여러 개인 경우 각 mesh를 별도 planning obstacle로 유지한다.
  로봇 collision sphere는 URDF의 관절 간 링크 구간과 collision mesh 범위를
  빠짐없이 덮어야 한다.
- 목표 사과는 transit 중 planning obstacle로 유지하고, 사과 중심에서 world
  `+Z` 반대 방향으로 `0.30 m` 떨어진 staging pose에 도달한 뒤 해제한다.
- 목표 사과 obstacle 해제 후 같은 접근축을 따라 `0.15 m` pre-grasp pose로
  이동하고, 이어서 의도된 `+Z` grasp 접근을 수행한다.
- `0.15 m` pre-grasp에서 사과 아래 `0.03 m`까지 저속 진입하고, 마지막
  `0.03 m`는 더 낮은 속도로 접근한다. 두 구간의 360 simulation step과
  `0.03 m` 전환 거리는
  실제 collider 접촉 시험 후 조정할 임시값이다.
- 진입 중 두 측면 palm joint는 URDF의 바깥쪽 limit인 각각 `+0.25 rad`,
  `-0.25 rad`로 벌린다. 세 distal joint는 `-1.20 rad`로 접어 손가락 끝을
  접근축에서 사과 통로 바깥으로 빼며, 이 값은 collider 시험용 임시값이다.
- 가운데 손가락 proximal joint 후보 `0.00`, `0.10`, `0.35`, `0.60 rad`를
  pre-grasp에서 시험하고, 현재 authored collision mesh를 TCP→사과 중심
  선분으로 sweep했을 때 최소 clearance가 가장 큰 자세를 선택한다. 후보값은
  시뮬레이션 시험 후 조정할 임시값이다.
- swept clearance는 사과 반지름을 제외하고 최소 `5 mm`를 확보해야 한다.
  확보하지 못하면 실제 ENTER를 시작하지 않고 `COLLISION_RISK`를 반환한다.
- gripper 물리 표현은 각 링크의 authored collision mesh 하나만 사용한다.
  동일 형상의 runtime 복제 collider를 동시에 활성화하지 않는다.
- 최종 저속 접근에서 palm collider의 사과 접촉이 확인되면 즉시 팔 pose를
  유지하고 `GRASP`를 허용한다. palm보다 손가락 collider가 먼저 접촉하거나
  일반 진입 구간에서 접촉하면 즉시 정지하고 `COLLISION_RISK`를 반환한다.
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

개인 PC 1이 계획을 만들지 못하면 `APPROACH_UNREACHABLE`로 해당 사과를
수확하지 않는다. GPU PC 1은 Action 실행 직전에 실제 PhysX collider가 이미
겹쳐 있는지 검사하고, 실행 중 Contact Report에서 로봇-나무 접촉을 감지하면
`UNEXPECTED_CONTACT`로 Action을 중단한다. 사과와 그리퍼의 의도된 접촉 및
로봇 자체 접촉은 이 나무 접촉 감시 조건에 포함하지 않는다.

Timeline Stop/Reset 시 GPU PC 1은 실행 중 Action을 종료하고 `reset_id`를
증가시킨 뒤 새 snapshot을 발행한다. 개인 PC 1은 이전 waypoint, IK seed 및
실패 대상 캐시를 폐기하고 `READY/PLAYING`과 snapshot 동기화를 확인한 후에만
다음 계획을 시작한다.

RMPflow gain, proxy voxel 크기, proxy 수 제한 및 영향 반경은 시뮬레이션 충돌
시험 후 조정한다. 조정값은 물리 collider 크기와 planning proxy 크기를 구분해
기록한다. proxy를 선별하더라도 위 최소 안전거리 자체는 축소하지 않는다.

## Twist & Pull

파지는 세 손가락 끝으로만 누르는 방식이 아니라 사과 뒷면의 palm collider
접촉을 먼저 확인하고 세 손가락이 사과를 감싸는 포위 파지를 사용한다. 명목
지름 80mm 사과의 중심 목표는 palm 로컬 `+Y 0.0908 m`이다. 이 접촉 형상으로
손목 TWIST 토크가 손가락 미끄럼 대신 사과와 줄기에 전달되도록 한다.

1. 그리퍼를 폐합한다.
2. end-effector 손목만 사용해 45°를 1초 동안 회전한다.
3. 회전 자세를 유지한다.
4. M0617이 줄기 반대 방향으로 일직선 당김을 수행한다.
5. 당김 기본 속도는 50mm/s다.
6. 최대 당김 거리는 100mm다.
7. 당김 중 유의미한 TCP 진전이 연속 3초 없으면 timeout이다.
8. `PULL` 단계는 stem joint가 break된 것까지 확인해야 성공으로 판정한다.

Stem joint:

- break force: 15N
- break torque: 1Nm

회전 중 1Nm을 초과해 조기 분리되는지 시험하고 필요 시 별도 승인 후 조정한다.

## 컨베이어 배치

- 컨베이어 1 상면 30mm 이하까지 사과를 낮춘다.
- `PLACE`는 목표 pose까지 이동만 수행한다.
- `RELEASE`는 현재 pose를 유지하고 그리퍼만 개방한다.
- 사과를 높은 곳에서 떨어뜨리지 않고 벨트에 거의 닿은 상태에서 그리퍼를 연다.
- 중심선 기준 좌우 배치 오차 목표는 ±30mm다.

## 모션 실행 규칙

- `GRASP`와 `RELEASE` Goal의 `target_pose`는 Goal 전송 시점의 현재 pose로 채운다.
- `GRASP`는 현재 pose를 유지하고 그리퍼만 폐합한다.
- 각 단계의 timeout은 `/clock` 기준으로 유의미한 TCP 위치
  또는 자세 진전이 연속 3초 없을 때 발생한다. Timeline Pause 중에는
  simulation time이 정지하므로 watchdog도 진행하지 않는다.
- 모션 Action 실행 중에는 새 Goal을 받지 않고 cancel만 허용한다.
- Feedback의 `progress`는 `0.0`에서 `1.0` 범위를 사용한다.
- 성공 Result의 `error_code`는 빈 문자열이다.
- 실행 중 실패하면 로봇 동작을 즉시 멈추고 실패 Result를 반환한다. 실패 후 자동 후퇴는 수행하지 않는다.
- Goal 전 계획·검증 실패는 `/harvest/motion_status`로 GPU PC 1에 전달한다.
- 계획·검증 실패 상태 메시지는 `success=false`, 기존 300번대 `error_code`, 실패 상태와 설명을 포함한다.
- GPU PC 1은 `MotionStatus` 실패를 기록·로그하지만 이 기록만으로
  후속 RobotMotion Goal을 차단하지 않는다. Goal 허용은 현재
  `SimulationState`, `reset_id`, `scene_version`, busy 상태로 판정한다.

## 실패 처리

- IK/경로 실패: 정지 후 실패 상태 보고
- Goal 전 IK/경로 실패: `/harvest/motion_status` 발행 후 실패 상태 종료
- 예상치 못한 충돌: 즉시 정지 후 실패 상태 보고
- stem 미분리: timeout 후 실패
- Action cancel: 즉시 정지 후 cancel 결과 보고
- 사과가 작업영역 밖으로 이탈: 비활성화
