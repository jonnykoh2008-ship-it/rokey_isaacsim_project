# OpenCV 기반 사과 크기 측정 계획

## 문서 목적

사과 품질 요소 중 크기를 우선 완성하기 위해 학습 모델 없이 OpenCV와 RGB-D
기하 계산으로 적도부 최대 직경을 측정하고 크기 구간을 판정하는 구현 계획을
정의한다.

이 문서는 크기 측정 기능의 작업 계획이다. 전체 품질 등급은 착색률, 크기, 손상
면적과 부패·형상 이상 조건을 함께 적용하므로 크기 단독 판정 결과를 최종 품질
등급과 동일하게 취급하지 않는다.

관련 기준 문서는 다음과 같다.

- [품질 분류](quality_grading.md)
- [컨베이어](conveyor.md)
- [ROS 2 인터페이스](../architecture/ros2_interfaces.md)
- [TF 및 시뮬레이션 시간](../architecture/tf_frames.md)
- [시뮬레이션 자산 요구사항](../assets/asset_requirements.md)
- [2차 개발: AI 및 도메인 무작위화](../phases/phase_2_ai_randomization.md)

## 범위

### 포함

- Isaac Sim에서 크기가 알려진 사과의 RGB, 정렬된 depth 및 CameraInfo 수집
- 검사 ROI 안의 depth 기반 전경 분리
- OpenCV를 이용한 사과 mask 생성과 정제
- mask와 RGB-D 기하를 이용한 실제 직경 계산
- 크기 구간 판정
- 대표 프레임별 측정과 사과 단위 결과 통합
- ground truth 대비 mask 및 직경 오차 검증
- 유효하지 않은 관측의 `RECHECK` 또는 `INSUFFICIENT_VIEWS` 처리

### 제외

- 착색률 판정
- 손상 mask 및 손상 면적 계산
- 부패, 윤택 및 형상 이상 판정
- 전체 `HIGH`, `MEDIUM`, `LOW` 품질 등급 확정
- YOLO 또는 다른 학습 모델 도입
- 컨베이어 물리, 카메라 및 공유 ROS 2 인터페이스의 소스 변경

## PC별 소유권

| 담당 | 책임 |
|---|---|
| GPU PC 1 | Isaac Sim 사과 크기 설정, 합성 RGB/depth/CameraInfo와 ground truth 생성, 컨베이어 카메라 raw 스트림 발행 |
| GPU PC 2 | raw 스트림 구독, ROI/tracker, 후보 및 대표 프레임 선택, OpenCV mask 생성, 직경 계산과 크기 결과 통합 |
| 개인 PC 2 | `QualityResult` 기반 결과 표시와 상태 확인 |

GPU PC 1과 GPU PC 2의 소스 경로는 이 문서에서 새로 정하지 않는다. GPU PC 2의
품질 캡처·측정 구현 경로는 현재 `TBD`다. 각 PC의 소스를 변경할 때는 해당 소유자와
대상 파일을 확인하고 별도 승인을 받아야 한다.

## 목표 처리 흐름

```text
Isaac Sim RGB + aligned depth + CameraInfo
  -> RGB-D timestamp 및 입력 유효성 검사
  -> 검사 ROI 추출
  -> depth 기반 벨트·배경 제거
  -> OpenCV 사과 mask 생성 및 정제
  -> mask 경계의 3D 역투영
  -> 대표 프레임별 적도부 최대 직경 계산
  -> 사과 단위 직경 통합
  -> 크기 구간 판정
  -> QualityResult 연계
```

## 크기 정의와 판정 규칙

측정 대상은 `quality_grading.md`에 정의된 적도부 최대 직경이다.

크기 단독 구간은 다음과 같이 해석한다.

| 구간 | 조건 |
|---|---:|
| `SMALL` | 직경 `< 60 mm` |
| `MEDIUM_SIZE` | `60 mm <=` 직경 `< 75 mm` |
| `LARGE` | 직경 `>= 75 mm` |

`MEDIUM_SIZE`는 최종 품질 등급의 `MEDIUM`과 구분하기 위한 내부 명칭 후보다.
크기 단독 결과의 정식 필드 및 enum을 공유 인터페이스에 추가할지는 `TBD`다.

경계값은 다음과 같이 검증한다.

| 입력 | 기대 구간 |
|---:|---|
| `59.9 mm` | `SMALL` |
| `60.0 mm` | `MEDIUM_SIZE` |
| `74.9 mm` | `MEDIUM_SIZE` |
| `75.0 mm` | `LARGE` |

