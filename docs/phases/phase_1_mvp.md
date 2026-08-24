# 1차 개발: MVP

## 목표

GPU PC 1이 발행한 RGB-D 영상을 개인 PC 1이 수신해 단일 사과의 3D world
target을 계산하고, GPU PC 1이 Lula RRT 기반 경로 계획과 로봇 실행으로
수확·컨베이어 배치·품질 등급 산출·결과 연결까지 확인한다.

## 환경

- 사과나무 1그루
- rigid body + collider 사과 1개
- Doosan M0617 1대
- Robotiq AGS-001-MTCP gripper 1개
- 컨베이어 3모듈
- 굵은 가지 rigid collision 활성화
- 얇은 가지와 잎 collision 비활성화, RGB-D occlusion 유지

## 수확

- GPU PC 1에서 RGB, depth, `CameraInfo`, TF 및 `/clock` 발행
- 개인 PC 1에서 RGB-D 검출, depth projection, TF world 변환 및 target 발행
- GPU PC 1에서 target timestamp, frame, `reset_id`, confidence를 검증
- LulaKinematicsSolver로 IK 수행
- Lula RRT로 정적 planning scene의 전역 c-space 경로 생성
- Lula trajectory generation으로 시간 매개화한 뒤 RMPflow로 실행
- RRT는 transit/staging/pre-grasp/retract에 적용하고, palm 접촉 이후 twist·pull은
  결정론적 task-space 동작으로 수행
- world `+Z` 기본 접근만 사용
- 굵은 가지 충돌 회피
- GPU PC 1이 몸통/가지 planning proxy snapshot과 명시적 simulation 상태를
  발행하고, 같은 PC에서 RRT 계획·trajectory 검증·RMPflow 실행을 수행한다.
- GPU PC 1은 실제 로봇-나무 PhysX 접촉 시 Action을 중단한다.
- GPU PC 1이 계획 경로와 상태 visualization을 발행하고 개인 PC 1 RViz에서
  원격 표시한다.
- 급격한 joint 변화 및 singularity 방지
- 45°/1초 손목 회전
- 50mm/s, 최대 100mm 직선 당김
- 15N/1Nm breakable stem joint
- 컨베이어 1에 저상 배치

## 품질 검사

- 컨베이어 2에서 RGB 프레임 수집
- GPU PC 2 품질 추론 인터페이스
- 상·중·하 결과 산출
- 컨베이어 3에서 `apple_id`와 품질 결과 연결 확인
- 가상 푸셔, 실제 푸셔와 상자 구현 제외

## 완료 기준

- Play 후 동일한 초기 조건으로 reset을 포함해 2회 실행한다.
- 2회 중 1회 이상 다음 전체 과정이 성공해야 한다.
  1. 접근
  2. 파지
  3. Twist & Pull 및 stem 분리
  4. 컨베이어 배치
  5. 품질 결과 산출
  6. 컨베이어 3에서 `apple_id`와 품질 결과 연결 확인
- 치명적인 penetration 또는 articulation 불안정이 없어야 한다.
- 개인 PC 1의 영상 target과 GPU PC 1의 계획 scene 세대가 불일치한 경우 stale
  target을 실행하지 않아야 한다.
- RViz 연결이 끊겨도 GPU PC 1의 안전 정지·실행 판정이 시각화 상태와 독립적으로
  동작해야 한다.
