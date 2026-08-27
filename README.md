# Isaac Sim 기반 사과 수확·품질 분류 시스템

디지털 트윈 환경에서 Doosan M0617 협동로봇 두 대와 Robotiq AGS-001-MTCP 3-finger soft gripper를 이용해 사과를 수확하고, MVP의 3모듈 컨베이어에서 품질을 판정하는 프로젝트다. v2.0에서는 개인 PC 1이 영상에서 사과의 3D 좌표를 계산하고, GPU PC 1이 해당 좌표를 받아 Lula 기반 경로 계획과 로봇 실행을 전담한다. 3차 통합에서는 저장된 USD의 두 M0617과 두 수확 영역을 로봇별 프로파일로 선택한다.

## 개발 목표

1. 단일 사과의 접근·파지·Twist & Pull 수확
2. 컨베이어 투입 및 검사 구간 이송
3. 상단 카메라 영상 기반 상·중·하 품질 판정
4. 2차 개발에서 컨베이어 4와 푸셔 3개를 추가해 물리 분류
5. 3차 개발에서 두 M0617, 다중 나무 및 전체 파이프라인 통합

## 기준 환경

- Isaac Sim 5.1.0
- Ubuntu 24.04
- ROS 2 Jazzy / Fast DDS
- Isaac Sim Python 3.11 / ROS 2 Python 3.12
- GPU 노트북 2대, 개인 노트북 2대
- 2.5Gbps 5포트 스위치 중 4포트 사용

## 저장된 USD 멀티로봇 매핑

현재 실행 자산의 기준 경로와 초기 관절 자세는 다음과 같다.

| 로봇 프로파일 | 로봇 Prim | 초기 관절 자세 (deg) | 수확 자산 영역 | 인식 카메라 Prim |
|---|---|---|---|---|
| `robot_01` | `/World/Xform_01/m0617_01` | `[0, 0, -90, 0, 90, 0]` | `/World/Xform`의 `tree`·`apple_branch[_1/_2]` | `/World/base_rsd455_01` |
| `robot_02` | `/World/Xform_02/m0617_02` | `[0, 0, 90, 0, -90, 0]` | `/World/Xform_03`의 `tree`·`apple_branch[_1/_2]` | `/World/base_rsd455_02` |

사과의 `PhysicsFixedJoint`는 각 `apple_branch_xx` 내부에 있으며,
`branchbody → applebody` 관계를 사용한다. GPU PC 1 코드는 실행 시 이 관계를
검증하고 파손 한계를 Session Layer에 적용한다. 각 로봇의 Articulation root는
`/World/Xform_01/m0617_rail/root_joint` 또는
`/World/Xform_02/m0617_rail/root_joint`이며, M0617 본체는 각각의
`m0617_01/FixedJoint`·`m0617_02/FixedJoint`로 rail mount에 연결된다. ROS topic/action namespace는
3차 통합 계약에서 `TBD`로 유지한다.

## v2.0 실행 구조

```text
GPU PC 1: Isaac Sim RGB-D/TF/장애물 발행
  → 개인 PC 1: 영상 수신·사과 3D 좌표 계산
  → GPU PC 1: Lula RRT 전역 계획·궤적 생성·RMPflow 실행·PhysX 안전 감시
  → 개인 PC 1: RViz 원격 표시
```

- 영상 기반 수확 인식의 실행 주체는 개인 PC 1이다.
- 경로 계획, 계획 검증, Action 실행 및 최종 충돌 감시는 GPU PC 1이다.
- motion planning 시각화 데이터는 GPU PC 1이 발행하고 RViz GUI는 개인 PC 1에서 실행한다.
- GPU PC 2는 컨베이어 카메라 영상을 받아 ROI/tracker, 후보 프레임 수집·대표 프레임
  선택, 품질 추론 및 사과 단위 결과 통합을 수행하고, 개인 PC 2는 결과 표시·푸셔
  선택을 담당한다.

쉽게 말하면 개인 PC 1은 카메라로 보는 **눈**, GPU PC 1은 경로를 결정하고 로봇을
움직이는 **두뇌와 팔**, 개인 PC 1의 RViz는 결과를 보는 **화면**이다.

