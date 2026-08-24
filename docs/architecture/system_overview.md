# 시스템 개요

## 목적

Isaac Sim에서 단일 사과나무의 사과를 협동로봇으로 수확하고 컨베이어에 배치한 뒤, 영상 기반 품질 등급을 산출한다. 수확 위치 인식과 품질 검사는 기능적으로 분리한다.

## 전체 흐름

```text
GPU PC 1 카메라 RGB-D 발행
  → 개인 PC 1 사과 검출·depth projection·world 좌표 계산
  → GPU PC 1 목표 검증 및 충돌 없는 접근 경로 계획
  → 파지
  → 손목 45° 회전
  → 로봇의 직선 당김
  → 줄기 분리
  → 컨베이어 1 저상 배치
  → 컨베이어 2 촬영·추론
  → 컨베이어 3 품질 결과 확인·배출
```

## 주요 구성

- 로봇: Doosan M0617, 6DOF
- 그리퍼: Robotiq AGS-001-MTCP 3-finger soft gripper의 rigid finger + compliant contact 근사
- 카메라: 베이스, arm, 컨베이어 상단에 Intel RealSense D455
- 환경: 사과나무 1그루, 사과 1개, 로봇 1개, 1차 MVP용 컨베이어 3모듈
- 모션: GPU PC 1의 Lula RRT 전역 계획 + Lula trajectory generation + RMPflow 실행
- 통신: ROS 2 Jazzy, Fast DDS, `/clock` 기반 simulation time

RRT는 정적 planning scene에서 transit/staging/pre-grasp/retract의 전역적으로 충돌 없는 c-space 경로를 찾는 용도다. RRT waypoint를 단순 선형 보간해 실행하지 않고 시간 매개화된 궤적으로 변환한 뒤 RMPflow로 추종한다. palm 접촉 이후의 twist·pull은 접촉 의도가 있는 결정론적 task-space 동작으로 유지한다. RMPflow는 실행 중 world view를 매 simulation step 갱신하는 반응형 실행 계층이며, PhysX contact monitor가 별도의 최종 안전 정지 계층이다.

## PC 역할

- GPU PC 1: Isaac Sim, 물리, 센서·TF·`/clock`, planning scene 발행, Lula RRT 및
  trajectory planning, RMPflow 기반 로봇 실행, 실제 PhysX collider 기반 최종 안전
  감시, motion planning 시각화 토픽 발행
- GPU PC 2: 품질 영상 추론 및 사과 단위 결과 통합
- 개인 PC 1: GPU PC 1의 RGB-D/CameraInfo/TF를 받아 사과 검출과 3D world 좌표를
  계산하고 target을 발행, GPU PC 1의 계획 결과를 RViz로 원격 표시
- 개인 PC 2: 모니터링 및 2차 개발의 푸셔 선택

수확 계획과 실행의 단일 권위(authority)는 GPU PC 1이다. 개인 PC 1은 로봇을
구동하거나 최종 경로를 승인하지 않는다. 역할 변경이 필요한 경우 공유
인터페이스와 PC 소유권을 함께 갱신한다.

쉽게 말하면 개인 PC 1은 영상을 보는 **눈**, GPU PC 1은 판단하고 로봇을 움직이는
**두뇌와 팔**, 개인 PC 1의 RViz는 계획을 보여 주는 **화면**이다.

수확 충돌 회피는 GPU PC 1에서 일관되게 수행한다. GPU PC 1은 자체 planning scene
snapshot과 현재 관절 상태로 RRT 전역 경로를 생성하고, trajectory 변환 및
RMPflow 실행 전에 같은 scene version으로 재검증한다. GPU PC 1은 실행 중 실제
로봇-나무 PhysX 접촉을 감지하면 현재 Action을 중단한다. 개인 PC 1은 필요하면
planning scene과 계획 시각화 토픽을 구독하지만 계획 결과의 권위자가 아니다.

## 기능 경계

- 개인 PC 1의 수확용 인식은 RGB-D 영상에서 사과 중심과 검출 메타데이터를
  계산해 GPU PC 1의 수확 기능에 전달한다.
- GPU PC 1의 수확 기능은 target의 세대·시간·frame을 검증하고 계획·실행한다.
- 수확 기능은 품질을 판정하지 않는다.
- 품질 분류는 컨베이어 상단 카메라에서 독립적으로 수행한다.
- MVP에서는 가상·실제 푸셔를 구현하지 않는다. 2차 개발에서 컨베이어 4와 실제 푸셔 3개를 추가한다.

## 시각화 경계

- GPU PC 1은 현재 로봇 TF, 목표, pre-grasp, RRT 경로, 시간 매개화 궤적,
  planning proxy 및 실행 상태를 RViz용 토픽으로 발행한다.
- 개인 PC 1은 RViz GUI와 설정을 소유하고 원격 토픽을 표시한다.
- RViz 연결 또는 시각화 노드 장애는 모션 실행의 안전·성공 판정에 영향을 주지
  않는다.

## 성공 상태

수확, 컨베이어 배치, 품질 판정 및 컨베이어 3에서의 결과 연결 확인이 모두 완료되어야 한 번의 실행을 성공으로 본다.
