# 베이스 카메라 기반 나뭇잎 회피 구현 검토

## 1. 문서 목적

이 문서는 베이스 RGB-D 카메라로 나뭇잎을 감지하고, 감지 결과를 로봇 경로 계획에 반영하여 M0617 로봇 팔이 나뭇잎을 피해 이동하도록 구현할 때 필요한 역할, 오류 가능성, 주의사항 및 검증 항목을 정리한다.

구현 책임은 다음과 같이 구분한다.

- **Personal PC 1:** RGB-D 기반 잎 검출, 3D 위치 계산, world 좌표 변환 및 장애물 후보 발행
- **GPU PC 1:** 장애물 후보 검증, planning scene 반영, Lula RRT/RMPflow 회피 계획, 실행 중 정지·재계획 및 최종 안전 판단

Personal PC 1은 로봇을 직접 제어하지 않으며, GPU PC 1은 RGB 영상에서 잎을 직접 검출하지 않는다.

## 2. 기준 환경

- NVIDIA Isaac Sim 5.1.0
- Ubuntu 24.04
- ROS 2 Jazzy / Fast DDS
- `/clock` 기반 Isaac Sim simulation time
- 모든 ROS 2 노드에 `use_sim_time:=true` 적용
- 최종 TF 권위자는 GPU PC 1의 Isaac Sim
- 최종 경로 계획과 로봇 실행 권위자는 GPU PC 1

## 3. 현재 명세와 변경 필요사항

현재 저장소 명세와 구현은 잎을 visual-only 자산으로 취급한다.

- 잎의 PhysX collision은 비활성화되어 있다.
- 잎은 planning scene과 Lula/RMPflow obstacle에서 제외된다.
- `ObstacleProxy`는 `CLASS_TRUNK`와 `CLASS_BRANCH`만 정의한다.
- GPU PC 1의 planning scene 생성 코드는 foliage mesh를 명시적으로 건너뛴다.

요청 기능을 구현하려면 다음 정책 변경이 필요하다.

> 잎은 PhysX collider로 만들지 않지만, Personal PC 1이 RGB-D 영상에서 검출한 잎 후보는 GPU PC 1의 검증을 거쳐 일시적인 planning proxy로 사용할 수 있다.

이 변경은 시각 자산의 물리 충돌을 활성화하는 것이 아니다. 로봇은 실제 잎 mesh가 아니라 검출 결과에서 생성한 보수적인 proxy를 회피한다. 검출하지 못한 잎에 대한 물리 접촉 검증은 불가능하므로, 회피 보장은 수신·검증된 proxy 범위로 한정된다.

## 4. 전체 데이터 흐름

```text
GPU PC 1 base D455
  ├─ RGB
  ├─ Depth
  ├─ CameraInfo
  ├─ TF
  ├─ /clock
  └─ SimulationState
        ↓
Personal PC 1
  RGB-D 동기화
    → 잎 segmentation
    → 유효 Depth 검사
    → camera-frame 3D 복원
    → 촬영 시각의 TF로 world 변환
    → voxel/sphere 장애물 후보 생성
    → reset·timestamp·상태 검증
    → leaf obstacle 후보 발행
        ↓
GPU PC 1
  메시지·세대·시간 검증
    → planning proxy 채택 또는 거부
    → planning scene 갱신
    → Lula RRT 경로 재계획
    → trajectory generation
    → RMPflow 실행
    → 변경·stale·오류 시 정지 또는 재계획
```

## 5. Personal PC 1 구현 사항

### 5.1 입력

| 입력 | 타입 | 용도 |
|---|---|---|
| `/base_camera/color/image_raw` | `sensor_msgs/msg/Image` | 잎 색상 및 영역 검출 |
| `/base_camera/depth/image_raw` | `sensor_msgs/msg/Image` | 검출 픽셀의 거리 계산 |
| `/base_camera/camera_info` | `sensor_msgs/msg/CameraInfo` | 픽셀을 camera-frame 3D 좌표로 역투영 |
| `/tf`, `/tf_static` | `tf2_msgs/msg/TFMessage` | 촬영 시각의 `base_camera → world` 변환 |
| `/simulation/state` | `appleproj_interfaces/msg/SimulationState` | Timeline 상태, `reset_id`, `scene_version` 확인 |
| `/clock` | `rosgraph_msgs/msg/Clock` | timestamp, stale 및 timeout 판정 |

### 5.2 처리 단계