## 3차 멀티로봇 실행 선택

GPU PC 1의 standalone 수확·통합 실행은 `--robot-id robot_01` 또는
`--robot-id robot_02`로 USD 로봇 프로파일을 선택한다. 두 프로파일은 각각의
`m0617_rail` Articulation root, M0617 본체, 나무/사과 영역, D455 Prim 및
초기 관절 자세를 사용한다.
두 로봇을 동시에 운용할 ROS topic/action namespace와 target의 최종 robot ID
필드는 아직 `TBD`다.

## 통합 실행 코드

각 PC에서 저장소 루트의 `system_launcher.py`를 실행한다. launcher는 원격 PC에
접속하지 않고 현재 PC 역할에 해당하는 프로세스만 시작한다. 네 PC는 같은
`ROS_DOMAIN_ID`와 Fast DDS 네트워크 설정을 사용해야 한다.

GPU PC 1에서 Isaac Sim과 두 로봇 Coordinator를 준비한다.

```bash
python3 system_launcher.py --role gpu_pc1 --robot-id robot_01
```

개인 PC 1에서는 두 카메라 detector를 실행한다.

```bash
python3 system_launcher.py --role personal_pc1
```

개인 PC 2에서는 품질 모니터를 실행한다.

```bash
python3 system_launcher.py --role personal_pc2
```

실행 전에 명령만 확인하려면 각 명령에 `--dry-run`을 붙인다. 현재
`vision_apple_pick.py`의 Isaac Sim runtime은 단일 `--robot-id` profile만 직접
실행하므로 GPU PC 1 launcher도 그 제한을 따른다. Coordinator와 detector는
`all` 모드로 두 로봇 endpoint를 준비하지만, 두 로봇을 하나의 Isaac Sim World에서
동시에 움직이는 최종 runtime은 별도 구현 대상이다.

## PC별 개발 범위

| PC | 담당 기능 | 유지·개발 대상 |
|---|---|---|
| GPU PC 1 | Isaac Sim, 물리, 센서·TF·planning scene, Lula RRT/trajectory/RMPflow, 로봇 실행, 충돌 감시, 계획 시각화 | `apple_pick.py`, `vision_apple_pick.py`, `base_camera_publish.py`, planner/executor |
| GPU PC 2 | 컨베이어 카메라 수신, ROI/tracker, 후보 프레임 수집·대표 프레임 선택, 품질 영상 추론 및 사과 단위 품질 결과 통합 | 품질 캡처·추론·결과 통합 소스 (`TBD`) |
| 개인 PC 1 | RGB-D 기반 사과 검출·3D 좌표 계산·target 발행, RViz 원격 표시 | PC1 perception 노드 및 RViz 설정 (`TBD`) |
| 개인 PC 2 | 모니터링, 품질 결과 표시, 재검 요청, 2차 푸셔 선택 | 모니터링·푸셔 선택 소스 (`TBD`) |

v2.0 기준으로 수확 계획·상태 머신·RobotMotion 실행을 담당하는
`harvest_coordinator.py`와 `harvest_route_planner.py`의 소유권은 GPU PC 1로
이전한다. 개인 PC 1은 새 perception 노드와 RViz 설정을 소유한다. 실제 코드
이관과 인터페이스 반영은 별도 구현 단계에서 수행하며, 공유 인터페이스와 문서는
네 PC 공동 소유다.

## 모션 계획 원칙

GPU PC 1은 정적 planning scene에서 Lula RRT로 시작 관절 상태부터 transit/staging/pre-grasp까지 전역 경로 후보를 만든다. RRT 출력 waypoint를 그대로 로봇에 보내지 않고 Lula trajectory generation으로 시간 매개화한 뒤, GPU PC 1의 RMPflow와 PhysX contact monitor로 실행 중 재검증한다. palm 접촉 이후의 twist·pull은 접촉 의도가 있는 결정론적 task-space 동작으로 유지한다. 동적 장애물이나 목표 변화가 생기면 현재 Action을 중단하고 최신 `reset_id/scene_version`으로 재계획한다.

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
