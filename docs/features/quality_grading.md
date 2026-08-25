# 품질 분류

## 현재 구현 범위

현재 GPU PC 2 MVP는 사과 검출과 크기 단일 분류가 끝까지 연결되는지 확인하는
단계다. 고정된 컨베이어 카메라 영상에서 한 번에 사과 한 개를 OpenCV로 검출하고,
검출 윤곽의 픽셀 직경을 카메라 보정값으로 mm 단위에 대응시킨 뒤 크기만으로
HIGH, MEDIUM, LOW를 판정한다.

착색률, 손상 면적, 심각 결함, 신경망 segmentation 학습은 현재 등급 판정에 사용하지
않으며 후속 확장 범위로 둔다. 이 결정은 합성데이터의 착색·손상 표현을 먼저
완성하려다 전체 감지·분류 흐름 검증이 지연되는 문제를 줄이기 위한 것이다.

v2.0 소유권은 다음과 같다.

- GPU PC 1: Isaac Sim 컨베이어 물리와 raw RGB/depth/CameraInfo 발행
- GPU PC 2: 컨베이어 영상 수신, 사과 검출, 크기 측정·분류, 결과 통합
- 개인 PC 2: 품질 결과 표시와 후속 푸셔 선택

개인 PC 1의 수확용 사과 인식과 harvest target 발행은 이 품질검사 흐름과 분리한다.

## 단계 A: 이미지 기반 OpenCV 확인

첫 합격 단계는 ROS 2나 tracker에 앞서 저장된 합성 RGB 이미지로 확인한다.

1. 배경과 사과가 함께 있는 RGB 이미지를 읽는다.
2. HSV saturation/value 범위로 전경 후보를 만든다.
3. morphology open/close 후 가장 큰 유효 contour를 사과로 선택한다.
4. contour, bounding box와 최소 외접원의 픽셀 직경을 계산한다.
5. 실제 렌더 직경을 아는 여러 size 시나리오로 픽셀-mm 선형 보정을 계산한다.
6. 픽셀 직경을 mm로 변환하고 크기 등급을 적용한다.
7. 원본 영상에 contour, bounding box, 픽셀 직경, mm 직경과 등급을 표시한다.

이 단계의 입력 제약은 다음과 같다.

- 고정 카메라와 고정 해상도
- 한 영상에 사과 한 개
- 사과와 saturation이 명확히 다른 배경
- 사과 전체가 영상 안에 들어옴
- 기준 이미지와 검사 이미지가 같은 카메라 pose와 렌더 설정을 사용함

OpenCV HSV 기본값은 초기 합성환경 시험값이며 실제 데이터 확인 후 조정한다.
픽셀값을 diameter_mm 필드에 직접 넣지 않는다.

## OpenCV와 YOLO 적용 기준

YOLO는 OpenCV에 포함된 사전학습 모델이 아니라 별도의 딥러닝 객체 검출·분할
모델 계열이다. YOLO 결과를 OpenCV로 후처리하거나 표시할 수 있지만 두 기술의
책임은 구분한다.

현재 단계 A는 다음 조건이므로 YOLO를 요구하지 않는다.

- 고정 카메라와 단순한 배경
- 한 화면에 사과 한 개
- 합성환경에서 사과와 배경의 saturation 차이가 분명함
- HSV mask, morphology와 contour만으로 사과가 안정적으로 검출됨

현재 OpenCV 책임:

- RGB/HSV 변환과 전경 mask 생성
- morphology 노이즈 제거
- contour, bounding box와 외접원 계산
- 픽셀 직경 측정
- 크기 보정, 등급 오버레이와 CSV 생성

다음 현상이 실제 Isaac Sim 또는 카메라 시험에서 반복되면 YOLO 도입을 검토한다.