## 선행 결정 사항

다음 항목은 구현 또는 최종 완료 판정 전에 승인이 필요하다.

1. 합성데이터에 적용할 최소·최대 사과 직경
2. 크기 구간별 데이터 수와 train/validation/test 구성
3. 허용 직경 오차와 크기 구간별 목표 정확도
4. 실제 D455 검증 데이터 수와 합격 기준
5. 대표 프레임 측정값의 사과 단위 통합 방식
6. 벨트 배경 depth 갱신 및 재보정 정책

`asset_requirements.md`는 모든 사과의 지름을 `80 mm`로 정의하지만,
`phase_2_ai_randomization.md`는 사과 크기를 도메인 무작위화 대상으로 정의한다.
80 mm 고정 상태에서는 `LARGE` 데이터만 생성되므로 합성데이터 수집 범위에서
크기 변경을 허용할지와 그 범위를 먼저 결정해야 한다. 결정 전까지 범위는 `TBD`다.

## 단계 1: 기준 합성데이터 생성

### 1.1 첫 번째 데이터 조건

전체 처리 흐름을 먼저 연결할 때는 변수를 제한한다.

- 사과 한 개
- 고정 카메라와 고정 검사 ROI
- 고정 조명
- 깨끗한 벨트 배경
- 사과 가림 없음
- 최소화된 depth 노이즈
- 크기 경계값 주변 표본 포함

### 1.2 저장 항목

각 프레임 또는 sample에는 다음 정보를 연결한다.

- RGB 이미지
- RGB에 정렬된 depth 이미지
- CameraInfo 또는 동등한 카메라 내부 파라미터
- 사과 instance 또는 semantic mask ground truth
- 실제 직경 `diameter_gt_mm`
- 크기 구간 label
- `apple_id`
- `inspection_id`
- `frame_index`
- `/clock` 기준 촬영 timestamp
- 카메라와 사과의 상대 위치 및 자세
- 적용한 조명, 노이즈 및 randomization 파라미터

RGB, depth, CameraInfo 및 ground truth는 동일한 프레임과 timestamp에 대응해야 한다.

### 1.3 확장 데이터 조건

기준 조건에서 성공한 뒤 다음 변수를 한 종류씩 추가한다.

1. 사과의 회전과 기울기
2. 카메라와 사과 사이 거리 변화
3. 검사 ROI 안의 좌우 위치 변화
4. 조명 밝기와 방향
5. 그림자와 표면 반사
6. depth 노이즈와 유효하지 않은 depth 픽셀
7. 벨트 색상과 재질 변화

여러 변수를 동시에 추가하기 전에 각 단계의 직경 bias와 실패 원인을 기록한다.

## 단계 2: RGB-D 입력과 ROI 검증

GPU PC 2는 후보 프레임마다 다음 항목을 확인한다.

- RGB, depth 및 CameraInfo 수신 여부
- RGB와 depth의 해상도 및 정렬 상태
- RGB와 depth의 촬영 timestamp 일치 여부
- depth 단위와 유효 범위
- 0, NaN 및 카메라 유효 범위 밖 depth 제외
- 사과 mask가 영상 경계에 닿지 않는지 여부
- 사과 mask의 90% 이상이 검사 ROI 안에 있는지 여부
- 유효 depth 픽셀 비율이 80% 이상인지 여부

90%와 80%는 기존 대표 프레임 선택의 초기 시험값이며 시험 결과에 따라 조정할
수 있다. 변경 시 근거와 검증 결과를 기록한다.

모든 ROS 2 노드는 `use_sim_time:=true`를 사용하고 timestamp는 Isaac Sim의
`/clock`을 기준으로 한다. Timeline Pause 중에는 검사 및 deadline timer도 함께
정지해야 한다.

## 단계 3: OpenCV 사과 mask 생성

### 3.1 벨트 배경 모델

사과가 없는 빈 벨트 depth 프레임 여러 장에서 픽셀별 중앙값을 계산해 기준 배경을
만드는 방식을 우선 후보로 사용한다.

```text
background_depth = median(empty_belt_depth_frames)
```

현재 depth와 배경 depth의 차이로 전경 후보를 만든다.

```text
foreground = valid_depth
             AND abs(background_depth - current_depth) > depth_threshold
```

`depth_threshold`, 빈 벨트 프레임 수와 배경 재보정 조건은 시험 전까지 `TBD`다.

