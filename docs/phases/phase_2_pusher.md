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

컨베이어 4 진입 trigger의 simulation time과 고정 속도로 예상 도착 시각을 계산하고, 푸셔 위치 trigger에서 최종 존재를 확인한다.

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

푸셔의 stroke, 속도, 가속도, 힘과 치수는 사과의 질량·속도 및 컨베이어 폭을 반영한 동역학 시험 후 확정한다. 각 trigger의 크기와 위치, 세 번째 푸셔와 컨베이어 4 출구 사이 안전거리, 실제 분류 영역 진입 판정 방법도 레이아웃 검증 전까지 TBD로 둔다. 푸셔 실패·jam·ID mismatch 복구, 다중 사과 queue, `RECHECK` 사과의 보관 방식, 완료 기준과 반복 시험 횟수는 통합 시험 계획과 함께 결정한다.
