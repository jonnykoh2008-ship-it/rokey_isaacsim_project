# 개인 PC 1 다중 사과 수확 인식 작업 목록

## 문서 목적

이 문서는 `personal_pc1_multi_apple_harvest.md` 수정 요청을 개인 PC 1에서
구현하기 위한 작업 목록과 완료 조건을 정리한다. 개인 PC 1 소유 기능과 GPU PC 1에
확인하거나 변경을 요청해야 하는 기능을 분리한다.

이 문서는 구현 계획이며 미확정 요구사항을 임의로 확정하지 않는다. 최종 robot별
ROS namespace, TF frame, tree 영역 판정 방식 및 오류 코드는 공동 승인 전까지
`TBD`로 유지한다.

## 적용 기준

- 실행·소유 PC: 개인 PC 1
- 주요 대상 소스: `base_apple_detector.py`
- 단위 테스트: `tests/test_base_apple_detector.py`
- 입력 권위자: GPU PC 1의 Isaac Sim 5.1.0
- 실행 환경: ROS 2 Jazzy, Fast DDS, Ubuntu 24.04
- 시간 기준: Isaac Sim `/clock`, 모든 ROS 2 노드 `use_sim_time:=true`
- 개별 연동 시험 Domain: `ROS_DOMAIN_ID=102`
- 전체 시스템 통합 Domain: `ROS_DOMAIN_ID=101`

관련 기준 문서:

- `docs/modification_requests/personal_pc1_multi_apple_harvest.md`
- `docs/features/harvest_perception.md`
- `docs/architecture/tf_frames.md`
- `docs/architecture/ros2_interfaces.md`
- `docs/architecture/hardware_network.md`

## 개인 PC 1의 역할

개인 PC 1은 GPU PC 1에서 받은 RGB-D, CameraInfo, TF 및 SimulationState를 사용해
사과를 검출하고 안정적인 target ID와 world 좌표를 생성하는 수확 인식 PC다.

개인 PC 1이 담당한다:

- RGB, Depth 및 CameraInfo 구독
- RGB와 Depth timestamp 동기화
- 사과 contour 검출과 검출 품질 계산
- depth projection을 이용한 camera 좌표계 3D 중심 계산
- 촬영 timestamp 기준 camera 좌표에서 `world` 좌표로 변환
- 최초 유효 후보 집합의 고정 target ID 생성
- 프레임 간 100 mm 최근접 일대일 tracking
- 현재 관측된 모든 유효 track의 `HarvestTarget` 발행
- 인식 실패 및 입력 오류의 `HarvestPerceptionStatus` 발행
- debug 영상과 tracker ID 표시
- reset에 따른 입력 cache, tracker, ID 및 발행 이력 초기화
- GPU PC 1의 planning 결과와 상태를 원격 RViz에 표시

개인 PC 1이 담당하지 않는다:

- 접근 orientation 및 pre-grasp pose 결정
- Lula RRT, trajectory 또는 RMPflow 경로 계획
- planning obstacle 최종 판정과 안전거리 적용
- 로봇 관절, 그리퍼 또는 RobotMotion Action 실행
- 수확 순서, 실패 재시도 순서 또는 안전 정지 결정
- TF 발행 또는 재발행

## 현재 구현 상태

`base_apple_detector.py`의 현재 작업 트리에는 다음 기능이 이미 반영돼 있다.
이 변경은 아직 최종 검증과 배포가 완료된 상태를 의미하지 않는다.

- [x] 필수 단일 `target_id` parameter 제거
- [x] `apple_001`, `apple_002`, ... ID 생성
- [x] robot base와의 world 3D 거리순 최초 ID 정렬
- [x] 동거리 후보의 world XYZ tie-break
- [x] 최초 ID 생성 시 robot base TF가 없으면 초기화 보류
- [x] 100 mm 이내 world 최근접 track 연결
- [x] 한 후보의 두 track 중복 배정 방지
- [x] 같은 `reset_id`에서 신규 ID 생성 방지
- [x] 프레임별 현재 관측 track 전체 발행
- [x] `/harvest/target` publisher QoS depth 10
- [x] reset 시 RGB-D cache, tracker, ID 및 발행 이력 초기화
- [x] debug 영상의 tracker ID 표시
- [x] 발행 ID 목록 최대 1 Hz 로그
- [x] 기본 다중 사과 단위 테스트 초안

아직 구현하거나 보완해야 한다:

