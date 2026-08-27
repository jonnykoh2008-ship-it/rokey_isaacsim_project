# 품질 분류

## 현재 구현 범위

현재 GPU PC 2 품질검사는 목표 착색률로 등급을 판정한다. 크기는 함께 측정해
발행하지만 등급에는 사용하지 않는다. GPU PC 2는 위·왼쪽·오른쪽 고정 RGB-D
카메라 입력에서 동일 사과의 3방향 뷰를 수집하고, 목표 착색 mask를 실제 측정값
으로 변환한 뒤 사과 단위로 통합한다.

검출기는 `HIGH`, `MEDIUM`, `LOW`를 직접 출력하지 않는다. 출력은 목표 착색
mask와 confidence이며, 최종 등급은 승인된 품질 규칙이 측정값에 적용되어
결정된다. 착색률 등급 경계 80%/60%는 컨베이어 실측을 근거로 승인받은 시험값이며
경계 주변 `RECHECK` 폭은 현재 `TBD`다.

v2.0 소유권은 다음과 같다.

- GPU PC 1: Isaac Sim 컨베이어 물리와 raw RGB/depth/CameraInfo 발행
- GPU PC 2: 컨베이어 영상 수신, 사과 검출·추적, 착색 추론과 결과 통합
- 개인 PC 2: 품질 결과 표시와 후속 푸셔 선택

개인 PC 1의 수확용 사과 인식과 harvest target 발행은 이 품질검사 흐름과 분리한다.

## OpenCV 진단 경로

OpenCV 경로는 사과 검출, RGB-D 정렬 확인, 러버 반사 억제, 목표 착색 mask
생성과 진단 오버레이에 사용한다. 현재 등급 판정은 이 경로로 이루어지며, 학습
segmentation 모델을 도입하면 비교할 baseline이 된다.

1. 배경과 사과가 함께 있는 RGB 이미지를 읽는다.
2. HSV saturation/value 범위로 전경 후보를 만든다.
3. aligned depth로 컨베이어 러버 반사와 배경 후보를 제거한다.
4. morphology open/close 후 사과별 contour와 mask를 생성한다.
5. 목표 착색 mask를 사과 mask와 ignore mask 내부로 제한한다.
6. 원본 영상에 사과 contour, 착색 mask와 진단값을 표시한다.

이 단계의 입력 제약은 다음과 같다.

- 고정 카메라와 고정 해상도
- 한 검사 ROI에는 한 번에 사과 한 개만 존재함
- 검사 ROI 안에서 사과가 서로 접촉하거나 가리지 않음
- 사과 전체가 영상 안에 들어옴
- 기준 이미지와 검사 이미지가 같은 카메라 pose와 렌더 설정을 사용함

OpenCV HSV 값은 초기 시험값이며 품종이나 조명이 바뀌면 재검증한다. 목표 적색
판별은 hue 대역과 RGB 비율(R>=1.45G, R>=1.60B)로 하고, 밝기 절대 임계값에
의존하지 않는다. 절대 밝기를 쓰면 곡면의 그늘진 면이 통째로 빠져 완전히 빨간
사과가 34%로 측정된다.

## OpenCV와 YOLO 적용 기준

YOLO는 OpenCV에 포함된 사전학습 모델이 아니라 별도의 딥러닝 객체 검출·분할
모델 계열이다. YOLO 결과를 OpenCV로 후처리하거나 표시할 수 있지만 두 기술의
책임은 구분한다.

OpenCV는 다음 기능에 유지한다.

- 고정 카메라와 단순한 배경
- RGB-D 디코딩과 timestamp 검증
- depth 기반 배경·러버 반사 제거
- 사과 ROI/tracker와 3방향 뷰 품질 검사
- 목표 착색 mask 생성과 시각화

현재 OpenCV 책임:

- RGB/HSV/Lab 변환과 진단 mask 생성
- morphology 및 connected-component 후처리
- contour와 bounding box 생성
- 세 카메라 timestamp 동기화, blur, ROI 포함률과 유효 depth 비율 계산
- 착색 mask 오버레이와 검증 결과 생성

다음 현상이 실제 Isaac Sim 또는 카메라 시험에서 반복되면 YOLO 도입을 검토한다.

- 배경이나 컨베이어 부품을 사과로 반복 오검출
- 조명·그림자·반사 변화에서 사과 검출 누락
- 붉은색 외 품종마다 HSV 규칙을 계속 수정해야 함
- 잎·가이드·다른 사과에 가려진 사과를 contour로 찾기 어려움
- 한 화면의 여러 사과를 각각 분리하고 apple_id에 연결해야 함

