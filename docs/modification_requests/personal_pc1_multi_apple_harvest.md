# 개인 PC 1 다중 사과 검출·ID 발행 수정 요청

## 요청 정보

- 실행·소유 PC: 개인 PC 1
- 요청 PC: GPU PC 1
- 대상 파일: `base_apple_detector.py`
- 대상 함수: `BaseAppleDetector.__init__`, `simulation_state_callback`,
  `process_rgbd`, `publish_harvest_target` 및 신규 tracker 보조 함수
- 관련 계약: `/harvest/target`, `/harvest/perception_status`

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
3. 후보를 world `(x, y, z)` 오름차순으로 정렬해 `apple_001`, `apple_002`, ...
   고정 ID를 부여한다.
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

1. 최소 3개 contour 입력에서 서로 다른 `apple_001`~`apple_003`이 발행되는지
   단위 테스트한다.
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