- [ ] 필수 `robot_id` parameter와 허용값 검증
- [ ] robot별 입력 topic과 camera frame 선택
- [ ] robot별 base frame parameter 적용
- [ ] camera/debug 출력 topic parameter화
- [ ] RGB, Depth, CameraInfo frame 일치 검증
- [ ] reset 시 CameraInfo cache 폐기
- [ ] 담당 tree 영역 불일치 target 차단
- [ ] tree 영역 불일치 진단 상태 발행
- [ ] reset 전 지연 도착 영상 차단 규칙
- [ ] 두 robot detector 동시 실행 시 target ID와 namespace 충돌 해결
- [ ] GPU PC 1과 ROS 2/Fast DDS 통합 시험

## 개인 PC 1 구현 작업

### 1. 실행 profile과 parameter

- [ ] `robot_id`를 필수 ROS parameter로 선언한다.
- [ ] 허용값을 `robot_01`, `robot_02`로 제한한다.
- [ ] 빈 값이나 알 수 없는 값은 노드 시작 시 명확한 오류로 중단한다.
- [ ] 임의 robot을 기본값으로 선택하지 않는다.
- [ ] 선택한 robot profile을 시작 로그에 남긴다.

승인된 USD 입력 매핑:

| `robot_id` | 카메라 Prim | 담당 USD 영역 |
|---|---|---|
| `robot_01` | `/World/base_rsd455_01` | `/World/Xform` |
| `robot_02` | `/World/base_rsd455_02` | `/World/Xform_03` |

ROS camera topic, camera frame 및 robot base frame의 최종 이름은 GPU PC 1과의
공동 승인 전까지 `TBD`다. USD Prim 이름을 ROS 이름으로 임의 확정하지 않는다.

### 2. 입출력 topic parameter화

- [ ] RGB topic을 ROS parameter로 전환한다.
- [ ] Depth topic을 ROS parameter로 전환한다.
- [ ] CameraInfo topic을 ROS parameter로 전환한다.
- [ ] camera frame을 ROS parameter 또는 승인된 robot profile로 선택한다.
- [ ] robot base frame을 ROS parameter로 전환한다.
- [ ] camera debug pose topic을 parameter화한다.
- [ ] debug image topic을 parameter화한다.
- [ ] target/status topic은 현재 공통 계약을 기본값으로 유지하되 robot별 최종
  namespace를 코드 상수로 확정하지 않는다.
- [ ] 시작 로그에 실제 선택된 topic과 frame을 모두 출력한다.

### 3. 입력 검증과 동기화

- [ ] RGB와 Depth의 timestamp 차이가 허용값을 넘으면 오래된 입력만 폐기한다.
- [ ] 이미 처리한 timestamp 또는 out-of-order RGB를 다시 처리하지 않는다.
- [ ] RGB와 Depth의 해상도가 다르면 해당 프레임을 거부한다.
- [ ] RGB, Depth 및 CameraInfo가 선택된 camera frame과 일치하는지 확인한다.
- [ ] 빈 image frame을 `base_camera`로 자동 대체하지 않고 설정 오류로 진단한다.
- [ ] CameraInfo의 `fx`, `fy` 및 영상 크기가 유효한지 확인한다.
- [ ] CameraInfo timestamp 동기화 정책은 승인 전까지 `TBD`로 둔다.

### 4. 후보 검출과 3D 변환

- [ ] 한 프레임의 모든 최소 면적 이상 빨간 contour를 후보로 유지한다.
- [ ] confidence threshold 미달 후보를 target에서 제외한다.
- [ ] 유효 depth 픽셀이 부족한 후보를 제외한다.
- [ ] 사과 표면 depth에서 camera 좌표계 중심을 계산한다.
- [ ] RGB 촬영 timestamp로 camera frame에서 `world` TF를 조회한다.
- [ ] TF를 조회할 수 없는 후보를 발행하지 않는다.
- [ ] 최초 ID 초기화 프레임에서 일부 후보만 TF 변환된 경우 초기화를 보류한다.

### 5. 최초 ID 초기화

- [ ] SimulationState가 `READY` 또는 `PLAYING`일 때만 초기화한다.
- [ ] 촬영 timestamp의 robot base 원점을 `world`에서 조회한다.
- [ ] robot base TF가 없으면 XYZ 순서로 대체하지 않고 초기화를 보류한다.
- [ ] 후보를 robot base와의 world 3D 거리 오름차순으로 정렬한다.
- [ ] 거리가 같으면 world `(x, y, z)` 오름차순으로 정렬한다.
- [ ] 정렬 결과에 `apple_001`, `apple_002`, ... ID를 순서대로 부여한다.
- [ ] 최초 ID 집합 생성 후 같은 `reset_id`에서는 신규 ID를 추가하지 않는다.

### 6. 프레임 간 tracking