학습 모델을 도입하는 경우 사과 ROI를 입력으로 받아 목표 착색 mask를 출력한다.
모델 입력은 RGB 640×640 resize/letterbox를 초기 기준으로 사용하고 배포 형식은
ONNX, GPU PC 2 실행 백엔드는 ONNX Runtime CUDA를 기본으로 한다. 학습 전
annotation 감사, 시나리오 단위 데이터 분리와 오검출 허용 기준을 확정해야 하며
정확한 합격값은 `TBD`다.

## RGB-D 및 ROS 2 통합

GPU PC 2의 adapter는 GPU PC 1이 발행한 위·왼쪽·오른쪽 raw RGB-D/CameraInfo를
받아 사과 mask와 ignore mask를 구성하고 내부 `InspectionImage`로 전달한다. 각
뷰의 RGB와 depth는 동일 픽셀 좌표계와 정확히 같은 timestamp를 사용한다. 카메라
간 timestamp의 최댓값과 최솟값 차이가 20ms 이내인 세 뷰를 같은 촬영 묶음으로
사용한다. camera intrinsics는 코드 상수로 고정하지 않는다.

GPU PC 2는 목표 착색 mask와 aligned depth/CameraInfo를 결합해 착색률과 직경을
계산한다. 착색률은 유효 사과 표면 중 목표 착색 mask의 비율이며 ignore 영역은
분모·분자에서 제외한다.

ROI/tracker가 `inspection_id`와 `apple_id`를 유지한다. 동일 inspection에서
apple_id가 바뀌면 결과를 확정하지 않고 RECHECK를 발행한 뒤 세션을 정리한다.

## 품질 측정과 등급 규칙

등급은 착색률 하나로 결정한다. 크기는 함께 측정해 발행하지만 등급 판정에는
사용하지 않는다. 손상은 현재 판정 대상이 아니다.

- 착색률: 모든 유효 프레임의 목표 착색 픽셀 수 합을 유효 사과 표면 픽셀 수
  합으로 나눈 값(면적 가중). 뷰별 비율의 평균이 아니다.
- 착색률 `HIGH`: 80% 이상
- 착색률 `MEDIUM`: 60% 이상 80% 미만
- 착색률 `LOW`: 60% 미만
- 크기: 직경을 측정해 `QualityResult.diameter_mm`으로 발행하되 등급에는 쓰지
  않는다.
- 손상 면적, 심각 결함: 판정에 사용하지 않으며 `damage_area_cm2`는 NaN이다.

경계값 처리:

- 정확히 80%는 `HIGH`
- 정확히 60%는 `MEDIUM`

크기 규칙에서 정확히 75mm가 `HIGH`인 것과 같이, 경계값은 더 좋은 등급에
포함한다.

80%와 60%는 사용자 승인을 받은 시험값이며 영구 확정값이 아니다. 근거는 컨베이어
실측이다. 잘 착색된 사과가 84~87%, 노란빛이 도는 사과가 54~56%로 나와 두 무리가
각 경계에서 4~7%p 여유를 두고 떨어졌고, 이는 관측된 산포(약 ±1.5%p)보다 충분히
크다. 품종이나 조명이 바뀌면 다시 검증해야 한다.

`UNCLASSIFIED` 또는 `REJECT` 착색 등급은 사용하지 않는다. 경계 주변 `RECHECK`
폭은 `TBD`다.

### 측정할 수 없는 표면

정반사로 하얗게 뜬 영역과 색을 분간할 수 없이 어두운 영역은 `ignore_mask`로
표시해 착색률의 분모에서 제외한다. 이 영역을 분모에 남기면 완전히 빨간 사과도
78%로 측정된다. 실측에서 깊은 그늘이 표면의 약 15%를 차지했다.

## 3방향 뷰 선택

`conv_rsd455`는 위쪽, `conv_rsd455_01`은 왼쪽, `conv_rsd455_02`는 오른쪽 표면을
촬영한다. 동일 `(inspection_id, apple_id)`에서 simulation timestamp 차이가 최대
20ms인 세 뷰를 한 묶음으로 사용하며 `frame_index`는 위쪽 0, 왼쪽 1, 오른쪽 2로
고정한다.

뷰 선택 초기 조건:

- 사과 contour/mask가 영상 경계에 닿지 않음
- 사과의 90% 이상이 검사 ROI 안에 있음
- RGB-D 측정 시 유효 depth 픽셀 비율 80% 이상
- Laplacian variance 100 이상
- 세 카메라가 동일한 `apple_id`를 검출함

