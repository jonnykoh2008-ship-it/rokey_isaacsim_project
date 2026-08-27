# GPU PC 1 이식 노트

GPU PC 1이 멈춘 동안 GPU PC 2에서 수확 스택을 되살리며 고친 내용이다.
이식할 때 무엇을 옮겨야 하는지, 그리고 왜 그렇게 고쳤는지를 남긴다.

옮겨야 할 것은 **USD 씬 수정**, **코드 수정**, **Isaac용 인터페이스 빌드** 세 가지다.

## 1. USD 씬 수정 (`m0617_3fgripper08201638.usd`)

로봇 1대짜리 씬에 두 번째 로봇과 나무를 복사하면서 생긴 문제들이다. 복사는
transform 은 갱신하지만 조인트 상태·앵커·참조 경로는 갱신하지 않는다는 점이
공통 원인이다.

| # | 문제 | 조치 | 증상 |
|---|---|---|---|
| 1 | 에셋 참조 5건이 `/home/rokey/cobot3_ws/...` 절대경로 | 저장소 상대경로로 변경 | 로봇 2 그리퍼 미로드 (관절 10개, 정상 23개) |
| 2 | `m0617_02/FixedJoint_03`, `ConveyorTrack` 이름 불일치 | 코드가 요구하는 이름으로 rename | `require_prim` 실패로 물리 시작 전 중단 |
| 3 | rename 이 relationship 2건을 끊음 | 새 경로로 복구 | 컨베이어 그래프가 사라진 prim 을 구동 |
| 4 | 레일 월드 앵커가 두 로봇 모두 `(1.5, 2.5, 0)` | 각 레일 실제 위치로 | Play 시 레일이 앵커로 끌려감 |
| 5 | 로봇 1 레일 state 가 캐리지 위치와 2m 불일치 | state 0 → 2.000 | **Play 시 로봇 1이 2m 순간이동** |
| 6 | 로봇 2 `joint_1` state/target 5도 차이 | target 을 state 에 맞춤 | Play 시 팔이 튕김 |
| 7 | base 카메라 두 대가 서로 반대 로봇에 위치 | transform 맞교환 | 로봇 2 검출기가 로봇 1 나무의 사과를 발행 |
| 8 | 맞교환이 회전까지 옮겨 각 카메라가 남의 나무를 향함 | 자기 나무로 재조준 (124.68도, 112.50도 -> 0.00도) | 사과가 화각(90도) 밖이라 자기 나무가 안 보임 |

### 카메라 조준은 반드시 자식 prim 기준으로

`base_rsd455_xx` 는 껍데기이고 실제로 렌더링하는 것은 그 아래
`RSD455/Camera_OmniVision_OV9782_Color` 다. 자식은 payload 안에 자체 변환을
가지고 있어서 **껍데기를 회전시켜도 광학 프레임이 예측대로 향하지 않는다.**
그리고 payload 는 일반 USD 리더에서 열리지 않으므로 자식의 오프셋을 오프라인
으로는 읽을 수 없다.

Isaac 런타임에서 자식이 원하는 자세가 되도록 껍데기를 역산해야 한다.

```
M_child_world = M_child_rel_holder x M_holder_world
=> M_holder_world = inverse(M_child_rel_holder) x M_child_desired
```

컨베이어 카메라(`conv_rsd455`)도 같은 구조라 같은 함정이 있다. 조준을 바꾼
뒤에는 **자식 prim 의 조준 오차**를 검증하고, 통과했을 때만 저장한다.

### rename 할 때 주의

USD 에서 `spec.name` 으로 이름만 바꾸면 **그 경로를 가리키던 relationship 이
자동으로 갱신되지 않는다.** 3번이 그렇게 생겼다. rename 뒤에는 dangling
relationship 을 반드시 검사한다.

### 순간이동 진단법

Play 직후 튀는 것은 대부분 **조인트 프레임과 바디 실제 위치의 불일치**다.
PhysX 가 조인트를 만족시키려고 바디를 끌어당긴다. 검사 방법은 조인트마다
`body0 world x localPos0` 과 `body1 world x localPos1` 을 계산해 두 결과의
거리를 재는 것이다. 1mm 를 넘으면 스냅이 일어난다.

