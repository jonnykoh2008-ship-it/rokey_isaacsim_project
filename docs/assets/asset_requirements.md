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
- 3차 USD 배치에서는 다음 두 Prim을 각각 독립 로봇으로 사용한다.

  | robot ID | USD Prim | 초기 관절 자세 (deg) |
  |---|---|---|
  | `robot_01` | `/World/Xform_01/m0617_01` | `[0, 0, -90, 0, 90, 0]` |
  | `robot_02` | `/World/Xform_02/m0617_02` | `[0, 0, 90, 0, -90, 0]` |

- 각 로봇은 `m0617_rail/root_joint`를 Articulation root로 사용한다. M0617 본체는
  `/World/Xform_01/m0617_01/FixedJoint` 또는
  `/World/Xform_02/m0617_02/FixedJoint`로 rail mount에 연결한다. `rail_joint`는
  저장된 초기 위치를 유지한다.
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

컨베이어 2의 품질검사 카메라는 3대다. 손상과 착색은 한쪽 면에만 나타날 수 있어
한 방향 촬영으로는 표면을 덮지 못하므로, 위·왼쪽·오른쪽 고정 뷰로 사과 표면을
동시에 관측한다.

| prim | 위치 | 토픽 namespace | optical frame |
|---|---|---|---|
| `conv_rsd455` | 위 | `/conveyor_camera` | `quality_camera_top_optical_frame` |
| `conv_rsd455_01` | 왼쪽 | `/conveyor_camera_01` | `quality_camera_left_optical_frame` |
| `conv_rsd455_02` | 오른쪽 | `/conveyor_camera_02` | `quality_camera_right_optical_frame` |

세 카메라는 동일한 render product 주기로 발행하며 한 검사의 세 뷰는 timestamp
차이가 20ms 이내여야 한다. 정확한 장착 위치와 각도는 실제 촬영 결과로 확정하며
현재 `TBD`다.

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

3차 USD의 수확용 base D455 Prim은 `robot_01 → /World/base_rsd455_01`,
`robot_02 → /World/base_rsd455_02`로 구분한다. 두 카메라의 최종 ROS topic 및
namespace는 `TBD`다.

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
- break torque: 2Nm
- 작업영역 밖으로 이탈하면 삭제하지 않고 physics, collision 및 visibility를 비활성화한다.
- reset 시 다시 활성화할 수 있도록 object pool 방식 사용을 우선한다.

사과 FixedJoint는 전역 `/World/FixedJoint`가 아니라 각
`/World/Xform/apple_branch_xx` 또는 `/World/Xform_03/apple_branch_xx` 내부에
두며, `branchbody`를 body0, `applebody`를 body1로 연결한다.

## 나무

- 3차 USD에서는 `/World/Xform/tree`와 `/World/Xform_03/tree`를 각각 담당
  로봇의 수확 대상 tree로 사용한다.
- 단일 구조 mesh는 연결 성분을 장축 방향 `40mm` 구간으로 나누고 각 구간의
  로컬 PCA 반경으로 분류한다. 로컬 반경 `20mm` 이상인 굵은 구간에만 짧은 rigid
  capsule collider를 활성화하고 로봇 전체 링크의 planning obstacle로도 사용한다.
- 같은 가지 안에서도 로컬 PCA 반경 `20mm` 미만인 가는 구간은 물리 collision과
  RRT/RMPflow planning proxy에서 모두 제외한다. `40mm` 구간과 `20mm` 반경 기준은
  새 `summerTree` 자산의 굵기 분포를 반영한 시뮬레이션 임시값이다.
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

planning 대상 로컬 굵은 구간은 `20mm` voxel sphere로 단순화하고, 같은 snapshot을
Lula RRT와 RMPflow에 적용한다. 잎은 최신 수확 동작 규약에 따라 PhysX와
Lula/RMPflow 양쪽에서 제외한다.
- 자산 라이선스 정보는 현재 없음. 외부 배포 전 출처와 사용 권한을 확인해야 한다.

## 컨베이어

- MVP는 총 3모듈, 각 0.5m로 구성해 전체 길이 1.5m로 한다.
- 2차 개발에서는 푸셔 전용 컨베이어 4를 추가해 총 4모듈, 전체 길이 2.0m로 확장한다.
- 푸셔 3개는 모두 컨베이어 4에 배치한다.
- collider와 surface velocity를 이용해 사과를 이송한다.
- 롤러는 우선 시각적으로 회전시키며 필요할 때만 revolute joint를 적용한다.