90%, 80%와 100은 초기 시험값이며 실제 검증 후 조정한다. 세 뷰 중 하나라도
누락되거나 유효하지 않으면 `INSUFFICIENT_VIEWS`로 처리한다.

사과 단위 착색률은 `docs/open_questions_gpu_pc2.md` G2-03 개정에 따라 면적
가중 합산 `sum(C_i) / sum(A_i)`를 사용한다. 뷰별 비율의 평균은 뷰마다 보이는
표면 크기가 다른데도 균등 가중하므로 표면 비율의 추정량이 되지 않는다.

이 값은 롤러 위에서 굴러가는 사과를 통과 구간의 여러 순간에 촬영해 합친
것이므로, 바닥 접촉면을 포함한 **전체 표면**의 착색률 추정값이다. 컨베이어가
평벨트였을 때는 바닥면이 영원히 보이지 않아 3방향 관측 표면에 한정되었으나,
롤러 전환으로 그 제약이 없어졌다.

추정이 편향되지 않는 근거는 두 가지다. 첫째, 비율이므로 같은 표면 조각이 여러
프레임에 나와도 분자와 분모에 함께 들어가 편향을 만들지 않는다. 둘째, 구 표면
조각의 투영 면적은 시선축과 이루는 각의 cos에 비례하므로, 자세가 고르게 섞이면
회전 대칭성에 의해 모든 조각의 기대 가중치가 같아진다. 실측에서 사과의 회전은
고정축 자전이 아니라 축이 계속 바뀌는 텀블링이어서 이 조건을 만족한다.

## 결과 및 예외 처리

- 착색률 측정과 confidence가 유효하면 품질 규칙을 적용해 VALID 결과를 발행한다.
- OpenCV가 사과를 찾지 못하면 NO_DETECTION 디버그 상태로 기록하고 품질 결과를
  확정하지 않는다.
- apple_id 변경, 중복 detection 또는 두 사과 겹침은 RECHECK다.
- 한 뷰라도 검출 또는 추론에 실패하면 `INSUFFICIENT_VIEWS`로 처리한다.
- ROI 이탈 후 simulation time 0.5초 deadline 정책은 ROS 2 통합 단계에서 유지한다.
- deadline까지 결과가 없으면 유일한 최종 결과로 TIMEOUT을 발행한다.
- deadline 이후 끝난 계산은 LATE_RESULT와 inspection/frame 정보를 내부 로그에만
  남기며 중복 결과를 발행하지 않는다.
- 모든 ROS 2 시간 판정은 /clock과 use_sim_time true를 사용한다.

## 통신

    GPU PC 1 위·왼쪽·오른쪽 raw RGB/depth/CameraInfo
      → timestamp 간격 최대 20ms인 3방향 뷰
      → /quality/inspection_images + /quality/inspection_completed
      → GPU PC 2 목표 착색 mask 생성
      → 뷰별 착색률 평균 + 품질 규칙
      → /quality/results

컨베이어 raw 토픽 이름은 docs/architecture/ros2_interfaces.md를 따르며 정확한 QoS는
`TBD`로 유지한다.

## 구현 순서

1. 컨베이어와 동일한 렌더 조건의 착색 데이터셋 재생성
2. 정상 사과, 착색 및 ignore mask annotation 감사
3. 시나리오 단위 train/validation/test 분리
4. 착색 segmentation 학습과 독립 test 평가
5. ONNX export 및 GPU PC 2 ONNX Runtime CUDA 검증
6. ROI/tracker, 3방향 뷰 동기화와 사과 단위 통합
7. `/quality/results` 다중 PC 시험

## 미확정 사항

착색률 경계 주변 `RECHECK` 폭, 착색 오검출 허용값, tracker 연속성 기준과 다중
사과 복구 규칙은 `TBD`다. 데이터셋 규모와 도메인 무작위화 범위도 검증 결과와
사용자 승인을 거쳐 확정한다.

손상 판정은 현재 범위에서 제외했다. 컨베이어 실측에서 손상 검출기가 실제로
구분한 것은 결함이 아니라 빨갛지 않은 표면의 비율이었고, 그것은 착색률로
측정하는 편이 이름과 내용이 일치한다. 손상을 다시 다루려면 손상과 미착색을
색만으로 분리할 수 없다는 한계를 먼저 해결해야 하며, 학습 기반 segmentation이
그 후보다.