prismatic 조인트는 슬라이드 거리만큼 차이가 나는 것이 정상이므로 이 지표를
그대로 적용하면 안 된다. 대신 `캐리지 오프셋 = localPos0 투영 + state` 관계가
성립하는지 본다. 5번이 이 방법으로 잡혔다.

## 2. 코드 수정

### 2-1. 멀티로봇 네임스페이스 (신규 `harvest_namespace.py`)

`--robot-id` 가 USD prim 과 OmniGraph 이름만 갈랐고 **ROS 2 인터페이스는 전부
전역**이었다. 두 로봇을 동시에 띄우면

- 카메라 두 대가 `/base_camera/color/image_raw` 한 토픽에 발행
- 서로 다른 위치의 카메라가 같은 TF frame `base_camera` 를 주장
- detector 두 개가 `/harvest/target` 하나에 발행
- Action 서버 `/harvest/robot_motion` 이름 충돌

수신 측이 어느 로봇의 관측인지 구분할 방법이 없었다.

`HarvestNames` 가 모든 로봇별 이름을 단독으로 결정하고 네 노드가 그 모듈을
import 한다. 발행하는 쪽과 구독하는 쪽이 같은 출처를 쓰므로 한쪽만 이름이
바뀌는 일이 생기지 않는다.

| 대상 | 이름 |
|---|---|
| 카메라 | `/<robot_id>/base_camera/{color/image_raw,depth/image_raw,camera_info}` |
| 카메라 TF frame | `<robot_id>/base_camera` (선행 슬래시 없음, tf2 규칙) |
| 검출 결과 | `/<robot_id>/harvest/target` |
| 인식 상태 | `/<robot_id>/harvest/perception_status` |
| 모션 Action | `/<robot_id>/harvest/robot_motion` |
| 모션 상태 | `/<robot_id>/harvest/motion_status` |
| 관절 상태 | `/<robot_id>/joint_states` |

컨베이어, `/clock`, planning scene 은 하나의 세계를 기술하므로 전역으로 둔다.
로봇별로 나누면 각자 다른 세계를 갖게 된다.

수정한 파일: `base_camera_publish.py`, `vision_apple_pick.py`,
`base_apple_detector.py`, `harvest_coordinator.py`.

`base_apple_detector.py` 는 개인 PC 1 소유이므로, 이식 시 그 PC 소유자에게
`--robot-id` 추가와 토픽 네임스페이스 적용을 요청해야 한다.

### 2-2. 방치 로봇 고정 (`apple_pick.py` 의 `hold_idle_robots`)

두 로봇 모두 `ArticulationRootAPI` 를 가져 PhysX 가 둘 다 시뮬레이션하는데,
`configure_joint_drives` 는 `--robot-id` 로 고른 한 대만 설정하고 나머지를
방치했다. 방치된 로봇은 drive target 이 없어 팔이 무너지고 레일이 미끄러졌다.
싱글 로봇 씬에서 문제가 없던 이유도 같다.

**주의**: 방치 로봇에 프로파일의 초기 자세를 쓰면 안 된다. 저장된 현재 자세와
다르면 Play 순간 그 자세로 순간이동한다. `state:angular:physics:position` 을
읽어 그 값을 drive target 으로 삼고, **state 는 건드리지 않는다.**

### 2-3. coordinator 의 기본 토픽

`DEFAULT_MOTION_STATUS_TOPIC` 이 모듈 로드 시점에 `robot_01` 로 굳어 있어,
`--robot-id robot_02` 로 띄워도 로봇 1의 상태 토픽을 구독했다. 빈 문자열을
기본값으로 두고 `robot_id` 에서 파생하게 고쳤다.

## 3. Isaac Python 3.11 인터페이스 빌드

`vision_apple_pick.py` 는 Isaac Sim 안에서 Action 서버를 띄우므로 커스텀
메시지가 **Isaac 의 Python 3.11** 에 있어야 한다. `colcon build` 산출물은
3.12 전용이라 import 되지 않는다.

`build_interfaces_for_isaac.sh` 가 처리한다. ROS 2 인터페이스 패키지는

- `lib<pkg>__rosidl_*.so` : 순수 C, 파이썬 버전 무관
- `<pkg>_s__rosidl_*.so` : CPython ABI 전용

로 나뉘므로, C 라이브러리는 기존 빌드를 재사용하고 확장 3개만 3.11 로
다시 컴파일한다. Isaac 안에 ROS 2 툴체인을 통째로 세울 필요가 없다.

