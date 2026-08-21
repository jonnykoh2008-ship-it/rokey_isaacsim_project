# 2차 개발: 푸셔 분류

## 목표

컨베이어 3에 prismatic joint 기반 푸셔 3개를 구현하고 `QualityResult`에 따라 사과를 물리적으로 분류한다.

## 구성

- 푸셔 수: 3개
- 위치 1: 컨베이어 3 진입점에서 0.10m, 상
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

컨베이어 3 진입 trigger의 simulation time과 고정 속도로 예상 도착 시각을 계산하고, 푸셔 위치 trigger에서 최종 존재를 확인한다.

## 상태 흐름

```text
WAITING
  → ARMED
  → APPLE_CONFIRMED
  → EXTENDING
  → PUSH_CONFIRMED
  → RETRACTING
  → HOME_CONFIRMED
  → WAITING
```

- 원점 복귀가 확인되기 전에는 다음 사과의 푸셔 동작을 허용하지 않는다.
- 미분류, `RECHECK`, timeout 및 놓친 사과는 라인 끝으로 통과시킨다.
- 상자 용량과 상자 교체는 구현하지 않는다.

## 통신

- 개인 PC 2가 `QualityResult`를 받아 푸셔를 선택한다.
- `SortCommand`를 GPU PC 1의 Isaac Sim으로 보낸다.
- GPU PC 1이 trigger와 명령을 검증한 후 joint를 구동한다.

## 미확정 사항

- 푸셔 stroke, 속도, 가속도, 힘 및 치수
- 각 푸셔 trigger의 크기와 위치
- 세 번째 푸셔와 컨베이어 출구 사이 안전거리
- 사과가 실제 분류 영역에 진입했는지 판정하는 방법
- 푸셔 실패, jam 및 ID mismatch 복구
- 동시에 여러 사과가 존재할 때 queue 정책
- `RECHECK` 전용 경로 또는 라인 끝 보관 방식
- 완료 기준과 반복 시험 횟수

