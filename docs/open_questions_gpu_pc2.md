# GPU PC 2 구현 논의사항

> 상태 안내 (2026-08-25): 현재 품질검사는 크기 판정을 제외하고 착색률·손상
> segmentation과 대표 프레임 4~6장 통합을 구현 범위로 사용한다. OpenCV는 RGB-D
> 사과 검출, 러버 반사 제거, 프레임 품질 검사와 모델 mask 후처리에 유지한다. 현재
> 구현 범위와 인터페이스의 기준은 `docs/features/quality_grading.md`,
> `docs/features/conveyor.md`, `docs/architecture/ros2_interfaces.md`가
> 우선한다.

## 목적

GPU PC 2의 품질 영상 추론과 사과 단위 결과 통합을 구현하기 전에 결정해야 할 사항을 관리한다. 이 문서는 미확정 값을 임의로 확정하지 않으며, 합의가 끝난 내용은 관련 기능 또는 아키텍처 문서에 반영한다.

## 기준 문서

- `docs/architecture/ros2_interfaces.md`
- `docs/architecture/tf_frames.md`
- `docs/architecture/hardware_network.md`
- `docs/features/quality_grading.md`
- `docs/features/conveyor.md`
- `docs/assets/asset_requirements.md`
- `docs/phases/phase_1_mvp.md`

인터페이스, 시간 및 네트워크에 관한 설명이 중복될 경우 아키텍처 문서를 우선한다. 품질 판정 동작은 `docs/features/quality_grading.md`를 기준으로 한다.

## 구현을 막는 결정사항

### G2-01. Depth와 CameraInfo 전달 계약

상태: `DECIDED`

- `InspectionImage`는 압축 RGB, 사과 mask, ignore mask, aligned depth와 `CameraInfo`를 한 메시지로 전달한다.
- 모든 영상 성분은 같은 픽셀 좌표계와 header를 사용한다.
- 손상 면적 계산은 사과 mask, 정렬된 depth와 camera intrinsics를 요구한다.

결정할 내용:

- `InspectionImage`에 depth와 camera intrinsics를 포함할지
- 별도의 동기화된 토픽으로 전달할지
- GPU PC 1에서 손상 면적을 계산하고 GPU PC 2에는 측정값만 전달할지

영향:

- 입력 메시지 구조
- GPU PC 1과 GPU PC 2의 기능 경계
- 손상 면적 계산 위치
- 네트워크 대역폭

결정:

- GPU PC 1은 대표 프레임의 RGB, 사과 mask, 정렬된 depth, CameraInfo를 GPU PC 2로 전달한다.
- GPU PC 2가 RGB/depth 기반 품질 추론과 손상 면적 계산을 담당한다.
- 품질검사 연산을 GPU PC 2에 집중해 PC 간 기능 경계를 명확히 한다.
- 현재 범위에서는 RGB, 사과 mask, ignore mask, 정렬된 depth, CameraInfo를 하나의
  custom `InspectionImage`에 함께 포함해 동일 대표 프레임 단위로 전달한다.
- depth는 optical Z-depth, `16UC1` millimeter, invalid 0, `compressedDepth png`를 사용한다.

### G2-02. 프레임별 품질 모델 입출력

상태: `DECIDED`

품질 모델은 등급을 직접 출력하지 않고 품질 측정값을 산출하는 구조로 확정했다. 다만 confidence threshold, 입력 해상도, 세부 annotation 규칙과 실행 백엔드는 시험 및 모델 구현 단계에서 조정한다.

결정할 내용:

- 모델이 직접 등급을 출력할지, 착색률·손상 면적·심각 결함을 출력할지
- 프레임별 confidence의 의미와 계산 방식
- confidence가 기준보다 낮을 때 사용할 상태
- 현재 모델의 입력 해상도와 전처리 규칙
- 모델 파일 형식과 실행 백엔드

결정:

- 모델은 `HIGH`, `MEDIUM`, `LOW` 등급을 직접 출력하지 않는다.
- 프레임별로 목표 착색 mask, 손상 mask, 심각 결함 여부와 각 confidence를 출력한다.
- 손상 면적은 모델의 손상 mask, 정렬된 depth와 camera intrinsics를 이용해 GPU
  PC 2에서 계산한다. 크기는 등급 판정에 사용하지 않는다.