1. RGB, Depth 및 CameraInfo의 해상도와 frame을 확인한다.
2. RGB와 Depth를 timestamp 기준으로 동기화한다.
3. 초기 MVP에서는 OpenCV HSV 방식으로 녹색 잎 mask를 생성한다.
4. morphology open/close와 최소 영역 필터로 작은 노이즈를 제거한다.
5. 사과 mask 및 명백한 비관심 영역을 잎 mask에서 제외한다.
6. mask 내부에서 유효한 Depth 픽셀만 선택한다.
7. `CameraInfo`의 `fx`, `fy`, `cx`, `cy`로 camera-frame 3D 포인트를 계산한다.
8. RGB 촬영 timestamp에 해당하는 TF로 포인트를 `world` frame으로 변환한다.
9. world 포인트를 voxel downsampling하고 인접 후보를 군집화한다.
10. 각 군집을 하나 이상의 sphere proxy로 근사한다.
11. frame 상태, `reset_id`, timestamp 및 검출 품질을 검증한다.
12. 정상 결과, 정상 무검출 또는 오류 상태를 구분해 발행한다.

HSV 범위, 최소 영역, Depth 범위, 동기화 허용 오차, voxel 크기, proxy 반지름, 안전거리, 검출 지속 프레임 수 및 stale 시간은 모두 `TBD`다. 승인 전에는 영구값으로 확정하지 않는다. 구현 시 ROS parameter로 노출하고, 임시 시험값을 사용할 경우 별도 승인을 받는다.

### 5.3 장애물 후보 규약

각 leaf proxy에는 최소한 다음 정보가 필요하다.

- 안정적인 `obstacle_id`
- `CLASS_LEAF`
- `SHAPE_SPHERE`
- world 기준 중심 pose
- sphere 반지름
- 형상 크기와 분리된 `safety_margin`
- RGB-D 촬영 timestamp
- `reset_id`
- Personal PC 1이 관측한 `scene_version`
- 관측 sequence 또는 동등한 세대 식별자

`obstacle_id`는 단순 프레임 순번이 아니라 world voxel index 또는 tracker ID를 기반으로 생성해 동일한 잎이 매 프레임 다른 장애물로 보이지 않게 한다.

### 5.4 상태 구분

빈 obstacle 배열은 원인에 따라 의미가 달라야 한다.

| 상태 | 의미 | GPU PC 1 처리 기대값 |
|---|---|---|
| `OK` | 정상 검출이며 leaf proxy 존재 | 검증 후 planning 후보로 사용 |
| `NO_LEAF` | 입력과 처리는 정상이지만 잎 없음 | 이전 leaf proxy 제거 가능 |
| `DEPTH_INVALID` | 잎 후보는 있으나 3D 위치 계산 불가 | 무장애물로 해석 금지 |
| `TF_UNAVAILABLE` | 촬영 시각의 world 변환 실패 | 무장애물로 해석 금지 |
| `STALE_FRAME` | 허용 수명을 넘긴 영상 | 후보 폐기 |
| `RESET_MISMATCH` | 다른 simulation 세대 결과 | 후보 폐기 및 캐시 초기화 |
| `INPUT_NOT_SYNCHRONIZED` | RGB/Depth 시간 불일치 | 해당 프레임 폐기 |
| `INTERNAL_ERROR` | 예상하지 못한 처리 오류 | 장애물 없음으로 간주 금지 |

정상적인 `NO_LEAF` 결과는 GPU PC 1이 이전 leaf proxy를 제거할 수 있도록 빈 배열과 함께 발행해야 한다. 센서·TF·처리 오류에 의한 빈 배열은 `NO_LEAF`와 구분한다.

### 5.5 reset 처리

Timeline Stop 또는 `reset_id` 변경 시 Personal PC 1은 다음 상태를 모두 폐기한다.

- 마지막 RGB와 Depth
- CameraInfo와 결합된 처리 대기 항목
- leaf mask와 point cloud 캐시
- voxel 및 군집 결과
- tracker와 obstacle ID 매핑
- 이전 세대의 발행 대기 메시지

새로운 `SimulationState`가 `READY` 또는 `PLAYING`이 되기 전에는 정상 leaf obstacle 후보를 발행하지 않는다.

## 6. Personal PC 1 예상 오류 및 주의사항

### 6.1 RGB/Depth 프레임 혼합

최신 RGB 한 장과 최신 Depth 한 장을 단순 결합하면 서로 다른 시각의 영상이 섞일 수 있다. 잎 윤곽과 Depth가 어긋나 잘못된 3D 장애물이 생성된다.