- [ ] 각 track의 마지막 world position을 저장한다.
- [ ] 모든 track-candidate world 거리 조합을 계산한다.
- [ ] 100 mm를 초과하는 연결 후보를 제외한다.
- [ ] 거리와 결정적 tie-break 기준으로 연결 후보를 정렬한다.
- [ ] 사용되지 않은 track과 candidate만 일대일로 연결한다.
- [ ] 전체 배정이 끝난 뒤 track의 마지막 위치를 갱신한다.
- [ ] 관측되지 않은 기존 track은 삭제하지 않는다.
- [ ] 연결되지 않은 신규 후보는 `UNMATCHED`로 표시하고 새 ID를 만들지 않는다.

### 7. target과 상태 발행

- [ ] 관측과 world 변환에 성공한 모든 track을 매 프레임 발행한다.
- [ ] 모든 target에 동일 RGB-D 촬영 timestamp를 사용한다.
- [ ] `header.frame_id`를 `world`로 설정한다.
- [ ] `target_id`, `reset_id`, `scene_version`을 채운다.
- [ ] world 중심 position을 채운다.
- [ ] 원본 camera frame의 `source_point`와 동일 timestamp를 보존한다.
- [ ] `confidence`, `valid_depth_ratio`, `tf_time_error_sec`를 채운다.
- [ ] target publisher QoS를 `Reliable + Volatile + Keep Last 10`으로 유지한다.
- [ ] 서로 다른 target ID의 `OK` 상태가 1 Hz throttle 때문에 잘못 합쳐지는지
  검토한다.

### 8. reset 처리

- [ ] `reset_id` 변경을 감지한다.
- [ ] 대기 중인 RGB와 Depth를 폐기한다.
- [ ] CameraInfo cache를 폐기한다.
- [ ] 마지막 처리 timestamp를 초기화한다.
- [ ] 모든 track과 tracker 초기화 상태를 폐기한다.
- [ ] ID counter를 1로 되돌린다.
- [ ] target 발행 이력과 debug/log throttle 이력을 초기화한다.
- [ ] 새 세대의 최초 target이 다시 `apple_001`부터 시작하는지 확인한다.

### 9. debug와 운영 진단

- [ ] 각 후보에 track ID 또는 거부 사유를 표시한다.
- [ ] 프레임별 실제 발행 ID 목록을 debug 영상에 표시한다.
- [ ] 후보 수, world 변환 수, 발행 ID 및 미연결 후보 수를 최대 1 Hz로 기록한다.
- [ ] 시작 로그에 `robot_id`, topic, camera frame, base frame 및 QoS를 출력한다.
- [ ] debug GUI가 없는 환경에서도 노드가 계속 실행되도록 유지한다.

## 오류 처리 기준

| 조건 | 개인 PC 1 동작 | 상태 |
|---|---|---|
| contour 없음 | target 미발행 | `NO_DETECTION` |
| 유효 depth 부족 | 후보 제외 | `DEPTH_INVALID` |
| confidence 미달 | 후보 제외 | `LOW_CONFIDENCE` |
| RGB/Depth timestamp 불일치 | 오래된 입력 폐기 | `INPUT_NOT_SYNCHRONIZED` |
| camera-to-world TF 없음 | 후보 또는 프레임 미발행 | `TF_UNAVAILABLE` |
| robot-base-to-world TF 없음 | 최초 ID 초기화 보류 | `TF_UNAVAILABLE` |
| SimulationState가 READY/PLAYING 아님 | target 미발행 | `SIMULATION_NOT_READY` |
| stale 영상 | target 미발행 | `STALE_FRAME` (`TBD` 기준 필요) |
| reset 세대 불일치 | target 미발행 | `RESET_MISMATCH` (판별 입력 `TBD`) |
| robot/camera frame 불일치 | target 미발행 | 상태 코드 `TBD` |
| 담당 tree 영역 불일치 | 후보 제외 | 상태 코드 `TBD` |
| 내부 처리 예외 | 해당 프레임 중단 | `INTERNAL_ERROR` |

## GPU PC 1에 확인할 사항

### 운용 방식

- [ ] 한 번에 robot 하나만 실행하는지 두 robot을 동시에 실행하는지 확정한다.
- [ ] 단일 robot 순차 운용이면 robot 전환과 reset 절차를 확정한다.
- [ ] 동시 운용이면 전체 robot별 ROS namespace와 TF 분리 작업을 별도 승인한다.

### 카메라 입력