벨트가 평면이고 카메라가 고정된 초기 조건에서는 배경 depth 차분을 우선한다.
카메라 자세나 벨트 형상이 변해 픽셀별 배경 모델이 불안정하면 depth point cloud의
벨트 평면 추정 방식을 대안으로 평가한다.

### 3.2 mask 정제

OpenCV 처리 후보 순서는 다음과 같다.

1. 유효 depth mask 적용
2. median 또는 Gaussian filter로 작은 depth 노이즈 완화
3. morphological opening으로 고립된 전경 픽셀 제거
4. morphological closing으로 사과 mask 내부의 작은 구멍 보정
5. connected component 또는 contour 추출
6. ROI 내부의 가장 큰 유효 객체 선택
7. 너무 작은 객체, 영상 경계 접촉 및 다중 객체 상황 거부

kernel 크기, 반복 횟수와 최소 객체 면적은 데이터 검증 전까지 `TBD`다.

HSV 또는 Lab 색상 조건은 depth mask 보조 조건으로만 평가한다. 빨간색 단독
threshold를 기본 분할 방식으로 사용하지 않는다. 착색이 부족하거나 녹색인 사과도
동일하게 측정할 수 있어야 한다.

## 단계 4: 대표 프레임별 직경 계산

### 4.1 1차 픽셀-직경 근사

초기 파이프라인 연결과 오류 확인에는 다음 pinhole 근사를 사용할 수 있다.

```text
diameter_mm = pixel_width * representative_depth_m / fx * 1000
```

- `pixel_width`: 선택한 수평선에서 사과 mask의 좌우 폭
- `representative_depth_m`: 해당 측정선 주변 유효 depth의 대표값
- `fx`: CameraInfo의 수평 초점거리

이 방식은 자세, 비구형 형상과 좌우 경계의 depth 차이에 민감하므로 최종 정확도
검증용 기본 방식으로 확정하지 않는다.

### 4.2 3D 경계점 방식

최종 후보 방식은 다음과 같다.

1. mask 중심부의 여러 수평 측정선을 선택한다.
2. 각 측정선의 왼쪽과 오른쪽 경계 픽셀을 찾는다.
3. 각 경계 주변에서 유효 depth의 robust 대표값을 구한다.
4. CameraInfo의 `fx`, `fy`, `cx`, `cy`를 사용해 경계점을 camera frame의 3D 점으로 역투영한다.
5. 좌우 3D 점 사이의 유클리드 거리를 계산한다.
6. 유효 측정선의 거리 집합에서 outlier를 제거한다.
7. 적도부 최대 직경 후보를 선택하고 `diameter_mm`로 변환한다.

depth가 없는 정확한 경계 픽셀은 인접한 mask 내부 픽셀의 유효 depth를 사용할 수
있다. 인접 영역 크기와 대표값 선택 방법은 검증 결과로 결정하며 현재 `TBD`다.

`minEnclosingCircle` 또는 bounding box 폭은 디버그 비교값으로 기록할 수 있지만,
원근과 자세 변화를 보정하지 못하므로 실제 mm 단위 결과의 단독 근거로 사용하지
않는다.

## 단계 5: 다중 프레임 결과 통합

GPU PC 2는 ROI 통과 중 0.1초 간격으로 후보 프레임을 최대 12장 수집하고 기존
기준에 따라 대표 프레임 4~6장을 선택한다.

각 대표 프레임에서 다음 값을 기록한다.

- `frame_index`
- mask 유효 여부
- 유효 depth 비율
- 프레임별 직경
- 측정선 수와 유효 측정선 수
- outlier 제거 전후 통계
- 실패 사유

사과 단위 직경 통합 후보는 다음과 같다.

- 대표 프레임 직경의 최댓값
- 대표 프레임 직경의 중앙값
- 대표 프레임 직경의 상위 percentile
- 자세 또는 가시 적도부 품질을 반영한 가중값

각 후보를 ground truth와 비교한 뒤 MAE, bias와 경계 분류 오류가 가장 작은 방식을
선택한다. 최종 통합 규칙은 시험 전까지 `TBD`다.

유효한 대표 프레임이 4장 미만이면 `INSUFFICIENT_VIEWS`로 처리한다.

## 단계 6: 결과 및 실패 처리

기존 `QualityResult`에는 다음 값을 연결한다.

- `diameter_mm`
- `frames_used`
- `frame_indices`
- `confidence`
- `result_timestamp`
- `status`

