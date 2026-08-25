# 3차 개발: 레일 및 시스템 통합

## 목표

레일을 따라 여러 나무를 이동하며 수확하고, 수확·검사·분류를 하나의 연속 파이프라인으로 통합한다.

## 레일

- M0617 베이스를 레일에 결합
- `odom → base_link` 동적 TF 확장
- 여러 나무의 작업 위치 이동
- 레일 위치별 접근 가능 사과 평가

## 다중 객체

- 여러 나무와 사과 ID 관리
- 사과별 수확·검사·분류 lifecycle 관리
- 최소 투입 시간과 중심 간격 적용
- 사과 간 rigid-body 충돌, 정체 및 순서 변경 처리
- base camera에서 동시에 보이는 사과는 world 위치 기반 고정 ID로 연결하고,
  GPU PC 1이 robot base 최근접 순서로 연속 수확한다.
- 접촉 전 첫 실패 target은 다른 사과 처리 후 1회 재시도하며, 접촉 이후 실패는
  다음 사과로 진행하지 않고 안전 정지한다.

## 시스템 통합

- GPU PC 1: Isaac Sim 및 센서, TF, Lula RRT/trajectory/RMPflow, 로봇 실행·안전
  감시, 수확·푸셔 계획 visualization 발행
- GPU PC 2: 품질 AI 추론 및 사과 단위 결과 통합
- 개인 PC 1: RGB-D 수확 인식·world target 발행, GPU PC 1 계획 visualization의
  RViz 원격 표시
- 개인 PC 2: 분류 제어·모니터링
- ROS 2 Jazzy/Fast DDS 기반 다중 PC 통신
- 영상 전송 latency, target 계산·전달 latency, RRT 계획시간, 실행시간,
  visualization latency, throughput 및 메시지 유실 측정

## 복구

- 수확 실패
- ID 유실
- 품질 결과 timeout
- 푸셔 실패
- 사과 작업영역 이탈
- 노드 또는 네트워크 장애

영상 또는 target 네트워크 장애 시 GPU PC 1은 마지막 target을 무기한 재사용하지
않고 stale 정책에 따라 정지한다. RViz 장애는 표시만 중단하며 수확 safety
monitor의 판정과 분리한다.

상세 복구 정책과 연속 운용 완료 기준은 TBD다.