- [ ] robot별 RGB topic 이름을 확인한다.
- [ ] robot별 Depth topic 이름을 확인한다.
- [ ] robot별 CameraInfo topic 이름을 확인한다.
- [ ] 실제 image/CameraInfo `header.frame_id`를 확인한다.
- [ ] 현재 `base_camera` 호환 frame을 유지할지 robot별 frame으로 바꿀지 결정한다.
- [ ] 카메라 TF가 영상 촬영 timestamp에서 조회되는지 확인한다.

### robot TF

- [ ] robot별 base frame 이름을 확정한다.
- [ ] robot별 `odom`, link 및 `palm` frame 이름 또는 namespace를 확정한다.
- [ ] 두 robot 동시 운용 시 동일 `base_link`/`palm` TF 중복 발행을 제거한다.
- [ ] `/clock` 권위자는 한 개만 유지한다.

### target과 coordinator

- [x] GPU PC 1 target subscriber가 `Reliable + Volatile + Keep Last 10`을
  사용하는지 소스에서 확인했다.
- [x] 현재 coordinator lifecycle key가 `(reset_id, target_id)`임을 확인했다.
- [ ] 두 robot의 `apple_001` 충돌을 해결할 namespace 또는 interface 정책을
  확정한다.
- [ ] 실행을 시작하지 않은 ID의 최신 표본을 대기열에 저장하는지 통합 확인한다.
- [ ] 실행을 시작한 ID의 후속 갱신이 새 Goal을 만들지 않는지 확인한다.
- [ ] stale target과 reset/scene mismatch target이 거부되는지 확인한다.
- [ ] 접근 전 첫 실패의 1회 후순위 재시도와 접촉 후 안전 정지를 확인한다.

### tree 영역 검증

- [ ] robot별 담당 tree의 world bounding box, tree TF 또는 승인된 ROI 중 하나를
  제공한다.
- [ ] 개인 PC 1이 target의 tree 소속을 판단할 수 있는 입력 계약을 확정한다.
- [ ] 영역 불일치에 사용할 `HarvestPerceptionStatus` 코드를 확정한다.
- [ ] `HarvestTarget.robot_id/tree_id` 추가 여부는 별도 공동 interface 작업으로
  유지한다.

### 세대와 시간

- [ ] Stop/Reset 후 `reset_id`가 증가하는지 확인한다.
- [ ] planning scene 변경 후 `scene_version`이 증가하는지 확인한다.
- [ ] RGB-D, TF, SimulationState 및 target이 모두 `/clock`을 사용하는지 확인한다.
- [ ] reset 전 지연 영상의 판별·폐기 방식을 확정한다.
- [ ] stale age, confidence, valid-depth 및 TF 시간 오차 threshold를 승인한다.

## 확인된 충돌과 주의사항

### 동시 다중 로봇 차단 사항

- GPU PC 1 카메라 publisher는 robot Prim을 선택하지만 두 profile 모두 공통
  `/base_camera/...` topic과 `base_camera` frame을 사용한다.
- GPU PC 1 robot TF는 공통 `odom`, `base_link`, link 및 `palm` frame을 사용한다.
- coordinator key에는 `robot_id`가 없으므로 서로 다른 robot의 동일 target ID를
  구분하지 못한다.
- `/simulation/state`, `/planning_scene`, `/joint_states`, RobotMotion Action 및
  MotionStatus도 공통 이름이다.
- 두 GPU 실행이 각각 `/clock`을 발행하면 simulation time 권위가 충돌한다.

따라서 현재 GPU PC 1 구조에서는 한 번에 한 robot을 선택하는 운용만 안전하다.
두 robot 동시 운용은 GPU PC 1 소유 source와 공동 interface의 별도 변경 승인이
필요하다.

### 개인 PC 1 현재 코드 주의사항

- reset 시 CameraInfo cache가 남아 있다.
- 빈 camera frame을 `base_camera`로 자동 대체한다.
- RGB, Depth와 CameraInfo의 frame 일치를 확인하지 않는다.
- `STALE_FRAME`과 `RESET_MISMATCH`의 완전한 판별 로직이 없다.
- confidence, valid-depth, stale age 및 TF 시간 threshold 중 일부는 승인 전
  sentinel로 비활성화돼 있다.
- status throttle이 status 코드만 비교하므로 서로 다른 target의 동일 상태를
  합칠 수 있다.
- 현재 다중 사과 source와 단위 테스트는 작업 트리에서 최종 검증·배포되지 않은
  상태다.

## 단위 테스트 목록

- [ ] 최소 3개 후보가 robot base 거리순으로 `apple_001`~`apple_003`이 되는지
  확인한다.
