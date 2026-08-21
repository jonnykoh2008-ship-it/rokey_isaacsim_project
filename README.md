# Isaac Sim 기반 사과 수확·품질 분류 시스템

디지털 트윈 환경에서 Doosan M0617 협동로봇과 Robotiq AGS-001-MTCP 3-finger soft gripper를 이용해 사과를 수확하고, MVP의 3모듈 컨베이어에서 품질을 판정하는 프로젝트다.

## 개발 목표

1. 단일 사과의 접근·파지·Twist & Pull 수확
2. 컨베이어 투입 및 검사 구간 이송
3. 상단 카메라 영상 기반 상·중·하 품질 판정
4. 2차 개발에서 컨베이어 4와 푸셔 3개를 추가해 물리 분류
5. 3차 개발에서 레일, 다중 나무 및 전체 파이프라인 통합

## 기준 환경

- Isaac Sim 5.1.0
- Ubuntu 24.04
- ROS 2 Jazzy / Fast DDS
- Isaac Sim Python 3.11 / ROS 2 Python 3.12
- GPU 노트북 2대, 개인 노트북 2대
- 2.5Gbps 5포트 스위치 중 4포트 사용

## 문서

### 공통 아키텍처

- [시스템 개요](docs/architecture/system_overview.md)
- [ROS 2 인터페이스](docs/architecture/ros2_interfaces.md)
- [TF 및 시간](docs/architecture/tf_frames.md)
- [하드웨어 및 네트워크](docs/architecture/hardware_network.md)

### 기능 명세

- [수확용 인식](docs/features/harvest_perception.md)
- [수확 및 파지](docs/features/harvesting.md)
- [컨베이어](docs/features/conveyor.md)
- [품질 분류](docs/features/quality_grading.md)
- [자산 요구사항](docs/assets/asset_requirements.md)

### 개발 단계

- [1차 MVP](docs/phases/phase_1_mvp.md)
- [2차 AI·도메인 무작위화](docs/phases/phase_2_ai_randomization.md)
- [2차 푸셔](docs/phases/phase_2_pusher.md)
- [3차 시스템 통합](docs/phases/phase_3_system_integration.md)

## 변경 규칙

파일 및 코드 변경은 반드시 사용자 승인 후 진행한다. 상세 규칙은 루트의 `AGENTS.md`를 따른다.