대응:

- timestamp 기반 bounded queue 또는 ROS 2 동기화 기능을 사용한다.
- 허용 오차를 넘은 쌍은 처리하지 않는다.
- 같은 RGB timestamp를 중복 처리하지 않는다.

### 6.2 CameraInfo 불일치

이전 해상도의 CameraInfo를 현재 영상에 사용하면 역투영 결과가 틀어진다.

대응:

- RGB, Depth, CameraInfo의 width, height 및 frame ID를 검증한다.
- intrinsics의 `fx`, `fy`가 0 이하이면 처리하지 않는다.

### 6.3 TF 방향 또는 timestamp 오류

최신 TF를 임의로 사용하면 카메라가 움직이는 구성에서 obstacle이 잘못된 world 위치에 생성된다.

대응:

- 반드시 RGB 촬영 timestamp의 `base_camera → world` TF를 조회한다.
- `/tf_static`의 timestamp 0은 모든 simulation time에 유효한 것으로 처리한다.
- TF를 찾지 못하면 후보를 발행하지 않고 오류 상태를 보낸다.

### 6.4 HSV 오검출

녹색 배경, 나무 재질 또는 조명 변화가 잎으로 오인될 수 있다. 반대로 어두운 잎이나 가려진 잎은 누락될 수 있다.

대응:

- HSV 범위를 ROS parameter로 노출한다.
- 최소 면적, Depth 범위, world 작업영역 및 시간 지속성 검사를 조합한다.
- debug mask와 3D proxy를 동시에 표시한다.
- 필요하면 후속 단계에서 semantic segmentation 또는 학습 모델로 검출부만 교체한다.

### 6.5 처리 성능 저하

1280×720 영상을 모든 픽셀에 대해 Python 반복문으로 역투영하면 처리 주기가 크게 떨어질 수 있다.

대응:

- NumPy 벡터 연산을 사용한다.
- mask 단계에서 pixel stride 또는 contour 내부 표본화를 적용한다.
- world 변환 후 voxel downsampling한다.
- 입력 FPS와 별도로 leaf obstacle 발행 주기를 제한한다.
- 최대 proxy 수를 둔다. 최종 값은 `TBD`다.

### 6.6 obstacle ID 진동

매 프레임 ID가 변경되면 GPU PC 1이 동일한 장면을 계속 새로운 obstacle scene으로 판단해 반복 재계획할 수 있다.

대응:

- world voxel index 기반의 결정론적 ID를 사용한다.
- 추가와 제거에 서로 다른 지속 조건을 적용하는 hysteresis를 둔다.
- 작은 위치 변화는 동일 proxy로 병합한다. 허용 변화량은 `TBD`다.

### 6.7 stale obstacle 잔류

잎이 사라졌는데 빈 정상 결과를 보내지 않으면 GPU PC 1에 이전 proxy가 남아 경로를 계속 막을 수 있다.

대응:

- `NO_LEAF` heartbeat를 발행한다.
- 오류 상태와 정상 무검출을 분리한다.
- reset 시 즉시 캐시를 비운다.

## 7. GPU PC 1 구현 사항

GPU PC 1은 Personal PC 1의 결과를 그대로 신뢰하지 않고 다음 조건을 검증한다.

- 메시지 `frame_id`가 `world`인지 확인
- 현재 `reset_id`와 일치하는지 확인
- timestamp가 stale하지 않은지 확인
- `scene_version` 또는 관측 세대가 수용 가능한지 확인
- proxy pose, quaternion, dimensions 및 safety margin이 유효한지 확인
- proxy 개수와 작업영역이 제한 안에 있는지 확인
- 로봇 시작 자세를 잘못 가두는 proxy인지 확인
- 정상 `NO_LEAF`와 인식 오류를 구분

검증을 통과한 proxy만 GPU PC 1의 planning scene에 채택한다. Personal PC 1은 최종 obstacle authority가 아니다.

## 8. GPU PC 1 예상 오류 및 주의사항

### 8.1 지원하지 않는 obstacle class

현재 `ObstacleProxy`와 GPU PC 1 코드는 `trunk`, `branch`만 지원한다. `leaf`를 그대로 전달하면 메시지 상수 부재, class 매핑 `KeyError` 또는 미분류 obstacle 처리가 발생한다.

대응:

