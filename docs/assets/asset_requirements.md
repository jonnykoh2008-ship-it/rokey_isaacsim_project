# 시뮬레이션 자산 요구사항

## 공통 단위

- 길이: meter
- 질량: kilogram
- 힘: newton
- 토크: newton-meter
- 모든 asset의 축, scale, articulation 및 collision을 Isaac Sim 5.1.0에서 검증한다.

## M0617

- 6DOF Doosan M0617
- fixed-base MVP 구성
- LulaKinematicsSolver에서 사용할 robot description과 URDF/USD 관절 이름을 일치시킨다.
- GPU PC 1의 Lula RRT·trajectory·RMPflow가 동일한 URDF, robot description,
  collision sphere 및 joint limit를 사용해야 한다.
- Lula RRT용 planner configuration은 RMPflow configuration과 분리해 관리한다.
  seed, step size, iteration/sampling limit, distance metric, task-space limits 및
  `link_6` end-effector frame 일치 여부를 GPU PC 1에서 검증한다. 실제 수치와
  지원 robot-description 경로는 `TBD`다.
- 장착 어댑터 asset은 만들지 않는다.

## Robotiq AGS-001-MTCP 그리퍼

- 방식: 3-finger soft gripper
- 시뮬레이션: rigid finger + compliant contact 근사
- 최대 개구폭: 155mm
- 파지 가능 직경: 20~155mm
- 파지력: 30~75N
- 질량: 2.1kg
- 포위 파지 가반하중: 10kg
- end-effector frame: `gripper_frame`
- 상세 joint 이름, joint range, mimic/동기 구동 방식 및 fingertip contact 위치는 TBD다.

## 카메라

베이스, arm, 컨베이어 카메라에 동일한 Intel RealSense D455 사양을 사용한다.

- 동작 범위: 0.4~6m, 권장 최적 범위 0.6m 이상
- Depth 최대 해상도: 1280×720
- Depth 최대 FPS: 90
- Depth FOV: 86°×57° (±3°)
- 4m 거리 depth 오차: 2% 미만
- RGB 최대 해상도: 1280×800
- RGB 최대 FPS: 90
- RGB FOV: 86°×57° (±3°)
- RGB/Depth global shutter
- MVP 초기 실행 프로파일 후보: 1280×720, 30fps
- 실제 해상도, FPS, intrinsics 및 장착 transform은 TBD다.

v2.0에서 GPU PC 1은 raw RGB, raw depth 및 `CameraInfo`를 발행하고 개인 PC 1은
이를 구독해 사과 중심을 계산한다. RGB와 depth의 촬영 timestamp와 카메라 TF가
같은 simulation-time 기준을 사용해야 한다. 해상도, FPS 및 허용 timestamp 오차는
`TBD`다.

## 사과

모든 사과에 다음을 적용한다.

- rigid body
- collider
- 중력
- 지름: 80mm
- 질량: 0.3kg
- 컨베이어, 푸셔 및 다른 사과와 물리 충돌
- 줄기에 연결된 동안 breakable joint 적용
- break force: 15N
- break torque: 1Nm
- 작업영역 밖으로 이탈하면 삭제하지 않고 physics, collision 및 visibility를 비활성화한다.
- reset 시 다시 활성화할 수 있도록 object pool 방식 사용을 우선한다.

## 나무

- 나무 1그루를 수확 대상 3D asset으로 사용한다.
- 굵은 가지는 rigid collider를 활성화하고 로봇 전체 링크의 planning obstacle로
  사용한다.
- 작은 가지는 물리 collision을 비활성화하되 별도의 capsule/sphere/convex
  planning proxy를 유지한다.
- 잎은 visual-only로 유지한다. 물리 collision을 비활성화하고 Lula/RMPflow
  planning obstacle에도 전달하지 않는다.
- visual mesh, PhysX collision mesh, planning collision proxy를 서로 분리한다.
- 복잡한 가지 visual mesh를 planning에 직접 전달하지 않고 capsule, sphere,
  convex 또는 voxel proxy로 단순화한다.
- planning proxy에는 자산 분류(`trunk`, `branch`)와 적용한 안전거리
  값을 기록한다.

GPU PC 1은 reset마다 planning proxy snapshot을 생성하고 Lula RRT와 RMPflow에
동일한 proxy 및 safety margin을 적용한다. 개인 PC 1은 proxy를 재생성하지 않고
필요할 때 RViz 표시용으로만 사용한다.

작은 가지의 물리 collision 비활성화는 경로 계획 장애물 제외를 의미하지
않으며 Lula/RMPflow 회피 대상으로 유지한다. 잎은 최신 수확 동작 규약에 따라
PhysX와 Lula/RMPflow 양쪽에서 제외한다.
- 자산 라이선스 정보는 현재 없음. 외부 배포 전 출처와 사용 권한을 확인해야 한다.

## 컨베이어

- MVP는 총 3모듈, 각 0.5m로 구성해 전체 길이 1.5m로 한다.
- 2차 개발에서는 푸셔 전용 컨베이어 4를 추가해 총 4모듈, 전체 길이 2.0m로 확장한다.
- 푸셔 3개는 모두 컨베이어 4에 배치한다.
- collider와 surface velocity를 이용해 사과를 이송한다.
- 롤러는 우선 시각적으로 회전시키며 필요할 때만 revolute joint를 적용한다.
