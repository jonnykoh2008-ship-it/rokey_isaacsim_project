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

임시 안전거리:

- 로봇 링크 ↔ 굵은 가지: 50mm
- 그리퍼 ↔ 작은 가지: 20mm
- 그리퍼 ↔ 잎: 10mm

정확한 singularity 기준, joint step 제한 및 안전거리는 시뮬레이션 시험 후 튜닝한다.

## Twist & Pull

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