- 최종 `HIGH`/`MEDIUM`/`LOW` 등급은 사전에 정의한 품질 기준과 측정값을 이용한 규칙 기반 판정으로 결정한다.
- 이 방식은 등급 판정 근거를 추적할 수 있고, 품질 기준 변경 시 모델 전체를 다시 학습하지 않고 판정 규칙을 조정할 수 있도록 하기 위한 것이다.
- 모델 입력은 RGB 기준 640×640으로 resize/letterbox하고, 픽셀 값은 모델 학습
  설정과 동일하게 정규화한다. Depth는 신경망 입력에 직접 넣지 않고 손상 면적
  계산용 기하 정보로 사용한다.
- 프레임 confidence는 품질 측정에 사용된 모델 출력들의 유효 confidence 평균으로 정의한다. 초기 유효 threshold는 0.5로 두며, 핵심 측정 항목의 confidence가 0.5 미만이면 해당 프레임의 해당 측정값을 무효 처리한다.
- 낮은 confidence 때문에 사과 단위 유효 프레임이 4장 미만이 되면 `INSUFFICIENT_VIEWS`, 손상 면적 유효 프레임이 2장 미만이면 기존 정책대로 `RECHECK`를 사용한다.
- 모델 배포 형식은 ONNX를 기본으로 하고 GPU PC 2에서는 ONNX Runtime CUDA를
  실행 백엔드로 사용한다. 이후 성능이 부족하면 TensorRT 변환을 최적화 단계에서
  검토한다.
- annotation은 사과 표면, 목표 착색, 손상, 무시 영역 mask와 심각 결함 여부를
  사용한다. 현재 대상은 목표 적색과 정상적인 노랑·연녹색 과피가 함께 나타날 수
  있는 품종군이며 정상적인 과피 거침은 손상에서 제외하고 scab은 손상에 포함한다.

### G2-03. 다중 프레임 통합 규칙

상태: `DECIDED`

결정 내용:

- 착색률은 모든 유효 프레임의 착색 픽셀 수 합을 유효 표면 픽셀 수 합으로 나눈
  면적 가중값 `sum(C_i) / sum(A_i)`을 사용한다.

  개정 사유: 최초 확정은 "프레임별 측정값의 평균"이었다. 컨베이어 2가 평벨트에서
  롤러형으로 바뀌면서 목표가 "카메라에 보인 세 면의 착색률"에서 "전체 표면의
  착색률"로 바뀌었고, 평균은 새 목표의 추정량이 되지 못한다. 뷰마다 보이는 표면
  크기가 다른데 균등 가중하기 때문이다. 실측에서 한 사과의 세 뷰가 각각
  0.188 / 0.892 / 0.708 이었고 평균은 0.596, 면적 가중은 0.527 이었다.

  면적 가중이 불편추정량인 근거: 비율이므로 같은 표면 조각이 여러 프레임에
  나와도 분자와 분모에 함께 들어가 편향을 만들지 않으며, 구 표면 조각의 투영
  면적이 시선축과 이루는 각의 cos 에 비례하므로 자세가 고르게 섞이면 회전
  대칭성에 의해 모든 조각의 기대 가중치가 같아진다.

  실측 근거: 한 순간만 쓰면 껍질의 36.2% 만 60도 이내로 관측되고(최대 사각
  155.8도) 통과 중 착색률이 0.68~0.99 로 흔들려(표준편차 0.079) 등급 경계를
  넘나든다. 순간 8개를 합치면 커버리지 99.6%, 오차 약 2.8%p 가 된다.
- 손상 면적(손상률)은 기존 확정안대로 대표 프레임별 유효 측정값 중 최댓값을 사용한다.
- 심각 결함은 유효 프레임 중 한 프레임에서라도 검출되면 `true`로 통합한다.
- 개별 프레임에서 `HIGH`, `MEDIUM`, `LOW` 등급을 각각 확정하지 않는다. 프레임별 측정값을 사과 단위로 통합한 뒤 최종 측정값에 품질 규칙을 적용하여 등급을 한 번만 결정한다.
- 일부 프레임 추론이 실패하더라도 최소 4장의 대표 프레임이 정상 처리되면 사과 단위 결과 통합을 수행한다. 정상 처리 프레임이 4장 미만이면 기존 정책에 따라 `INSUFFICIENT_VIEWS`로 처리한다.
- 최종 confidence는 유효 프레임별 confidence의 평균을 기본 방식으로 사용한다. confidence의 정확한 의미와 계산 방식은 G2-02의 세부 모델 설계 및 시험 결과에 따라 조정할 수 있다.

선택 근거:

- 착색률은 여러 방향의 관측을 평균하여 특정 시점의 편향을 줄인다.
- 손상과 심각 결함은 한 방향에서만 보이는 결함을 놓치지 않도록 보수적으로 통합한다.
- 프레임별 등급을 투표하는 대신 통합 측정값으로 최종 등급을 계산하여 G2-02에서 확정한 측정값 기반 품질 판정 구조를 유지한다.

### G2-04. 검사 완료와 deadline 시작 신호

상태: `DECIDED`

결정:

- GPU PC 1은 검사 대상 사과가 카메라 ROI를 이탈하면 `/quality/inspection_completed`에 `InspectionCompleted`를 발행한다.
- 완료 이벤트에는 `header`, `inspection_id`, `apple_id`, `total_frames`를 포함한다.
- GPU PC 2는 검사 완료 이벤트의 ROI 이탈 simulation timestamp를 결과 deadline의 시작점으로 사용하며, 결과 deadline은 해당 시점부터 simulation time 0.5초다.
- 검사 완료 이벤트를 수신했을 때 누락된 `frame_index`가 있으면 GPU PC 2는 deadline까지 해당 프레임의 도착을 기다린다.
- deadline까지 도착하지 않은 프레임은 실패 프레임으로 처리한다. 이후 정상 처리 가능한 대표 프레임이 4장 이상이면 수신된 유효 프레임으로 결과를 계산하고, 4장 미만이면 `INSUFFICIENT_VIEWS`로 처리한다.
- 완료 이벤트 전에는 모든 프레임이 도착했더라도 결과를 확정하지 않는다.

선택 근거:

- `total_frames`만으로는 ROI 이탈 시점과 deadline 시작 시점을 명확하게 알 수 없으므로 검사 완료 이벤트를 명시적으로 전달한다.
- `/clock` 기반 simulation timestamp를 사용하여 기존 결과 deadline 및 `use_sim_time:=true` 계약과 일관성을 유지한다.
- 프레임 누락 시 즉시 실패시키지 않고 기존 0.5초 deadline까지 수신 기회를 주어 다중 PC 통신의 일시적 지연을 허용한다.

### G2-05. 예외 상태 판정 책임

상태: `DECIDED`

결정:

- GPU PC 2는 G2-04의 ROI 이탈 simulation timestamp를 기준으로 0.5초 deadline을 계산한다.
- deadline까지 최종 결과를 생성하지 못하면 해당 검사의 유일한 결과로 `TIMEOUT`을 발행한다.
- deadline 이후 정상 추론이 끝나면 `LATE_RESULT`를 내부 로그에만 기록하고 별도 결과 메시지를 발행하지 않는다.
- `ID_MISMATCH`는 컨베이어 tracker ID와 rigid body prim 정보를 모두 확인할 수 있는 공정/추적 관리 노드에서 판정한다. GPU PC 2가 직접 비교하지 않는다.
- GPU PC 2는 검사 완료 이벤트와 프레임의 `apple_id` 일치 여부만 검증하며, 동일 검사 내부에서 ID가 다르면 입력 오류로 거부하고 상태 로그를 남긴다.

선택 근거:

- 시간 기반 예외는 실제 추론 완료 시점을 알고 있는 GPU PC 2가 가장 명확하게 판정할 수 있다.
- 물체 추적 ID의 물리적 일치 여부는 품질 추론 노드보다 공정/추적 정보를 가진 노드가 책임지는 것이 기능 경계상 적절하다.
- deadline 이후 정상 결과를 다시 최종 결과로 사용하면 분류 제어 측에서 같은 사과에 대해 결과가 뒤집힐 수 있으므로 한 검사에는 하나의 최종 상태만 사용한다.

### G2-06. ROS 2 QoS

상태: `DECIDED`

결정:

- `/quality/inspection_images`는 `RELIABLE`, `VOLATILE`, `KEEP_LAST`, `depth=6`을 사용한다.
- `/quality/inspection_completed`도 `RELIABLE`, `VOLATILE`, `KEEP_LAST`, `depth=10`을 사용한다.
- `/quality/results`는 `RELIABLE`, `VOLATILE`, `KEEP_LAST`, `depth=10`을 사용한다.
- 현재 범위에서는 재전송으로 인한 약간의 지연보다 대표 프레임 또는 최종 결과
  유실을 더 큰 위험으로 본다.
- 실제 다중 PC 시험에서 재전송 지연이 0.5초 deadline을 반복적으로 침범하면 이미지 토픽만 `BEST_EFFORT`로 변경하는 비교 시험을 수행한다.