- 공유 인터페이스에 `CLASS_LEAF`를 추가한다.
- scene 직렬화·역직렬화 매핑에 `leaf`를 추가한다.
- route planner에 leaf 전용 분류와 개수 제한을 추가한다.

### 8.2 foliage 강제 제외

현재 GPU PC 1의 planning geometry 생성은 foliage mesh를 건너뛰고 `leaf 0`으로 scene을 만든다. Personal PC 1이 후보를 발행해도 별도의 구독·병합 경로가 없으면 로봇은 잎을 회피하지 않는다.

대응:

- ground-truth foliage mesh 제외 정책은 유지한다.
- Personal PC 1에서 수신하고 검증한 leaf proxy만 별도의 perception-derived obstacle 계층으로 병합한다.
- 정적 trunk/branch proxy와 동적 leaf proxy의 생성 주기와 소유권을 구분한다.

### 8.3 scene version 반복 증가

카메라 결과가 매 프레임 조금씩 변할 때마다 `scene_version`을 증가시키면 Personal PC 1의 `HarvestTarget`이 계속 이전 version이 되어 GPU PC 1에서 거부될 수 있다.

대응:

- raw observation sequence와 최종 planning `scene_version`을 구분한다.
- 안정화된 leaf proxy 구성이 의미 있게 달라질 때만 scene을 갱신한다.
- 변경 판단 위치·크기·개수 기준은 `TBD`다.
- scene 갱신 후 Personal PC 1이 최신 `SimulationState`를 수신하고 새 target을 발행하도록 한다.

### 8.4 RRT/RMPflow world 불일치

RRT에는 새 leaf proxy를 추가했지만 RMPflow에는 반영하지 않거나, 반대 순서로 적용하면 계획 경로와 실행 중 회피 world가 달라진다.

대응:

- 동일한 검증된 proxy snapshot과 safety margin을 RRT와 RMPflow에 적용한다.
- Action 승인 시 사용한 leaf generation을 기록한다.
- 실행 전에 같은 generation으로 경로를 다시 검증한다.

### 8.5 obstacle 제거 실패

사라진 잎 proxy를 RMPflow나 USD runtime obstacle에서 제거하지 않으면 보이지 않는 장애물이 계속 남는다.

대응:

- proxy ID별 add, update, disable/remove lifecycle을 관리한다.
- 정상 `NO_LEAF` 시 이전 leaf proxy를 제거한다.
- reset 시 모든 perception-derived leaf obstacle을 제거한다.

### 8.6 proxy 과다로 인한 경로 실패

나뭇잎이 많은 장면을 작은 sphere 수백 개로 표현하면 RRT 수렴 시간이 증가하거나 모든 경로가 막힐 수 있다.

대응:

- 로봇 작업영역과 후보 경로 corridor 주변 proxy만 선택한다.
- 가까운 proxy를 우선한다.
- 최대 leaf proxy 수를 trunk/branch 제한과 별도로 관리한다.
- proxy 병합과 단순화를 적용하되 승인된 최소 안전거리를 축소하지 않는다.

### 8.7 실행 중 장애물 변경

RRT는 실행 중 반응형 회피 계층이 아니다. 실행 중 leaf scene이 의미 있게 바뀌었는데 기존 경로를 계속 실행하면 새 장애물과 겹칠 수 있다.

대응:

- 현재 Action을 중단한다.
- 로봇을 현재 자세에서 안전하게 정지시킨다.
- 최신 leaf snapshot으로 재계획한다.
- 안전한 재계획이 없으면 움직이지 않고 실패를 보고한다.

### 8.8 인식 stream stale

Personal PC 1 연결이 끊겼는데 마지막 leaf obstacle만 계속 사용하면 사라진 장애물과 새로 나타난 장애물을 구분할 수 없다.

대응:

- simulation time 기반 leaf stream deadline을 적용한다.
- 계획 전 stream freshness를 확인한다.
- 실행 중 stale 발생 시 fail-open으로 장애물을 삭제하지 않는다.
- 정지·유지·실패 중 최종 정책과 시간값은 `TBD`이며 사용자 승인이 필요하다.

## 9. 공유 ROS 2 인터페이스 후보

다음은 구현 전 승인해야 할 후보이며 아직 확정 계약이 아니다.

```text
토픽 후보: /harvest/leaf_obstacles
타입 후보: appleproj_interfaces/msg/LeafObstacleArray
송신: Personal PC 1
수신: GPU PC 1
QoS 후보: Reliable, Volatile, Keep Last 1
frame_id: world
```

