# 품질 분류

## 범위

컨베이어 2 상단 D455 카메라 한 대로 사과 영상을 수집하고 상·중·하 등급을 산출한다. 수확용 사과 위치 인식과는 별도 기능이다.

v2.0에서 GPU PC 1은 컨베이어 물리·checkpoint와 컨베이어 카메라 raw RGB/depth/
CameraInfo 스트림을 발행한다. GPU PC 2는 raw 스트림을 구독해 ROI/tracker, 후보
프레임 수집, 대표 프레임 선택, 품질 추론과 사과 단위 결과 통합을 수행한다. 개인
PC 1의 RGB-D 수확 인식과 target 발행은 이 문서의 품질 `apple_id` lifecycle과
분리한다.

## 검사 흐름

1. GPU PC 2가 raw RGB/depth/CameraInfo를 수신하고 RGB 영상과 bounding box 검출을 상시 수행한다.
2. GPU PC 2의 tracker가 `apple_id`를 유지한다.
3. GPU PC 2가 ROI 진입 시 `inspection_id`를 생성하고 후보 프레임을 수집한다.
4. GPU PC 2가 후보 프레임 중 대표 프레임을 선택한다.
5. GPU PC 2가 대표 프레임별 품질을 추론한다.
6. GPU PC 2가 프레임 결과를 사과 단위로 통합한다.
7. GPU PC 2가 ROI 이탈 시 `QualityResult`를 확정한다.
8. ID가 유실·변경되거나 관측이 부족하면 GPU PC 2가 `RECHECK`로 처리한다.

GPU PC 2는 ROI 통과 중 후보 프레임을 0.1초 간격으로 최대 12장 수집하고,
흔들림·blur·중복 시점을 제외한 대표 프레임 4~6장을 추론에 사용한다. 결과에는
실제 사용한 `frame_index`를 기록한다.

## 대표 프레임 선택

- 사과 mask가 영상 경계에 닿지 않아야 한다.
- 사과 mask의 90% 이상이 검사 ROI 안에 있어야 한다.
- 유효 depth 픽셀 비율이 80% 이상이어야 한다.
- Laplacian variance가 100 이상이어야 한다.
- 이전 대표 프레임과 추정 회전 차이가 45° 미만이면 제외한다.
- 최대 6장, 최소 4장을 선택한다.
- 대표 프레임이 4장 미만이면 `INSUFFICIENT_VIEWS`로 처리한다.

90%, 80%, 100, 45°는 초기 시험값이며 시험 결과에 따라 조정한다.

GPU PC 2의 카메라 ROI는 영상 수집의 시작과 종료를 판단한다. GPU PC 1의 trigger
collider/checkpoint event는 컨베이어 진입·이탈 시각, 점유시간 및 공정 상태 전환을
제공하며 대표 프레임 선택 자체에는 직접 사용하지 않는다.

## 등급 규칙

### 상 (`HIGH`)

다음을 모두 만족해야 한다.

- 착색률 80% 이상
- 적도부 최대 직경 75mm 이상
- 손상 면적 1.0cm² 이하
- 부패나 심각한 형상 이상 없음

### 하 (`LOW`)

다음 상품성 상실 조건 중 하나라도 만족하면 적용한다.

- 착색률 60% 미만
- 적도부 최대 직경 60mm 미만
- 손상 면적 2.5cm² 초과
- 부패, 큰 멍 또는 심각한 형상 이상

### 중 (`MEDIUM`)

- 하에 해당하지 않으며 상의 모든 조건을 만족하지 않는 판매 가능한 사과

예: 착색률 90%, 직경 80mm, 손상 1.5cm²인 사과는 `MEDIUM`이다.

경계값은 다음과 같이 처리한다.

- 착색률 60%는 `LOW` 조건이 아니며 80%는 `HIGH` 조건을 만족한다.
- 직경 60mm는 `LOW` 조건이 아니며 75mm는 `HIGH` 조건을 만족한다.
- 손상 면적 1.0cm²는 `HIGH` 조건을 만족한다.
- 손상 면적 2.5cm²는 `LOW` 조건이 아니며 2.5cm²를 초과할 때 `LOW`다.

## 측정 정의

- 크기: 적도부 최대 직경
- MVP 손상 면적: RGB의 사과·손상 mask와 정렬된 depth 및 camera intrinsics로 손상 픽셀을 3D 점으로 역투영하고, mask 내부의 인접한 유효 3D 점으로 구성한 삼각형의 면적 합으로 국소 표면 면적을 근사한 뒤 대표 프레임별 값 중 최댓값을 사용
- 확장: 다중 프레임 mask를 사과 표면 좌표계에 투영한 합집합 면적
- depth가 0, NaN 또는 카메라 유효 범위 밖이면 계산에서 제외한다.
- 유효한 손상 면적 측정 프레임이 2장 미만이면 `RECHECK`로 처리한다.
- 사과 구면 모델 투영과 mask 비율·추정 표면적 방식은 대안으로 기록하며 MVP 기본 방식으로 사용하지 않는다.

## ID 예외 처리

- ID가 변경되면 `RECHECK`로 처리한다.
- 두 사과의 bounding box가 겹치거나 ID switch가 발생한 경우 `RECHECK`로 처리한다.
- 한 사과가 여러 detection으로 분리된 경우 `RECHECK`로 처리한다.
- 일시 누락 후 동일 ID로 복구된 경우에도 해당 inspection의 관측 연속성을 검증하며, 연속성을 보장할 수 없으면 `RECHECK`로 처리한다.
- 컨베이어 2의 `apple_id`와 컨베이어 3 trigger의 rigid body prim이 일치하지 않으면 `ID_MISMATCH`로 처리한다.

## 결과 시간 처리

- 결과 deadline은 카메라 ROI 이탈 후 simulation time 0.5초다.
- deadline 안에 결과가 도착하면 정상 처리한다.
- deadline까지 결과가 없으면 `TIMEOUT`으로 처리한다.
- deadline 이후 결과가 도착하면 `LATE_RESULT`로 기록한다.
- `TIMEOUT`, `LATE_RESULT`, `RECHECK`, `UNCLASSIFIED`는 푸셔와 연결하지 않고 컨베이어 3 라인 끝으로 통과시킨다.
- 공정 시간은 `/clock` 기준 simulation time을 사용한다.

## 통신

```text
GPU PC 1
컨베이어 raw RGB/depth/CameraInfo + checkpoint event
  → GPU PC 2

GPU PC 2
ROI/tracker + 후보 프레임 수집 및 대표 프레임 선택
  → 이미지별 품질 추론 및 사과 단위 통합
  → QualityResult

MVP
QualityResult와 apple_id 연결 확인 후 컨베이어 3 라인 끝으로 배출

2차 개발
개인 PC 2가 등급별 푸셔를 선택
  → GPU PC 1의 컨베이어 4 실제 푸셔 작동
```

## 참고

- EU 공식 규격: <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R2429-20251004>
- 내부 참고: `TalkFile_apple_harvesting_quality_grading_design.md` (현재 저장소 존재 여부 확인 필요)

## 미확정 사항

품질 모델 구조와 세부 출력 필드, confidence threshold 및 등급별 목표 정확도는 협동 데이터 학습과 검증 후 확정한다. 착색률·윤택·부패·형상 이상의 annotation 규칙과 프레임별 결과 통합 규칙도 데이터 특성을 확인할 때까지 TBD로 둔다. 일시 누락 후 동일 ID 복구를 허용할 구체적인 연속성 기준, 네트워크 장애 감지용 wall-time timeout 및 다중 사과 상황의 ID 복구 규칙은 통신 시험을 거쳐 확정한다.
