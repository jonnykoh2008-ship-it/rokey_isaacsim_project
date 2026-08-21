# 하드웨어 및 네트워크

## 장비

- RTX 5080 GPU 노트북 2대
- 개인 Linux 노트북 2대
- 2.5Gbps 5포트 Ethernet 스위치 중 4포트 사용
- 유선망은 인터넷과 분리하고 공용 Wi-Fi로 인터넷을 사용한다.

## 고정 IP

| 장비 | IP | 기본 역할 |
|---|---|---|
| GPU PC 1 | `10.10.0.1` | Isaac Sim 및 센서 발행 |
| GPU PC 2 | `10.10.0.2` | 품질 추론 |
| 개인 PC 3 | `10.10.0.3` | 로봇 계획·개발 |
| 개인 PC 4 | `10.10.0.4` | 분류 제어·모니터링 |

## ROS 2

- 배포판: ROS 2 Jazzy
- RMW: Fast DDS
- 통합 환경 `ROS_DOMAIN_ID=101`
- 개별 테스트 `ROS_DOMAIN_ID=102~107`
- 다중 PC 통신에 UDP transport를 사용하도록 Fast DDS 설정을 통일한다.
- 센서 데이터는 필요한 경우 compressed transport로 전달한다.
- RGB는 JPEG 기반 압축, depth는 `compressedDepth` 또는 PNG 기반 무손실 압축을 우선한다.
- 가능하면 GPU PC 1에서 원본 센서를 처리하고 네트워크에는 pose나 선별 이미지처럼 축소된 결과를 전달한다.

## 운영 규칙

- 모든 PC의 ROS_DOMAIN_ID, RMW 설정 및 메시지 버전을 실행 전에 확인한다.
- Wi-Fi와 Ethernet의 라우팅 우선순위가 ROS 2 discovery를 방해하지 않도록 인터페이스를 고정한다.
- 네트워크 대역폭과 추론 지연은 통합 시험에서 측정한다.

