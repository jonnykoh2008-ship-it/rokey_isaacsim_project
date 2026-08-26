# 개인 PC 1 다중 사과 검출·ID 발행 수정 요청

## 요청 정보

- 실행·소유 PC: 개인 PC 1
- 요청 PC: GPU PC 1
- 대상 파일: `base_apple_detector.py`
- 대상 함수: `BaseAppleDetector.__init__`, `simulation_state_callback`,
  `process_rgbd`, `publish_harvest_target` 및 신규 tracker 보조 함수
- 관련 계약: `/harvest/target`, `/harvest/perception_status`

## USD 멀티로봇 입력 매핑 추가

GPU PC 1의 저장된 USD가 다음 두 수확 입력을 제공하도록 변경되었다.

| `robot_id` | 카메라 Prim | 담당 USD 수확 영역 | 초기 관절 자세 (deg) |
|---|---|---|---|
| `robot_01` | `/World/base_rsd455_01` | `/World/Xform/tree` 및 `/World/Xform/apple_branch[_1/_2]` | `[0, 0, -90, 0, 90, 0]` |
| `robot_02` | `/World/base_rsd455_02` | `/World/Xform_03/tree` 및 `/World/Xform_03/apple_branch[_1/_2]` | `[0, 0, 90, 0, -90, 0]` |

개인 PC 1 인식 노드는 다음 수정을 요청한다.

1. 실행 parameter로 `robot_id`를 받아 담당 RGB-D/CameraInfo 입력을 선택한다.
2. `robot_01`은 `base_rsd455_01`, `robot_02`는 `base_rsd455_02` 카메라
   frame/TF를 사용한다. 영상 timestamp 기준의 `world` 변환 규칙은 유지한다.
3. 두 인식 프로세스를 분리 실행할 수 있도록 카메라별 입력 topic과 debug 출력
   구성을 parameter화한다. 최종 robot별 ROS topic/action namespace는 공동
   인터페이스 승인 전까지 `TBD`로 두며, 임의의 고정 이름을 계약으로 승격하지
   않는다.
4. 선택한 `robot_id`와 담당 tree 영역이 일치하지 않는 target은 발행하지 않고
   `perception_status`에 진단 상태를 기록한다. `HarvestTarget.msg`에
   `robot_id`/`tree_id` 필드를 추가하는 것은 공동 interface 승인 후 별도 작업으로
   진행한다.
5. reset 시 선택한 카메라의 입력 cache, track 및 target 발행 이력을 해당
   `robot_id` 범위에서 폐기한다.

이 요청은 개인 PC 1 소유의 `base_apple_detector.py`를 GPU PC 1이 직접 수정하지
않기 위한 변경 계약이다. 구현 후 개인 PC 1에서 ROS 2 Jazzy/Fast DDS와
`use_sim_time:=true` 조건으로 검증한다.

## 관찰된 문제

현재 검출기는 한 프레임에서 모든 유효 빨간 사과 contour를 계산하지만 카메라와
가장 가까운 후보 하나만 선택한다. 모든 후보가 실행 시 주입한 동일 `target_id`를
사용하므로 GPU PC 1은 두 번째 사과를 첫 번째 사과의 갱신으로 해석한다. 또한
`/harvest/target` QoS depth가 1이라 한 프레임에서 여러 target을 연속 발행하면
중간 메시지를 보존하기 어렵다.

## 요청 동작

1. `target_id` 단일 필수 parameter를 제거하고 기본 prefix `apple`을 사용한다.
2. reset 후 최초로 유효 후보 집합을 확보한 프레임에서 각 후보를 camera 좌표에서
   world 좌표로 변환한다.
3. 촬영 timestamp의 `world → base_link` TF로 로봇 base 원점을 구하고, 후보를
   로봇 base와의 world 3D 거리 오름차순으로 정렬해 `apple_001`,
   `apple_002`, ... 고정 ID를 부여한다. 거리가 같으면 world `(x, y, z)`
   오름차순으로 순서를 결정한다. 최초 ID 생성 시 `base_link` TF가 없으면
   XYZ 순서로 대체하지 않고 ID 초기화를 보류한다.
4. 이후 프레임에서는 마지막 world 위치에서 100mm 이내인 최근접 후보만 기존
   track에 연결한다. 한 후보를 두 track에 중복 할당하지 않는다.
5. 최초 ID 집합을 만든 뒤 같은 `reset_id`에서는 신규 ID를 추가하지 않는다.
   수확되어 컨베이어로 이동한 사과가 새 ID로 등록되는 것을 방지하기 위한
   규칙이다.
6. 매 RGB-D 처리 프레임에서 현재 관측·변환에 성공한 모든 track의
   `HarvestTarget`을 발행한다. 각 메시지는 해당 track ID와 동일한 촬영 timestamp,
   `reset_id`, `scene_version`, world position, camera source point 및 품질
   메타데이터를 사용한다.
7. `/harvest/target` publisher QoS를 `Reliable, Volatile, Keep Last 10`으로
   변경한다.
8. debug 영상의 각 후보에 tracker ID를 표시하고, 프레임별 발행 ID 목록을
   최대 1Hz로 로그에 남긴다.
9. `reset_id`가 변경되면 track, ID 카운터, RGB-D 캐시와 발행 이력을 모두
   폐기한다.

## 인터페이스 영향

- `HarvestTarget.msg` 필드 변경은 없다.
- GPU PC 1 coordinator는 `(reset_id, target_id)`를 lifecycle key로 사용한다.
- GPU PC 1은 실행 중 다른 ID의 target을 저장하며, 현재 실행 ID의 갱신은 실행
  Goal에 반영하지 않는다.
- 개인 PC 1과 GPU PC 1의 target QoS depth를 모두 10으로 맞춰야 한다.
- custom interface 재빌드는 필요 없지만 개인 PC 1 배포 코드 재빌드·재실행은
  필요하다.

## 실패·재시도 계약

- 접촉 전 첫 `APPROACH` 실패 target은 GPU PC 1이 후순위 대기열에 넣는다.
- 다른 일반 target을 모두 수확한 뒤 해당 target을 1회 재시도한다.
- 두 번째 실패는 최종 실패다.
- `GRASP` 이후 실패는 GPU PC 1이 다음 target을 실행하지 않고 안전 정지한다.
- 개인 PC 1은 완료·실패 순서를 결정하지 않고 안정적인 ID와 최신 좌표만
  계속 제공한다.

## 검증 요청

1. 최소 3개 contour 입력에서 로봇 base와 가까운 순서로 서로 다른
   `apple_001`~`apple_003`이 발행되는지 단위 테스트한다.
2. contour 열거 순서가 바뀌어도 100mm 이내 world 최근접 연결로 ID가 유지되는지
   확인한다.
3. 수확된 사과가 100mm 밖으로 이동하거나 화면에서 사라져도 새 ID가 생기지
   않는지 확인한다.
4. 동일 후보가 두 track에 배정되지 않는지 확인한다.
5. `reset_id` 변경 후 ID가 `apple_001`부터 새로 생성되는지 확인한다.
6. 세 target을 한 프레임에 연속 발행했을 때 GPU PC 1이 세 ID를 모두 수신하는지
   ROS 2 Jazzy/Fast DDS 통합 시험한다.
7. 개인 PC 1에서 `use_sim_time:=true`, `ROS_DOMAIN_ID=102` 및 world TF timestamp
   규약이 유지되는지 확인한다.
8. 최초 ID 생성 시 `world → base_link` TF를 구할 수 없으면 target을 발행하지
   않고 ID 초기화를 보류하는지 확인한다.