`LeafObstacleArray` 필드 후보:

- `header`: RGB-D 촬영 simulation time, `frame_id=world`
- `reset_id`
- `observed_scene_version`
- `observation_sequence`
- `status`
- `message`
- `ObstacleProxy[] obstacles`

`ObstacleProxy`에는 `CLASS_LEAF` 추가가 필요하다. 최종 메시지 이름, 필드, 토픽 이름, QoS 및 status enum은 `TBD`이며 공유 인터페이스 변경 승인을 받은 뒤 확정한다.

## 10. PC 간 통합 순서

1. 공유 leaf obstacle 메시지와 상태 의미를 확정한다.
2. `appleproj_interfaces`를 수정하고 네 PC에서 동일 버전을 빌드한다.
3. Personal PC 1에서 저장 RGB-D 기반 offline 검출을 검증한다.
4. Personal PC 1에서 live RGB-D, TF 및 SimulationState 통합을 검증한다.
5. Personal PC 1 결과를 RViz 또는 별도 debug 표시로 world 좌표에서 확인한다.
6. GPU PC 1에서 leaf subscriber와 메시지 검증만 먼저 적용한다.
7. GPU PC 1 planning scene에 leaf proxy를 표시하되 로봇은 움직이지 않는다.
8. 정적 자세에서 RRT 경로가 leaf proxy를 우회하는지 검사한다.
9. 시간 매개화 trajectory와 RMPflow world가 같은 proxy를 사용하는지 확인한다.
10. 저속 실행 시험 후 stale, reset, obstacle 변경 및 경로 실패 처리를 검증한다.
11. 모든 실패 시험을 통과한 뒤 정상 수확 상태 흐름에 연결한다.

## 11. 검증 체크리스트

### 11.1 Personal PC 1 단위 시험

- [ ] 녹색 잎 mask 생성
- [ ] 작은 노이즈 제거
- [ ] 사과 영역 제외
- [ ] RGB/Depth 해상도 불일치 거부
- [ ] RGB/Depth timestamp 불일치 거부
- [ ] 16UC1 millimetre Depth 변환
- [ ] 32FC1 metre Depth 처리
- [ ] 유효하지 않은 Depth 제거
- [ ] CameraInfo 역투영 계산
- [ ] 촬영 시각 TF world 변환
- [ ] voxel downsampling
- [ ] sphere proxy 생성
- [ ] 안정적인 obstacle ID 생성
- [ ] 정상 `NO_LEAF`와 오류 상태 구분
- [ ] reset 시 모든 캐시 폐기

### 11.2 Personal PC 1 통합 시험

- [ ] live RGB-D 입력에서 debug mask 확인
- [ ] world proxy가 실제 잎 위치와 정렬되는지 확인
- [ ] 같은 장면에서 ID와 proxy가 불필요하게 진동하지 않는지 확인
- [ ] 잎 제거 후 빈 정상 결과 발행 확인
- [ ] TF 중단과 네트워크 지연 상태 확인
- [ ] 목표 입력 해상도와 FPS에서 처리 주기 측정

### 11.3 GPU PC 1 단위 시험

- [ ] `CLASS_LEAF` 직렬화·역직렬화
- [ ] 잘못된 frame 거부
- [ ] reset mismatch 거부
- [ ] stale 메시지 거부
- [ ] NaN, Inf, 음수 크기 및 잘못된 quaternion 거부
- [ ] 최대 proxy 수 제한
- [ ] leaf add, update, remove lifecycle
- [ ] 정상 `NO_LEAF` 처리
- [ ] 인식 오류를 무장애물로 처리하지 않는지 확인
- [ ] scene version 변경 조건 확인

### 11.4 GPU PC 1 시뮬레이션 시험

- [ ] 잎이 없는 경우 기존 경로 유지
- [ ] 직선 경로에 잎 proxy가 있을 때 우회 경로 생성
- [ ] 로봇 전체 링크와 leaf proxy의 최소 clearance 확인
- [ ] 우회 경로가 없으면 로봇을 움직이지 않고 실패 처리
- [ ] 실행 전 leaf scene 변경 시 재계획
- [ ] 실행 중 leaf scene 변경 시 정지 후 재계획
- [ ] leaf stream stale 시 승인된 fail-safe 처리
- [ ] reset 시 이전 leaf obstacle과 RRT tree 폐기
- [ ] RRT와 RMPflow가 동일 proxy snapshot을 사용하는지 확인
- [ ] 반복 scene 갱신으로 무한 재계획하지 않는지 확인