- 배경이나 컨베이어 부품을 사과로 반복 오검출
- 조명·그림자·반사 변화에서 사과 검출 누락
- 붉은색 외 품종마다 HSV 규칙을 계속 수정해야 함
- 잎·가이드·다른 사과에 가려진 사과를 contour로 찾기 어려움
- 한 화면의 여러 사과를 각각 분리하고 apple_id에 연결해야 함

도입 시 일반 bounding box detection보다 사과별 외곽 mask를 제공하는 instance
segmentation을 우선 검토한다. YOLO mask는 사과 위치와 표면 범위를 제공하며,
OpenCV는 mask 후처리·blur 검사·시각화를 계속 담당한다.

YOLO만으로 실제 직경 mm가 계산되는 것은 아니다. YOLO 또는 OpenCV가 만든
사과 mask에 정렬된 depth와 CameraInfo를 적용해 3D 직경을 계산해야 한다.

    현재 단계
    OpenCV 검출 → 픽셀-mm 보정 → 크기 등급

    환경이 복잡해진 후속 단계
    YOLO instance segmentation → OpenCV 후처리
      → depth + CameraInfo 직경 계산 → 크기 등급

YOLO 학습을 시작하기 전 bounding box/mask annotation, 합성·실제 데이터 분리,
목표 검출률과 오검출 허용 기준을 확정해야 하며 해당 값은 현재 TBD다.

## 단계 B: RGB-D 및 ROS 2 통합

단계 A가 합격하면 GPU PC 2가 GPU PC 1의 raw RGB/depth/CameraInfo 스트림을
구독하도록 연결한다. 실제 운영 직경은 사과 mask의 유효 depth 픽셀을 CameraInfo로
3D 역투영해 계산한다. camera intrinsics를 코드 상수로 고정하지 않는다.

기존 InspectionImage와 quality inspection completed 경로는 이 RGB-D 통합을
위한 스캐폴딩이다. 모델 경로를 지정하지 않은 기본 실행에서는 착색·손상 신경망을
요구하지 않고 depth 기하 직경만 사용한다.

ROI/tracker와 다중 사과 처리는 단계 A 이후 연결한다. 동일 inspection에서
apple_id가 바뀌면 결과를 확정하지 않고 RECHECK를 발행한 뒤 세션을 정리한다.

## 크기 등급 규칙

현재 등급은 적도부 최대 직경 한 항목만 사용한다.

| 직경 | 등급 |
|---|---|
| 75mm 이상 | HIGH |
| 60mm 이상 75mm 미만 | MEDIUM |
| 60mm 미만 | LOW |

경계값 처리:

- 정확히 60mm는 MEDIUM
- 정확히 75mm는 HIGH

착색률, 손상 면적 또는 심각 결함 값은 현재 크기 등급을 바꾸지 않는다.
QualityResult의 color_ratio와 damage_area_cm2는 현재 MVP에서 NaN으로 발행한다.

## 크기 측정과 보정

### 단계 A 픽셀 보정

같은 카메라 조건에서 실제 렌더 직경을 알고 있는 여러 기준 사과를 검출해 다음
선형식을 구한다.

    estimated_diameter_mm = mm_per_pixel * detected_diameter_px + intercept_mm

한 장 기준의 pixels_per_mm 보정도 지원하지만 픽셀 양자화와 자세 변화에 민감하다.
권장 보정에는
58mm, 60mm, 62mm, 73mm, 75mm, 78mm처럼 두 경계의 아래·경계·위 데이터를
포함하고 각 시나리오 여러 자세의 픽셀 직경 중앙값을 사용한다. case 0으로
보정하고 case 1로 검증하며, 요청한 target 값이 아니라 metadata의
aggregate_measured_diameter_mm를 정답으로 사용한다. 허용 오차와 경계 주변
RECHECK 폭은 검증 후 확정하며 현재 TBD다.

### 단계 B RGB-D 측정

