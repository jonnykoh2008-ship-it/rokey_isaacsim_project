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

## 품질 분류

- 현재 선행 MVP는 크기·위치·자세·조명을 바꾼 합성 RGB로 OpenCV 사과 검출과
  크기 단일 등급을 검증한다.
- 58/60/62mm와 73/75/78mm처럼 크기 경계 아래·경계·위 데이터를 같은 카메라
  조건에서 생성해 픽셀-mm 보정과 경계 혼동을 확인한다.
- 크기 단일 검증 후 raw RGB-D 통신과 실제 단위 직경 측정을 연결한다.
- 착색·손상 도메인 무작위화와 segmentation 모델 학습은 후속 확장으로 진행한다.
- 후속 단계에서 다중 프레임 결과 통합, 손상 면적, confidence와 `RECHECK`
  정책을 확정한다.

## 완료 기준

데이터셋 규모, 인식 정확도, 파지 성공률 및 평가 시나리오는 TBD다.