```bash
./build_interfaces_for_isaac.sh
export APPLEPROJ_INTERFACES_PREFIX=$PWD/install_isaac311/appleproj_interfaces
```

`.msg` / `.action` 을 수정하면 `colcon build` 후 이 스크립트를 다시 돌린다.

### 함정 두 가지

**numpy ABI** — 생성된 코드가 numpy 헤더를 쓴다. 시스템 numpy 로 빌드하면
컴파일은 성공하고 런타임에 깨진다. Isaac 이 쓰는 numpy 의 헤더를 써야 한다.

**미해결 심볼** — 메시지가 품은 `builtin_interfaces`, `std_msgs` 등의
`convert_to_py` 심볼을 링크하지 않으면 import 시점에 **세그폴트**한다.
스크립트가 `ldd -r` 로 빌드 시점에 검사한다.

## 4. 실행

```bash
# 0. 한 번만
./build_interfaces_for_isaac.sh
export APPLEPROJ_INTERFACES_PREFIX=$PWD/install_isaac311/appleproj_interfaces

# 1. Isaac 수확 서버 (카메라 발행 + Action 서버를 한 프로세스에서)
PYTHONUNBUFFERED=1 ROS_DOMAIN_ID=103 ~/isaacsim/python.sh \
  vision_apple_pick.py --robot-id robot_02

# 2. 검출기 (target_id 는 필수, robot_02 는 apple_004~006)
python3 base_apple_detector.py --robot-id robot_02 \
  --ros-args -p target_id:=apple_004

# 3. 조율기 (--execute 없이 먼저 관측만)
python3 harvest_coordinator.py --robot-id robot_02
```

`PYTHONUNBUFFERED=1` 이 없으면 Isaac 종료 시 stdout 이 유실되어 아무것도 안
한 것처럼 보인다.

### 진단 순서

값이 안 나올 때는 앞에서부터 확인한다.

```bash
ros2 topic echo /simulation/state --once          # state 3 = PLAYING
ros2 topic hz /<robot>/base_camera/color/image_raw
ros2 topic echo /<robot>/harvest/perception_status --once
ros2 topic echo /<robot>/harvest/target --once
ros2 topic echo /<robot>/harvest/motion_status
```

`/simulation/state` 가 0(STOPPED) 이면 검출기는 사과를 찾아도 target 을
발행하지 않는다. 카메라도 함께 멈춘다.

## 5. 미해결

| 항목 | 상태 |
|---|---|
| 로봇 1 레일 위치 | state 2.000 으로 두었으나 나무까지 0.83m 로 로봇 2(1.37m)보다 가깝다. STAGING 구간에서 정체한다. 0.232 가 로봇 2와 같은 기하다. |
| 로봇 2 파지 실패 | 접근·파지·당김·후퇴를 모두 수행하지만 사과가 따라오지 않는다. 꼭지 조인트(15N)가 끊기지 않는다. |
| 컨베이어 카메라 2대 | `conv_rsd455_01`, `_02` 가 씬에 없다. 품질검사 3면 촬영이 막혀 있다. |
| RViz 시각화 토픽 3종 | `/harvest/planning_markers`, `planned_path`, `planned_joint_trajectory` 는 아직 전역이라 두 로봇이 동시에 발행하면 섞인다. |

## 6. 진단 도구

조사에 쓴 스크립트는 재현 가능하도록 접근법만 남긴다.

- **참조 검사** — 레이어의 reference/payload 를 순회하며 로컬 경로가 실제로
  존재하는지 확인한다. 원격(omniverse/http) 은 캐시로 해결되므로 제외한다.
- **prim 경로 검사** — 코드가 문자열로 요구하는 경로를 뽑아 stage 와 대조한다.
  런타임에 만들어지는 `Runtime*` prim 은 없는 것이 정상이다.
- **조인트 일관성 검사** — 위 "순간이동 진단법" 참고.
- **물리 이동 측정** — `World.reset()` 전후와 N 스텝 뒤의 월드 좌표를 비교한다.
  reset 직후 이미 크게 움직였으면 조인트 스냅, 서서히 커지면 중력이나
  권한 없는 drive 다. 정적 분석만으로는 5번을 찾지 못했다.
