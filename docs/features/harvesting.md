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
- 각 단계의 기본 timeout은 `/clock` 기준 simulation time 3초다.
- 모션 Action 실행 중에는 새 Goal을 받지 않고 cancel만 허용한다.
- Feedback의 `progress`는 `0.0`에서 `1.0` 범위를 사용한다.
- 성공 Result의 `error_code`는 빈 문자열이다.
- 실행 중 실패하면 로봇 동작을 즉시 멈추고 실패 Result를 반환한다. 실패 후 자동 후퇴는 수행하지 않는다.

## 실패 처리

- IK/경로 실패: 정지 후 실패 상태 보고
- 예상치 못한 충돌: 즉시 정지 후 실패 상태 보고
- stem 미분리: timeout 후 실패
- Action cancel: 즉시 정지 후 cancel 결과 보고
- 사과가 작업영역 밖으로 이탈: 비활성화
