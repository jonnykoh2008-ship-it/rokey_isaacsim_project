# 하드웨어 및 네트워크

## 장비

- RTX 5080 GPU 노트북 2대
- 개인 Linux 노트북 2대
- 2.5Gbps 5포트 Ethernet 스위치 중 4포트 사용
- 유선망은 인터넷과 분리하고 공용 Wi-Fi로 인터넷을 사용한다.

## 고정 IP

| 장비 | IP | 기본 역할 |
|---|---|---|
| GPU PC 1 | `10.10.0.1` | Isaac Sim, 센서·TF 발행, Lula RRT/trajectory/RMPflow, 로봇 실행·안전 감시, motion visualization 발행 |
| GPU PC 2 | `10.10.0.2` | 컨베이어 영상 수신·프레임 수집/선택·품질 추론 |
| 개인 PC 1 | `10.10.0.3` | RGB-D 수신·사과 3D 좌표 계산·target 발행, RViz 원격 표시 |
| 개인 PC 2 | `10.10.0.4` | 분류 제어·모니터링 |

## ROS 2

- 배포판: ROS 2 Jazzy
- RMW: Fast DDS
- 통합 환경 `ROS_DOMAIN_ID=101`
- 개별 테스트 `ROS_DOMAIN_ID=102~107`
- 다중 PC 통신에 UDP transport를 사용하도록 Fast DDS 설정을 통일한다.
- 수확 v2.0의 RGB와 depth 입력은 raw `sensor_msgs/msg/Image`로 확정한다.
- GPU PC 1은 RGB/depth/CameraInfo를 개인 PC 1으로 전달하고, 개인 PC 1은 사과
  3D target을 GPU PC 1으로 반환한다. 해상도와 FPS는 별도 시험값으로 관리한다.
- 수확 입력과 컨베이어 품질 입력은 GPU PC 1에서 raw RGB/depth/CameraInfo로
  발행한다. GPU PC 2가 raw 스트림을 구독해 후보 프레임 수집과 대표 프레임 선택을
  수행하며, 대표 이미지의 전용 cross-PC 압축 토픽과 이름/QoS는 `TBD`다.
- motion planning visualization은 GPU PC 1에서 발행하고 개인 PC 1의 RViz가
  원격 표시한다. RViz 데이터는 안전·실행 경로가 아니므로 유실을 허용한다.
- planning scene은 GPU PC 1에서 RRT/RMPflow에 직접 사용하고, 개인 PC 1에는
  시각화·디버그용 snapshot으로 전달한다.
- 정적인 나무 planning scene은 전체 snapshot 한 개로 전달한다. QoS는
  `Reliable + Transient Local + Keep Last 1`을 사용하고, 개인 PC 1은 누락 또는
  버전 불일치 시 `/planning_scene/get_snapshot`으로 최신 snapshot을 요청한다.

## 운영 규칙

- 모든 PC의 ROS_DOMAIN_ID, RMW 설정 및 메시지 버전을 실행 전에 확인한다.
- target, `PlanningScene`, `SimulationState`, `MotionStatus` 또는 visualization
  인터페이스가 변경되면 GPU PC 1의 Isaac Python 3.11 인터페이스와 개인 PC 1의
  ROS Python 3.12 인터페이스를 함께 재빌드한다. 한쪽만 이전 인터페이스를
  사용하는 상태에서는 통합 실행하지 않는다.
- Wi-Fi와 Ethernet의 라우팅 우선순위가 ROS 2 discovery를 방해하지 않도록 인터페이스를 고정한다.
- 네트워크 대역폭과 RGB-D 전송 지연, TF-target timestamp 오차, target-to-plan
  지연, RViz 표시 지연은 통합 시험에서 별도로 측정한다.
- 영상 또는 target 연결이 끊기면 GPU PC 1은 stale target을 실행하지 않고
  정지·실패 상태를 발행한다. 네트워크 노드 장애 감지용 wall-time timeout은
  simulation-time motion timeout과 분리하며 값은 `TBD`다.
