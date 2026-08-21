# 1차 개발: MVP

## 목표

단일 사과의 ground-truth pose를 이용해 수확하고 컨베이어에 배치한 뒤 품질 등급과 가상 푸셔 위치까지 확인한다.

## 환경

- 사과나무 1그루
- rigid body + collider 사과 1개
- Doosan M0617 1대
- AGS-001-MTCP gripper 1개
- 컨베이어 3모듈
- 굵은 가지 rigid collision 활성화
- 얇은 가지와 잎 collision 비활성화, RGB-D occlusion 유지

## 수확

- 사과 pose를 직접 전달
- LulaKinematicsSolver 사용
- world `+Z` 기본 접근만 사용
- 굵은 가지 충돌 회피
- 급격한 joint 변화 및 singularity 방지
- 45°/1초 손목 회전
- 50mm/s, 최대 100mm 직선 당김
- 15N/1Nm breakable stem joint
- 컨베이어 1에 저상 배치

## 검사 및 분류

- 컨베이어 2에서 RGB 프레임 수집
- GPU PC 2 품질 추론 인터페이스
- 상·중·하 결과 산출
- 컨베이어 3의 가상 푸셔 위치와 결과 연결
- 실제 푸셔와 상자 구현 제외

## 완료 기준

- Play 후 동일한 초기 조건으로 reset을 포함해 2회 실행한다.
- 2회 중 1회 이상 다음 전체 과정이 성공해야 한다.
  1. 접근
  2. 파지
  3. Twist & Pull 및 stem 분리
  4. 컨베이어 배치
  5. 품질 결과 산출
  6. 가상 푸셔 위치 매칭
- 치명적인 penetration 또는 articulation 불안정이 없어야 한다.

