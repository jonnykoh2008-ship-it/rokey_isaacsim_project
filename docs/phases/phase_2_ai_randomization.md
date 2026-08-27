# 2차 개발: AI 및 도메인 무작위화

## 목표

사과와 환경 변화에 대응할 수 있도록 수확용 인식, 접근 계획 및 품질 모델의 일반화 성능을 높인다.

## 도메인 무작위화

- 사과 위치 및 크기
- 사과 표면, 착색, 손상, 윤택
- 조명, 배경 및 카메라 노이즈
- 가지와 잎의 배치
- 마찰 및 접촉 파라미터의 허용 범위

## 수확 인식

- Isaac Sim Replicator 데이터 생성
- 개인 PC 1의 OpenCV/YOLOv8 기반 사과 검출
- 개인 PC 1의 RGB-D 기반 3D 위치 계산 및 `world` target 발행
- GPU PC 1의 target 세대·timestamp 검증
- 다중 사과 ID 도입
- 작은 가지와 잎의 인식 후보 추출은 개인 PC 1에서 수행할 수 있으나, planning
  obstacle 채택과 safety margin 적용은 GPU PC 1이 결정

## 접근 및 파지

- 기본 `+Z` 접근 실패 시 다른 접근 각도 탐색
- GPU PC 1의 Lula RRT 기반 전역 경로 후보 탐색 및 RMPflow 실행
- 가지를 planning obstacle로 사용하고, 잎은 PhysX collision과 planning obstacle에서
  제외한다. 잎은 occlusion/confidence 판단에만 사용한다.
- 사과 위치·크기 변화에 대한 파지 안정성 향상
- 필요 시 강화학습 적용

RRT seed, sampling limit, collision-check 해상도, trajectory 제약 및 재계획
정책은 GPU PC 1에서 시험한다. 개인 PC 1은 검출·좌표 계산 성능과 target
timestamp 품질을 시험한다.

## 다중 사과 연속 수확

- 다중 사과의 ID·대기열·실패 후순위 재시도 및 접촉 이후 안전 정지 동작은
  `docs/features/harvest_perception.md`와 `docs/features/harvesting.md`를 따른다.
- 이 단계의 각 사과 stem FixedJoint에는 승인된 break force `15N`, break torque
  `2Nm`를 동일하게 적용한다. 파손은 `TWIST` 또는 `PULL`에서 확인하며,
  `APPROACH`·`GRASP` 중 파손은 조기 파손 실패로 처리한다.

## 품질 분류

- 현재 품질 분류는 크기를 사용하지 않고 목표 착색률과 손상만 처리한다.
- GPU PC 1은 실제 컨베이어 카메라 pose, 조명, 러버 재질과 반사를 포함한 RGB,
  aligned depth, CameraInfo 및 ground-truth mask를 생성한다.
- 데이터 annotation은 사과 표면, 목표 착색, 손상, ignore mask와 심각 결함 여부를
  포함한다. 완전 정상 사과 시나리오는 모든 시점의 손상 mask가 0이어야 한다.
- 크기 변화는 등급 label이 아니라 사과 검출·segmentation 일반화를 위한 도메인
  무작위화 요소로만 사용할 수 있다.
- 요청 착색률·손상 면적과 실제 렌더 측정값이 허용 범위에 들어오지 않은 시나리오는
  학습 데이터에서 제외한다. 허용 범위는 `TBD`다.
- 동일 `group_id`의 모든 시점은 train/validation/test 중 한 split에만 둔다.
- 품질 모델은 목표 착색 mask와 손상 mask/confidence를 출력하고 ONNX로 배포한다.
- GPU PC 2는 유효 대표 프레임 4~6장을 추론해 착색률 평균과 손상 면적 최댓값을
  사과 단위로 통합한다.

## 완료 기준

데이터셋 규모, 인식 정확도, 파지 성공률 및 평가 시나리오는 TBD다.