### 11.5 End-to-End 완료 기준

- [ ] Personal PC 1이 베이스 카메라의 잎을 안정적으로 검출한다.
- [ ] 검출 결과가 촬영 시각 기준의 올바른 world 위치로 변환된다.
- [ ] GPU PC 1이 검증된 leaf proxy만 planning scene에 채택한다.
- [ ] leaf proxy가 직접 경로를 막을 때 로봇 팔이 충돌 없는 우회 경로를 사용한다.
- [ ] 안전한 경로가 없거나 인식 상태가 유효하지 않으면 로봇이 이동하지 않는다.
- [ ] reset, stale, 네트워크 단절 및 장애물 변경 시 이전 결과를 안전하게 폐기한다.
- [ ] RViz 장애와 무관하게 GPU PC 1의 planner와 안전 처리가 동작한다.

## 12. GPU PC 1 수정 검토 요청

현재 실행 PC는 Personal PC 1이므로 다음 GPU PC 1 소유 소스를 직접 수정하지 않는다. GPU PC 1 소유자에게 아래 내용을 검토 요청한다.

### 대상 파일과 기능

| 파일 | 검토 대상 |
|---|---|
| `vision_apple_pick.py` | leaf obstacle 구독, 메시지 검증, planning scene 발행 및 class 매핑 |
| `apple_pick.py` | 검증된 leaf sphere를 RRT/RMPflow world에 추가·갱신·제거, 실행 중 변경 처리 |
| `harvest_route_planner.py` | leaf class 분류, corridor 선택, proxy 수 제한 및 clearance 검사 |
| `harvest_coordinator.py` | scene generation, target admission, stale 및 재계획 상태 연결 |
| `tests/test_harvest_route_planner.py` | leaf proxy 경로 회피 단위 시험 |
| `tests/test_harvest_coordinator.py` | version, stale, reset 및 오류 상태 시험 |

### 관찰된 문제

- 현재 obstacle class 매핑은 trunk와 branch만 지원한다.
- foliage는 planning geometry 수집에서 명시적으로 제외된다.
- Personal PC 1 obstacle 후보를 수신하는 인터페이스가 없다.
- leaf add, update, remove lifecycle이 없다.
- 동적 leaf generation과 기존 `scene_version`의 상호작용이 정의되지 않았다.

### 제안 동작

- ground-truth foliage mesh는 계속 제외한다.
- Personal PC 1이 발행한 perception-derived leaf proxy만 검증 후 사용한다.
- RRT와 RMPflow에 동일 snapshot과 safety margin을 적용한다.
- 실행 중 의미 있는 leaf 변경을 감지하면 정지 후 재계획한다.
- stale, reset mismatch 또는 잘못된 메시지는 장애물 없음으로 해석하지 않는다.

### 인터페이스 영향

- `ObstacleProxy.CLASS_LEAF` 추가 필요
- leaf obstacle 배열 메시지 및 토픽 추가 필요
- `scene_version` 또는 별도 observation generation 규약 확정 필요
- 네 PC에서 `appleproj_interfaces` 동일 버전 재빌드 필요

### 검증 절차

- 새 class와 메시지 단위 시험
- 정적 leaf proxy를 이용한 RRT 우회 시험
- RMPflow obstacle 일치 시험
- live Personal PC 1 입력 연동 시험
- stale, reset, 네트워크 단절 및 obstacle 변경 실패 시험
- 안전한 경로가 없는 경우 정지·실패 처리 확인

## 13. 승인 또는 추가 결정이 필요한 `TBD`

- 검출 방식의 MVP 범위: HSV 또는 semantic segmentation
- HSV 범위와 최소 contour 면적
- RGB/Depth 동기화 허용 오차
- 유효 Depth 범위와 최소 유효 비율
- leaf voxel 크기
- leaf proxy 반지름과 safety margin
- 최대 leaf proxy 수
- obstacle 추가·제거 temporal hysteresis
- material change 판단 기준
- leaf stream stale 시간과 fail-safe 정책
- 토픽 이름, 메시지 필드, status enum 및 QoS
- `scene_version`과 observation sequence의 관계
- 실제 회피 성공을 판정할 최소 clearance

위 값은 시뮬레이션 시험을 통해 조정하되, 임시값과 최종값 모두 사용자 승인 없이 영구 요구사항으로 확정하지 않는다.