- 사과 mask와 정렬된 depth의 유효 픽셀을 사용한다.
- CameraInfo로 3D 역투영한 수평·수직 범위 중 큰 값을 가시 최대 직경으로 사용한다.
- depth가 0, NaN 또는 카메라 유효 범위 밖이면 계산에서 제외한다.
- 여러 유효 프레임을 사용할 때 직경은 통계적 중앙값을 사용한다.
- 짝수 개 프레임의 중앙값은 가운데 두 값의 평균이다.

## 프레임 선택

단계 A는 저장 이미지 한 장으로 전체 흐름을 먼저 확인한다. 단계 B에서는 동일 사과의
선명한 프레임을 최대 3장까지 사용할 수 있고 직경 중앙값을 사용한다.

프레임 선택 초기 조건:

- 사과 contour/mask가 영상 경계에 닿지 않음
- 사과의 90% 이상이 검사 ROI 안에 있음
- RGB-D 측정 시 유효 depth 픽셀 비율 80% 이상
- Laplacian variance 100 이상

90%, 80%, 100은 초기 시험값이며 실제 검증 후 조정한다. 유효 프레임이 없으면
UNCLASSIFIED, ID가 바뀌거나 다중 사과가 겹치면 RECHECK로 처리한다.

## 결과 및 예외 처리

- 크기 측정과 confidence가 유효하면 VALID와 크기 등급을 발행한다.
- OpenCV가 사과를 찾지 못하면 NO_DETECTION 디버그 상태로 기록하고 품질 결과를
  확정하지 않는다.
- apple_id 변경, 중복 detection 또는 두 사과 겹침은 RECHECK다.
- 일부 프레임 측정이 실패해도 유효 직경 프레임이 하나 이상이면 현재 MVP는 통합할
  수 있다.
- ROI 이탈 후 simulation time 0.5초 deadline 정책은 ROS 2 통합 단계에서 유지한다.
- deadline까지 결과가 없으면 유일한 최종 결과로 TIMEOUT을 발행한다.
- deadline 이후 끝난 계산은 LATE_RESULT와 inspection/frame 정보를 내부 로그에만
  남기며 중복 결과를 발행하지 않는다.
- 모든 ROS 2 시간 판정은 /clock과 use_sim_time true를 사용한다.

## 통신

    단계 A
    합성 RGB 파일
      → GPU PC 2 OpenCV 사과 검출
      → 크기 보정·등급 판정
      → contour/bounding box/직경/등급 오버레이 + CSV

    단계 B
    GPU PC 1 raw RGB/depth/CameraInfo
      → GPU PC 2 ROI/tracker 및 대표 프레임 선택
      → RGB-D 직경 측정과 크기 등급 통합
      → /quality/results

컨베이어 raw 토픽 이름과 정확한 QoS는
docs/architecture/ros2_interfaces.md에 따라 TBD로 유지한다.

## 후속 확장

크기 단일 분류가 합격한 뒤 다음 순서로 확장한다.

1. raw RGB ROS 2 구독과 디버그 오버레이 발행
2. ROI/tracker와 안정적인 apple_id
3. RGB-D 실제 직경 측정
4. 착색 mask와 착색률
5. 손상 mask와 손상 면적
6. 다중 프레임 표면 통합과 confidence 보정

후속 착색·손상 annotation 최소 단위는 사과 표면, 목표 착색 영역, 손상 영역,
무시 영역 mask와 심각 결함 여부다. 해당 항목이 실제 등급 규칙에 다시 포함될
시점과 경계값은 검증 데이터와 사용자 승인을 거쳐 확정한다.

## 미확정 사항

raw 컨베이어 카메라 토픽 이름과 QoS, OpenCV HSV 범위의 최종값, 픽셀 보정 허용
오차, 경계 주변 RECHECK 폭, tracker 연속성 기준과 다중 사과 복구 규칙은 TBD다.
실제 데이터로 크기 단일 분류가 합격하기 전에는 착색률·손상 면적을 현재 MVP 필수
조건으로 다시 올리지 않는다.