- [ ] contour 순서를 바꿔도 ID가 유지되는지 확인한다.
- [ ] 거리 동률에서 world XYZ tie-break가 적용되는지 확인한다.
- [ ] 100 mm 밖의 후보가 신규 ID가 되지 않는지 확인한다.
- [ ] 한 후보가 두 track에 연결되지 않는지 확인한다.
- [ ] 사라진 track을 삭제하지 않고 관측된 track만 발행하는지 확인한다.
- [ ] reset 후 ID가 `apple_001`부터 다시 시작하는지 확인한다.
- [ ] reset 후 RGB, Depth, CameraInfo 및 발행 이력이 모두 초기화되는지 확인한다.
- [ ] 최초 robot base TF가 없으면 ID 초기화와 target 발행을 보류하는지 확인한다.
- [ ] 세 target이 한 프레임에서 같은 timestamp와 세대 메타데이터를 보존하는지
  확인한다.
- [ ] 잘못된 `robot_id`를 거부하는지 확인한다.
- [ ] robot별 topic/frame override가 적용되는지 확인한다.
- [ ] image/CameraInfo frame 불일치를 거부하는지 확인한다.
- [ ] 담당 tree 밖 후보를 등록·연결·발행하지 않는지 확인한다.

## 통합 시험 목록

- [ ] 개인 PC 1과 GPU PC 1에서 동일 ROS interface 버전을 사용한다.
- [ ] 양쪽의 `RMW_IMPLEMENTATION`과 Fast DDS 설정을 확인한다.
- [ ] 격리된 연동 시험에서 양쪽 `ROS_DOMAIN_ID=102`를 확인한다.
- [ ] 전체 시스템 시험에서는 모든 PC의 `ROS_DOMAIN_ID=101`을 확인한다.
- [ ] `use_sim_time:=true`와 `/clock` 수신을 확인한다.
- [ ] robot별 RGB, Depth 및 CameraInfo 수신을 확인한다.
- [ ] 영상 timestamp에서 camera-to-world와 robot-base-to-world TF 조회를 확인한다.
- [ ] 한 프레임의 세 target을 GPU PC 1이 모두 수신하는지 확인한다.
- [ ] GPU PC 1이 세 ID를 서로 다른 대기열 항목으로 보관하는지 확인한다.
- [ ] 동일 ID의 최신 좌표 갱신이 중복 Goal을 만들지 않는지 확인한다.
- [ ] reset 후 이전 세대 target과 지연 영상이 사용되지 않는지 확인한다.
- [ ] target-to-plan 지연과 TF-target timestamp 오차를 기록한다.

## 완료 조건

개인 PC 1 작업은 다음 조건을 모두 충족해야 완료로 판단한다.

- [ ] 승인된 robot 운용 방식과 topic/frame 계약이 적용됐다.
- [ ] 다중 사과 tracker 단위 테스트가 모두 통과한다.
- [ ] reset과 세대 전환 테스트가 모두 통과한다.
- [ ] 담당 영역 검증 방식과 진단 상태가 승인·구현됐다.
- [ ] GPU PC 1이 한 프레임의 모든 target ID를 유실 없이 수신한다.
- [ ] GPU PC 1 coordinator가 ID별 lifecycle을 올바르게 유지한다.
- [ ] `/clock`, TF timestamp, `reset_id` 및 `scene_version` 계약이 유지된다.
- [ ] ROS 2 Jazzy/Fast DDS 통합 시험 결과가 기록됐다.
- [ ] 변경 파일, 실행 명령, 시험 환경 및 결과가 최종 보고됐다.

## GPU PC 1 수정 검토 요청 대상

동시 다중 로봇 운용이 요구되면 개인 PC 1이 GPU PC 1 source를 직접 변경하지 않고
다음 수정 검토 요청을 전달한다.

- 대상 파일·기능:
  - `base_camera_publish.py`: robot별 camera topic/frame
  - `vision_apple_pick.py`: robot별 TF, state, planning scene 및 Action namespace
  - `harvest_coordinator.py`: robot별 target 구독과 lifecycle key
- 관찰된 문제:
  - 두 profile이 공통 ROS topic/frame을 사용한다.
  - `(reset_id, target_id)`만으로 robot별 target을 구분할 수 없다.
- 제안 동작:
  - `/clock`은 공통 권위자 하나로 유지한다.
  - robot별 센서, TF, planning, target 및 Action 경계를 승인된 namespace로
    분리하거나 shared interface에 `robot_id`를 추가한다.
- interface 영향:
  - namespace만 변경할지 메시지 필드를 추가할지 공동 결정이 필요하다.
- 검증:
  - 두 robot의 camera/TF/target을 동시에 발행해 frame과 lifecycle key가 서로
    섞이지 않는지 시험한다.