크기 단독 구간을 기존 `grade`에 직접 쓰지 않는다. 기존 `grade`는 착색률, 크기,
손상 면적 및 기타 결함을 통합한 최종 품질 등급이다. 크기 단독 결과 전달 방식은
GPU PC 2 내부 결과로 먼저 유지하고, 공유 인터페이스 변경 필요성은 별도로 검토한다.

다음 상황에서는 직경을 강제로 판정하지 않는다.

- 사과 mask를 검출하지 못함
- mask가 영상 경계에 닿음
- 여러 사과 또는 객체가 하나의 mask로 합쳐짐
- RGB-depth 입력이 동기화되지 않음
- CameraInfo가 없거나 입력 해상도와 일치하지 않음
- 유효 depth 비율이 부족함
- 대표 프레임 수가 부족함
- 프레임별 직경 편차가 허용 범위를 벗어남
- `apple_id` 또는 `inspection_id`의 연속성을 보장할 수 없음

대표 프레임 부족은 `INSUFFICIENT_VIEWS`, 신뢰할 수 없는 측정은 `RECHECK` 후보로
처리한다. 구체적인 직경 편차와 confidence threshold는 `TBD`다.

## 단계 7: 검증 계획

### 7.1 데이터 분리

같은 사과와 scene의 연속 프레임이 파라미터 조정용 데이터와 최종 검증 데이터에
동시에 포함되지 않도록 `apple_id` 또는 scene 단위로 분리한다.

### 7.2 검증 지표

- OpenCV mask와 Replicator ground-truth mask 사이의 IoU
- 직경 MAE
- 직경 최대 절대 오차
- 직경 bias
- 직경 구간별 confusion matrix
- 크기 구간별 정확도
- `RECHECK` 및 `INSUFFICIENT_VIEWS` 비율
- 프레임 처리시간
- ROI 이탈 후 사과 단위 결과 산출시간

목표 데이터 규모, 허용 직경 오차, 목표 정확도와 허용 실패율은 현재 `TBD`다.
첫 기준 데이터의 결과를 확보한 뒤 강사 및 팀과 합격 기준을 확정한다.

### 7.3 검증 순서

1. 고정 자세와 고정 조명의 합성데이터
2. 회전, 기울기와 거리 변화 합성데이터
3. 조명, 반사와 depth 노이즈 합성데이터
4. 실제 D455로 촬영한 제한된 검증 데이터
5. 대표 프레임 수집과 컨베이어 deadline을 포함한 통합 시험

카메라 ROI 이탈 후 결과 deadline은 simulation time `0.5초`다. deadline 안의 정상
결과 산출 여부를 통합 시험에서 확인한다.

## OpenCV 방식 유지 및 모델 전환 기준

OpenCV 방식은 고정 카메라, 제한된 검사 ROI와 통제된 벨트 배경에서 우선 완성한다.
다음 문제가 합의된 목표를 지속적으로 만족하지 못할 때만 사과 mask 생성부를
segmentation 모델로 교체하는 것을 검토한다.

- 조명과 반사 변화로 depth 보조 mask도 불안정함
- 여러 사과나 다른 객체의 분리가 필요함
- 실제 영상의 depth 결측으로 mask가 반복적으로 단절됨
- 배경 변화마다 threshold 재조정이 필요함
- 합의한 mask IoU와 직경 오차 기준을 달성하지 못함

모델을 도입하더라도 RGB-D 기하 기반 직경 계산과 판정 규칙은 유지한다.

## 완료 조건

다음을 모두 만족하면 OpenCV 기반 크기 측정 기능을 완료한 것으로 판정한다.

- 세 크기 구간과 60 mm, 75 mm 경계를 포함한 검증 데이터가 있다.
- RGB, 정렬된 depth, CameraInfo 및 직경 ground truth가 같은 sample로 연결된다.
- OpenCV가 검사 ROI의 사과 mask를 생성한다.
- depth와 CameraInfo로 대표 프레임별 `diameter_mm`를 계산한다.
- 다중 프레임 측정값을 사과 단위 결과로 통합한다.
- ground truth 대비 mask 및 직경 오차 보고서가 있다.
- 크기 구간 confusion matrix와 경계값 테스트 결과가 있다.
- 유효하지 않은 입력을 정상 결과와 분리한다.
- 모든 처리 timestamp와 timer가 simulation time 규칙을 따른다.
- 합의한 데이터 규모, 정확도, 오차, 실패율 및 처리시간 기준을 통과한다.
- 실제 D455 검증 데이터에서 합의한 기준을 통과한다.

수치 합격 기준이 `TBD`인 동안에는 알고리즘이 동작하더라도 최종 완료로 확정하지
않는다.