선택 근거:

- 대표 프레임은 사과당 최대 6장으로 제한되어 있어 무제한 센서 스트림과 성격이 다르며, 한 장의 유실도 최소 4장 조건에 영향을 줄 수 있다.
- 결과 메시지는 분류 제어의 입력이므로 신뢰성 우선이 적절하다.
- `VOLATILE`을 사용해 새로 접속한 노드에 과거 사과 결과나 오래된 이미지를 재전송하지 않는다.

## 명세 간 불일치 또는 보완 필요 사항

### G2-07. 대표 프레임 선택 기준의 상태

상태: `DECIDED`

결정:

- 구현 기준은 `docs/features/quality_grading.md`와 `docs/features/conveyor.md`를 우선한다.
- 초기 시험값으로 ROI 포함률 90% 이상, 유효 depth 80% 이상, Laplacian variance
  100 이상, 대표 프레임 간 회전 차이 45° 이상을 적용한다.
- 첫 6개 후보 프레임을 그대로 사용하는 기존 데모 방식은 제거하고 기능 명세의 대표 프레임 선택 규칙에 맞춘다.
- 위 수치는 영구 기준이 아니라 초기 시험값이며 실제 촬영 결과에 따라 조정할 수 있다.

선택 근거:

- 현재 문서 자체가 기능 명세를 기준 문서로 지정하고 있으므로 README의 오래된 `TBD` 설명보다 기능 명세를 우선하는 것이 일관적이다.
- GPU PC 2의 품질 추론 성능을 비교하려면 GPU PC 1에서 입력 프레임 품질을 일정하게 관리해야 한다.

### G2-08. 개인 PC 명칭

상태: `DECIDED`

결정:

- 시스템 문서 전체에서 개인 장비 명칭은 `개인 PC 1`, `개인 PC 2`로 통일한다.
- `hardware_network.md`의 `개인 PC 3`, `개인 PC 4` 표기는 문서 불일치로 보고 각각 `개인 PC 1`, `개인 PC 2`로 수정한다.
- 분류 제어·모니터링 장비 `10.10.0.4`는 `개인 PC 2`로 사용한다.

선택 근거:

- `system_overview.md`와 `ros2_interfaces.md`에서 이미 개인 PC 1·2 체계를 사용하고 있어 이를 기준으로 맞추는 편이 변경 범위가 작고 이해하기 쉽다.

### G2-09. RGB-D 구성요소의 header

상태: `DECIDED`

결정:

- 기준 timestamp와 frame ID는 `InspectionImage.header`를 단일 기준으로 사용한다.
- `image.header`, `apple_mask.header`, `ignore_mask.header`, `aligned_depth.header`, `camera_info.header`에도 동일한 timestamp와 frame ID를 복사한다.
- frame ID는 해당 뷰를 촬영한 카메라의 optical frame을 사용한다. 컨베이어 2는
  카메라 3대이므로 `quality_camera_top_optical_frame`,
  `quality_camera_left_optical_frame`, `quality_camera_right_optical_frame`
  중 하나다. 한 `InspectionImage`는 한 카메라에서 나오므로 그 메시지의 여섯
  header는 여전히 모두 같아야 한다.
- `frame_index`는 카메라 위치로 고정한다. 위쪽 `conv_rsd455`는 0, 왼쪽
  `conv_rsd455_01`은 1, 오른쪽 `conv_rsd455_02`는 2이며 `total_frames`는 3이다.
  검출 순서로 매기면 한 면이 빠졌을 때 index가 다른 면을 가리키게 된다.
- `InspectionCompleted`는 카메라가 아니라 컨베이어의 ROI 이탈 사건이므로
  optical frame이 아니라 `conveyor_inspection_roi` frame을 사용한다.
- GPU PC 2는 여섯 header 중 하나라도 다르면 해당 프레임을 거부한다.
- 중복 header는 현재 custom message에서 유지한다.

선택 근거:

- 하나의 기준 header를 명시하면 프레임 동기화와 로그 추적이 단순해진다.
- 기존 `CompressedImage` 구조를 즉시 변경하지 않아도 되면서 두 timestamp가 달라지는 오류를 조기에 검출할 수 있다.

## 구현 시험 후 확정할 사항

### G2-10. 카메라 실행 프로파일과 intrinsics

상태: `PROVISIONAL`

초기 구현 기준:

- 1280×720, 30fps를 기본 실행 프로파일로 사용한다.
- RGB와 depth는 동일 해상도 기준으로 정렬해 GPU PC 2에 전달한다.
- camera intrinsics와 장착 transform은 실행 시 사용되는 실제 카메라 설정값을 메시지/TF에서 읽고 코드에 상수로 고정하지 않는다.
- aligned depth는 optical Z-depth이며 `16UC1; compressedDepth png` 계약을 사용한다.
- 대표 프레임 품질, 착색률·손상률 측정 안정성, 네트워크 사용량을 측정한 뒤
  해상도와 FPS를 최종 확정한다.

검증 기준:

- 4~6장 대표 프레임을 안정적으로 확보할 수 있는지 확인한다.
- 0.5초 결과 deadline을 반복적으로 침범하지 않는지 확인한다.
- 착색률 및 손상률 측정 오차가 프로젝트 허용 범위 안에 들어오는지 확인한다.

### G2-11. 네트워크 장애 감지

상태: `PROVISIONAL`

초기 구현 기준:

- 공정 결과 deadline은 기존대로 Isaac Sim `/clock`을 사용한다.
- 노드/네트워크 생존 여부는 별도의 wall-time heartbeat/watchdog으로 감지한다.
- 관련 노드는 1초 주기로 heartbeat를 발행하고, 연속 3초 동안 heartbeat를 받지 못하면 통신 장애 상태로 판단한다.
- 통신 복구 시 자동 재연결을 허용하되, 장애 중 진행되던 사과 검사는 재사용하지 않고 새 검사부터 정상 처리한다.

선택 근거:

- simulation time이 정지하거나 느려지는 상황에서도 실제 PC 또는 네트워크 장애는 감지되어야 하므로 wall time이 필요하다.
- 1초/3초 기준은 초기 디버깅에 충분히 단순하며 실제 통신 시험에서 조정 가능하다.

### G2-12. 동일 ID 복구와 다중 사과

상태: `PROVISIONAL`

현재 결정:

- 검사 ROI 안에 서로 접촉하거나 가리지 않는 사과를 최대 2개까지 허용한다.
- 각 사과는 독립 `inspection_id`와 `apple_id`를 유지하며 한 검사 세션에는 동일
  `apple_id`의 프레임만 허용한다.
- 두 사과가 접촉·중첩되어 mask를 분리할 수 없으면 해당 검사를 `RECHECK`로 처리한다.
- 검사 도중 ID가 사라졌다가 다시 나타나는 자동 ID 복구는 현재 수행하지 않는다.
  동일 ID가 끊기면 현재 검사를 종료 또는 실패 처리하고 새 검사로 시작한다.

선택 근거:

- 현재 대표 프레임 통합, deadline, 품질 결과 구조가 사과 단위 검사에 초점을 맞추고 있어 다중 객체 복구까지 포함하면 추적 문제와 품질 추론 문제를 동시에 해결해야 한다.
- 최대 2개로 범위를 제한하면 품질 추론과 장기 ID 복구 문제를 분리하면서 현재
  컨베이어 운용 조건을 검증할 수 있다.

## 현재 확정되어 구현에 사용할 수 있는 항목

- GPU PC 2 역할: 품질 영상 추론 및 사과 단위 결과 통합
- 입력 토픽: `/quality/inspection_images`
- 출력 토픽: `/quality/results`
- custom interface 패키지: `appleproj_interfaces`
- 시간 기준: Isaac Sim `/clock`
- 모든 ROS 2 노드: `use_sim_time:=true`
- 미들웨어: ROS 2 Jazzy, Fast DDS
- GPU PC 2 IP: `10.10.0.2`
- 통합 시험 `ROS_DOMAIN_ID=101`
- 등급: `HIGH`, `MEDIUM`, `LOW`
- 대표 프레임: 최소 4장, 최대 6장
- 대표 프레임 부족 상태: `INSUFFICIENT_VIEWS`
- 손상 면적 유효 측정 프레임이 2장 미만일 때: `RECHECK`
- 결과 deadline: ROI 이탈 후 simulation time 0.5초
- MVP에서는 푸셔 및 물리 분류를 구현하지 않음

## 결정 기록 양식

각 항목을 확정할 때 다음 내용을 기록한다.

- 결정 날짜:
- 결정 참여자:
- 선택한 방식:
- 선택 근거:
- 영향을 받는 문서:
- 영향을 받는 코드와 인터페이스:
- 검증 방법:
