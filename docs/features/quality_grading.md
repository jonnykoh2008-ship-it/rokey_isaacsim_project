# 품질 분류

## 범위

컨베이어 2 상단 D455 카메라 한 대로 사과 영상을 수집하고 상·중·하 등급을 산출한다. 수확용 사과 위치 인식과는 별도 기능이다.

## 검사 흐름

1. RGB 영상과 bounding box 검출을 상시 수행한다.
2. tracker가 `apple_id`를 유지한다.
3. ROI 진입 시 `inspection_id`를 생성하고 후보 프레임을 수집한다.
4. 후보 프레임 중 대표 프레임을 선택한다.
5. GPU PC 2가 프레임별 품질을 추론한다.
6. 프레임 결과를 사과 단위로 통합한다.
7. ROI 이탈 시 `QualityResult`를 확정한다.
8. ID가 유실·변경되거나 관측이 부족하면 `RECHECK`로 처리한다.

ROI 통과 중 후보 프레임을 0.1초 간격으로 최대 12장 수집하고, 흔들림·blur·중복 시점을 제외한 대표 프레임 4~6장을 추론에 사용한다. 결과에는 실제 사용한 `frame_index`를 기록한다.

## GPU PC 2 입력 및 모델

- GPU PC 1은 각 대표 프레임의 압축 RGB, 사과 표면 mask, RGB에 정렬된 depth 및 해당 시점의 `CameraInfo`를 GPU PC 2로 전달한다.
- GPU PC 2가 RGB/depth 기반 품질 추론과 직경·손상 면적 기하 측정을 담당한다.
- RGB 모델 입력은 640×640으로 resize/letterbox하고 학습과 추론에 동일한 정규화를 적용한다.
- depth는 신경망 입력에 직접 사용하지 않고 직경과 손상 면적 계산에 사용한다.
- 모델은 등급을 직접 출력하지 않고 목표 착색 mask, 손상 mask, 심각 결함 여부와 각 출력의 confidence를 생성한다.
- 착색률은 유효 사과 표면 중 목표 착색 mask의 비율로 계산하고, 손상 면적은 손상 mask와 depth로 계산한다.
- 직경은 정렬된 depth와 실행 시 전달받은 camera intrinsics로 계산한다. intrinsics를 코드 상수로 고정하지 않는다.
- 프레임 confidence는 유효한 모델 출력 confidence의 평균이다. 초기 유효 threshold는 0.5이며 핵심 측정의 confidence가 0.5 미만이면 해당 측정값을 무효 처리한다.
- 모델 배포 형식은 ONNX를 기본으로 하고 GPU PC 2의 MVP 실행 백엔드는 ONNX Runtime CUDA를 사용한다. 성능이 부족하면 TensorRT 변환을 검토한다.
- annotation 최소 단위는 사과 표면, 목표 착색 영역, 손상 영역, 무시 영역 mask와 심각 결함 여부다. MVP는 동일 적색 사과 품종군을 대상으로 하며 정상적인 과피 거침은 손상에서 제외하고 검은별무늬병(scab)은 손상에 포함한다.

`InspectionImage`는 RGB, 사과 mask, `16UC1; compressedDepth png` 형식의 optical Z-depth와 `CameraInfo`를 한 프레임으로 전달한다. 완료 이벤트는 `/quality/inspection_completed`의 `InspectionCompleted`를 사용한다. 정확한 필드와 QoS는 `docs/architecture/ros2_interfaces.md`를 따른다.

## 대표 프레임 선택

- 사과 mask가 영상 경계에 닿지 않아야 한다.
- 사과 mask의 90% 이상이 검사 ROI 안에 있어야 한다.
- 유효 depth 픽셀 비율이 80% 이상이어야 한다.
- Laplacian variance가 100 이상이어야 한다.
- 이전 대표 프레임과 추정 회전 차이가 45° 미만이면 제외한다.
- 최대 6장, 최소 4장을 선택한다.
- 대표 프레임이 4장 미만이면 `INSUFFICIENT_VIEWS`로 처리한다.

90%, 80%, 100, 45°는 초기 시험값이며 시험 결과에 따라 조정한다.

카메라 ROI는 수집의 시작과 종료를 판단한다. trigger collider는 컨베이어 진입·이탈 시각, 점유시간과 공정 상태 전환을 측정하며 대표 프레임 선택에는 직접 사용하지 않는다.

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

- 착색률: `target_color_mask / (apple_surface_mask - ignore_mask)`의 픽셀 비율
- 크기: 사과 표면 mask의 유효 depth 픽셀을 3D로 역투영한 뒤 영상 수평·수직 방향 범위 중 큰 값으로 근사한 가시 최대 직경
- MVP 손상 면적: RGB의 사과·손상 mask와 정렬된 depth 및 camera intrinsics로 손상 픽셀을 3D 점으로 역투영하고, mask 내부의 인접한 유효 3D 점으로 구성한 삼각형의 면적 합으로 국소 표면 면적을 근사한 뒤 대표 프레임별 값 중 최댓값을 사용
- 확장: 다중 프레임 mask를 사과 표면 좌표계에 투영한 합집합 면적
- 사과 경계, 반사광, 가림처럼 판정할 수 없는 픽셀은 ignore mask로 제외한다.
- depth가 0, NaN 또는 카메라 유효 범위 밖이면 계산에서 제외한다.
- 유효한 손상 면적 측정 프레임이 2장 미만이면 `RECHECK`로 처리한다.
- 사과 구면 모델 투영과 mask 비율·추정 표면적 방식은 대안으로 기록하며 MVP 기본 방식으로 사용하지 않는다.

## 다중 프레임 통합

- 착색률은 유효 대표 프레임 측정값의 평균을 사용한다.
- 직경은 유효 측정값의 중앙값을 사용한다.
- 손상 면적 또는 손상률은 유효 대표 프레임 측정값 중 최댓값을 사용한다.
- 심각 결함은 유효 프레임 한 장에서라도 검출되면 `true`로 통합한다.
- 프레임별로 등급을 확정하거나 등급 투표를 하지 않는다. 측정값을 사과 단위로 통합한 뒤 등급 규칙을 한 번 적용한다.
- 일부 프레임 처리가 실패해도 정상 처리된 대표 프레임이 4장 이상이면 통합한다. 4장 미만이면 `INSUFFICIENT_VIEWS`로 처리한다.
- 최종 confidence는 유효 프레임별 confidence의 평균을 사용한다.

## ID 예외 처리

- ID가 변경되면 `RECHECK`로 처리한다.
- 두 사과의 bounding box가 겹치거나 ID switch가 발생한 경우 `RECHECK`로 처리한다.
- 한 사과가 여러 detection으로 분리된 경우 `RECHECK`로 처리한다.
- 일시 누락 후 동일 ID로 복구된 경우에도 해당 inspection의 관측 연속성을 검증하며, 연속성을 보장할 수 없으면 `RECHECK`로 처리한다.
- 컨베이어 2의 `apple_id`와 컨베이어 3 trigger의 rigid body prim이 일치하지 않으면 `ID_MISMATCH`로 처리한다.

## 결과 시간 처리

- GPU PC 1은 사과가 카메라 ROI를 이탈하면 `/quality/inspection_completed`에 `InspectionCompleted`를 발행한다.
- GPU PC 2는 검사 완료 이벤트의 ROI 이탈 timestamp를 deadline 시작점으로 사용한다.
- 완료 이벤트 수신 시 누락된 `frame_index`가 있으면 deadline까지 기다리고, 이후에도 누락된 프레임은 실패 프레임으로 처리한다.
- 결과 deadline은 카메라 ROI 이탈 후 simulation time 0.5초다.
- deadline 안에 결과가 도착하면 정상 처리한다.
- deadline까지 결과가 없으면 해당 검사에 대한 유일한 최종 결과로 `TIMEOUT`을 발행한다.
- deadline 이후 끝난 추론은 `LATE_RESULT`로 내부 로그에만 기록한다.
- deadline 이후 계산된 정상 등급 또는 별도 `LATE_RESULT` 메시지는 다시 발행하지 않는다.
- `ID_MISMATCH`는 tracker ID와 rigid body prim 정보를 함께 가진 공정·추적 관리 노드가 판정하며 GPU PC 2는 입력 검사 내부의 `apple_id` 일치만 검증한다.
- `TIMEOUT`, `RECHECK`, `UNCLASSIFIED`는 푸셔와 연결하지 않고 컨베이어 3 라인 끝으로 통과시킨다.
- 공정 시간은 `/clock` 기준 simulation time을 사용한다.
- 완료 이벤트가 없는 미완료 세션은 wall time 3초 후 폐기해 메모리 누적을 방지한다.

## 통신

```text
GPU PC 1
후보 프레임 수집 및 대표 프레임 선택
  → inspection_id + apple_id + frame_index
    + compressed RGB + apple mask + aligned depth + CameraInfo
  → ROI 이탈 검사 완료 이벤트

GPU PC 2
이미지별 품질 추론 및 사과 단위 통합
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

세부 모델 규모, 등급별 목표 정확도, 정규화 세부값과 confidence 보정 방식은 학습 및 검증 후 확정한다. 압축 depth로 계산한 직경·손상 면적의 허용 오차와 무시 영역의 세부 annotation 사례는 실제 데이터 검증 후 확정한다. 네트워크 장애 감지용 heartbeat 토픽과 다중 사과 ID 복구 규칙은 통신 시험을 거쳐 확정한다.
