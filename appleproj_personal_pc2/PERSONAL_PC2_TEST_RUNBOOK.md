# 개인 PC2 로컬 테스트 실행 순서

## 1. 목적

개인 PC2에서 `appleproj_interfaces`와 `appleproj_personal_pc2`를 빌드하고,
단위 테스트 및 ROS 2 메시지 수신 기능이 정상적으로 작동하는지 확인한다.

이 문서는 개인 PC2에서 실행할 명령만 다룬다. 다른 PC의 소스나 설정은
변경하지 않는다.

## 2. 현재 테스트 가능 범위

현재 저장소에서 확인할 수 있는 기능은 다음과 같다.

- `appleproj_interfaces` 및 개인 PC2 패키지 빌드
- 모니터 상태, 결과 요약, 이벤트 이력 및 푸셔 선택 단위 테스트
- `quality_monitor` 노드 실행
- 개발용 품질 결과의 로컬 발행 및 수신
- 품질 등급과 상태 로그 표시
- 잘못된 품질 결과 ID 검출

현재 다음 기능은 공유 계약이 확정되지 않았거나 구현되지 않아 실제 송신 시험을 할 수 없다.

- `SortCommand` 생성 및 송신
- GPU PC1의 실제 푸셔 구동과 연동

현재 구현은 `/quality/results`를 구독한다. 단위 테스트의 푸셔 선택 성공은
실제 푸셔 명령이 송신된다는 뜻이 아니다. `/quality/classifications`와
`/sorting/pusher_command`는 현재 공유 인터페이스에 정의된 이름이 아니므로
시험 대상 토픽으로 사용하지 않는다.

## 3. 실행 파일 구분

직접 실행하는 항목:

- `launch/personal_pc2.launch.py`: `quality_monitor` 노드 실행
- `appleproj_personal_pc2/mock_quality_source.py`: 개발용 결과 발행
- `appleproj_personal_pc2/retry_inspection.py`: GPU PC 1에 재검사를 요청하는 일회성 CLI 클라이언트
- `test/test_*.py`: `colcon test`를 통해 실행

직접 실행하지 않는 라이브러리:

- `appleproj_personal_pc2/monitor_state.py`
- `appleproj_personal_pc2/pusher_selection.py`
- `appleproj_personal_pc2/result_summary.py`
- `appleproj_personal_pc2/event_history.py`

`retry_inspection.py`의 입력 검증과 서비스 미가용 처리는 개인 PC 2에서 확인한다.
승인, 거부 및 응답 timeout은 GPU PC 1의 `/quality/retry_inspection` 서비스가
실행되는 통합 환경에서 확인한다.

### 3.1 실행 전 승인 및 생성 산출물

- 환경·인터페이스 조회처럼 파일을 변경하지 않는 명령은 읽기 전용 확인으로 수행할 수 있다.
- `colcon build`와 `colcon test`는 작업공간의 `build/`, `install/`, `log/`에 파일을 생성하거나 기존 산출물을 갱신한다.
- 빌드나 테스트를 실행하기 전에 대상 패키지, 실행 명령 및 생성·갱신할 경로를 사용자에게 제시하고 명시적 승인을 받는다.
- 승인된 패키지와 산출물 범위를 넘어서는 빌드·테스트가 필요하면 추가 승인을 받는다.
- 이벤트 이력처럼 별도 결과 파일을 생성하거나 추가 기록할 때는 정확한 출력 경로와 생성·append 동작에 대한 승인을 별도로 받는다.
- 실행 후에는 생성·변경된 산출물과 수행 결과를 보고한다.

## 4. 터미널 1: ROS 2 환경 확인

새 터미널을 열고 다음을 실행한다.

```bash
cd /home/roh/cobot_ws/rokey_isaacsim_project
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

echo "ROS_DISTRO=$ROS_DISTRO"
echo "RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
echo "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
```

확인 기준:

- `ROS_DISTRO=jazzy`
- `RMW_IMPLEMENTATION=rmw_fastrtps_cpp`
- 다중 PC 연동 시 `ROS_DOMAIN_ID`는 모든 PC에서 동일해야 한다.
- 합의되지 않은 `ROS_DOMAIN_ID`를 영구 설정하지 않는다.

## 5. 터미널 1: 패키지 빌드

같은 터미널에서 실행한다.

```bash
colcon build \
  --symlink-install \
  --packages-select appleproj_interfaces appleproj_personal_pc2
```

빌드가 성공하면 환경을 적용한다.

```bash
source install/setup.bash

ros2 pkg prefix appleproj_interfaces
ros2 pkg prefix appleproj_personal_pc2
```

두 패키지의 설치 경로가 모두 출력되어야 한다.

## 6. 터미널 1: 인터페이스 확인

```bash
ros2 interface show appleproj_interfaces/msg/QualityResult
ros2 interface show appleproj_interfaces/msg/CheckpointEvent
ros2 interface show appleproj_interfaces/srv/RetryInspection
```

현재 설치 환경에 `SortCommand` 후보 인터페이스가 있는지는 참고 목적으로만 확인한다.

```bash
ros2 interface list | grep -i sort
```

출력이 없다면 컴퓨터나 ROS 2 설치 문제가 아니라 공유 `SortCommand` 계약이
아직 정의되지 않은 상태다. 출력이 있더라도
`docs/architecture/ros2_interfaces.md`에서 계약이 확정되기 전에는 해당
인터페이스를 개인 PC 2의 송신 계약으로 사용하지 않는다.

## 7. 터미널 1: 단위 테스트

```bash
colcon test \
  --packages-select appleproj_personal_pc2 \
  --event-handlers console_direct+

colcon test-result --verbose
```

통과 기준:

```text
0 tests failed
```

단위 테스트에서는 다음을 확인한다.

- checkpoint 및 deadline 상태 처리
- 품질 결과 ID 불일치 검출
- 중복 결과 처리
- `VALID` 결과의 등급별 의미 기반 푸셔 선택
- 비정상 결과의 푸셔 선택 제외
- 결과 요약
- 이벤트 이력

단위 테스트가 실패하면 ROS 2 통신 시험으로 넘어가지 않고 실패 내용을 먼저
확인한다.

## 8. 터미널 1: 개인 PC2 모니터 실행

```bash
ros2 launch appleproj_personal_pc2 personal_pc2.launch.py
```

예상 로그:

```text
Personal PC 2 monitor started with use_sim_time=true
deadline_checkpoint_id is TBD and unset
```

모니터가 실행된 터미널은 계속 켜 둔다.

## 9. 터미널 2: 노드 및 구독 확인

새 터미널을 열고 다음을 실행한다.

```bash
cd /home/roh/cobot_ws/rokey_isaacsim_project
source /opt/ros/jazzy/setup.bash
source /home/roh/cobot_ws/rokey_isaacsim_project/install/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

ros2 node list
ros2 node info /quality_monitor
```

현재 구현에서는 다음 구독이 표시되어야 한다.

```text
/quality/results
/conveyor/checkpoint_events
```

## 10. 터미널 2: 정상 HIGH 결과 발행

```bash
ros2 topic pub --once \
  /quality/results \
  appleproj_interfaces/msg/QualityResult \
  "{
    header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''},
    inspection_id: 'INS-001',
    apple_id: 'APPLE-001',
    grade: 1,
    confidence: 0.95,
    color_ratio: 0.82,
    diameter_mm: 75.0,
    damage_area_cm2: 0.5,
    frames_used: 4,
    frame_indices: [0, 1, 2, 3],
    result_timestamp: {sec: 0, nanosec: 0},
    status: 1
  }"
```

터미널 1에서 다음 내용이 출력되는지 확인한다.

```text
inspection=INS-001
apple=APPLE-001
grade=HIGH
status=VALID
```

## 11. 터미널 2: MEDIUM 결과 발행

```bash
ros2 topic pub --once \
  /quality/results \
  appleproj_interfaces/msg/QualityResult \
  "{
    header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''},
    inspection_id: 'INS-002',
    apple_id: 'APPLE-002',
    grade: 2,
    confidence: 0.88,
    color_ratio: 0.65,
    diameter_mm: 70.0,
    damage_area_cm2: 1.2,
    frames_used: 4,
    frame_indices: [0, 1, 2, 3],
    result_timestamp: {sec: 0, nanosec: 0},
    status: 1
  }"
```

예상 로그:

```text
grade=MEDIUM
status=VALID
```

## 12. 터미널 2: LOW 결과 발행

```bash
ros2 topic pub --once \
  /quality/results \
  appleproj_interfaces/msg/QualityResult \
  "{
    header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''},
    inspection_id: 'INS-003',
    apple_id: 'APPLE-003',
    grade: 3,
    confidence: 0.80,
    color_ratio: 0.42,
    diameter_mm: 64.0,
    damage_area_cm2: 2.8,
    frames_used: 4,
    frame_indices: [0, 1, 2, 3],
    result_timestamp: {sec: 0, nanosec: 0},
    status: 1
  }"
```

예상 로그:

```text
grade=LOW
status=VALID
```

## 13. 터미널 2: 재검사 필요 상태 발행

```bash
ros2 topic pub --once \
  /quality/results \
  appleproj_interfaces/msg/QualityResult \
  "{
    header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''},
    inspection_id: 'INS-004',
    apple_id: 'APPLE-004',
    grade: 1,
    confidence: 0.40,
    color_ratio: 0.50,
    diameter_mm: 68.0,
    damage_area_cm2: 1.0,
    frames_used: 2,
    frame_indices: [0, 1],
    result_timestamp: {sec: 0, nanosec: 0},
    status: 2
  }"
```

예상 로그:

```text
grade=HIGH
status=RECHECK
```

`RECHECK`는 푸셔 선택 대상에서 제외되어야 한다. 현재 이 동작은 단위
테스트에서만 확인할 수 있다.

이 단계는 재검사가 필요한 결과를 표시하는 시험이다. 실제 재검사 요청은
다음 단계에서 별도로 수행한다.

## 14. 터미널 2: 재검사 서비스 가용성 확인

GPU PC 1의 재검사 서비스 서버가 실행 중인 통합 환경에서 확인한다.

```bash
ros2 service list -t | grep /quality/retry_inspection
ros2 service type /quality/retry_inspection
```

예상 결과:

```text
/quality/retry_inspection [appleproj_interfaces/srv/RetryInspection]
appleproj_interfaces/srv/RetryInspection
```

서비스가 없으면 승인·거부·응답 timeout 시험으로 넘어가지 않는다. GPU PC 1이
서비스 서버와 실제 재검사 실행을 담당하므로 개인 PC 2에서 임시 서버를 구현하지
않는다. 이 경우 17단계의 서비스 미가용 처리를 확인한다.

## 15. 터미널 2: 실제 재검사 요청

13단계에서 `RECHECK`로 확인한 원래 검사 ID와 사과 ID를 사용한다.

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  INS-004 \
  APPLE-004 \
  "RECHECK status received" \
  --wait-timeout 5.0
```

GPU PC 1이 요청을 승인하면 다음 형식의 로그와 종료 코드 0을 확인한다.

```text
retry accepted: new_inspection_id=<비어 있지 않은 새 검사 ID> message=<서버 메시지>
```

이후 터미널 1의 `/quality/results` 모니터에서 다음을 확인한다.

- 새 결과의 `inspection_id`가 응답의 `new_inspection_id`와 같다.
- 새 결과의 `apple_id`가 원래 `APPLE-004`와 같다.
- 운영자가 원래 `INS-004`와 새 검사 ID의 관계를 추적할 수 있다.

GPU PC 1이 요청을 거부하면 다음 형식의 경고와 0이 아닌 종료 코드를 확인한다.

```text
retry rejected: message=<거부 사유>
```

승인 조건과 거부 조건은 GPU PC 1의 실제 서비스 정책을 따른다. 합의된 거부
조건이 아직 없으면 임의의 조건을 만들지 않고 해당 시험을 `TBD`로 기록한다.
자동 반복 요청과 동일 검사 중복 요청 정책도 `TBD`이므로 이 명령을 자동으로
재실행하지 않는다.

## 16. 터미널 2: 잘못된 재검사 요청 입력 검증

각 명령은 서비스 호출 전에 인수 오류와 0이 아닌 종료 코드로 거부되어야 한다.

빈 검사 ID:

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  "" APPLE-004 "RECHECK status received"
```

빈 사과 ID:

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  INS-004 "" "RECHECK status received"
```

빈 사유:

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  INS-004 APPLE-004 ""
```

0 이하 wait timeout:

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  INS-004 APPLE-004 "RECHECK status received" \
  --wait-timeout 0
```

예상 오류에는 각각 다음 문구가 포함되어야 한다.

```text
inspection_id must not be empty
apple_id must not be empty
reason must not be empty
--wait-timeout must be positive
```

## 17. 터미널 2: 재검사 서비스 오류 경로 확인

### 17.1 서비스 미가용

GPU PC 1 서비스가 실행되지 않은 로컬 환경에서 다음을 실행한다.

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  INS-004 APPLE-004 "service unavailable test" \
  --wait-timeout 1.0
```

예상 로그와 종료 상태:

```text
/quality/retry_inspection is unavailable
```

- 0이 아닌 종료 코드로 끝난다.
- 자동으로 재요청하지 않는다.

### 17.2 응답 timeout과 통신 예외

이 시험은 GPU PC 1 담당자와 조율하여 서비스는 발견되지만 응답이
`--wait-timeout`보다 늦게 도착하는 조건에서 수행한다. GPU PC 1의 시험 조건이나
지연 방법이 합의되지 않았으면 임의로 서버를 변경하지 않고 `TBD`로 기록한다.

```bash
ros2 run appleproj_personal_pc2 retry_inspection \
  INS-004 APPLE-004 "response timeout test" \
  --wait-timeout 1.0
```

응답 timeout의 예상 로그는 다음과 같다.

```text
RetryInspection response timed out
```

통신 또는 future 예외가 발생한 경우에는 다음 형식으로 구분되어야 한다.

```text
RetryInspection call failed: <예외 메시지>
```

두 경우 모두 0이 아닌 종료 코드로 끝나고 자동으로 재요청하지 않아야 한다.

## 18. 터미널 2: 잘못된 ID 검증

```bash
ros2 topic pub --once \
  /quality/results \
  appleproj_interfaces/msg/QualityResult \
  "{
    header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''},
    inspection_id: '',
    apple_id: 'APPLE-005',
    grade: 1,
    confidence: 0.90,
    color_ratio: 0.80,
    diameter_mm: 75.0,
    damage_area_cm2: 0.5,
    frames_used: 4,
    frame_indices: [0, 1, 2, 3],
    result_timestamp: {sec: 0, nanosec: 0},
    status: 1
  }"
```

터미널 1에서 `INVALID_RESULT` 오류가 표시되어야 한다.

## 19. `/clock` 수신 확인

Isaac Sim이 실행 중인 통합 환경에서는 개인 PC2 터미널에서 다음을 확인한다.

```bash
ros2 topic list | grep clock
ros2 topic echo /clock --once
ros2 topic hz /clock
```

확인 기준:

- `/clock`이 존재한다.
- 시간이 0에 고정되지 않고 증가한다.
- Isaac Sim Timeline이 일시정지하면 simulation time 진행도 멈춘다.

`/clock`이 없으면 simulation-time 기반 deadline 시험은 통과로 판정하지 않는다.

## 20. 선택 사항: 개발용 mock 파일 실행

이 시험은 `/clock`이 정상적으로 진행하고 실제 GPU 발행기가 실행 중이지 않을
때만 수행한다.

```bash
python3 -c \
'from appleproj_personal_pc2.mock_quality_source import main; main()' \
--inspection-id INS-MOCK-001 \
--apple-id APPLE-MOCK-001 \
--grade HIGH \
--status VALID
```

예상 결과:

- mock 터미널에 `development-only mock messages published` 출력
- 모니터 터미널에 `INS-MOCK-001`, `APPLE-MOCK-001`, `HIGH`, `VALID` 출력

mock과 실제 GPU 발행기를 동시에 실행하지 않는다.

## 21. 현재 계약과 미확정 푸셔 송신 확인

```bash
ros2 topic list -t
ros2 topic info /quality/results --verbose
```

현재 예상 결과:

- `/quality/results`에는 `/quality_monitor` 구독자가 있다.
- 개인 PC 2에서 GPU PC 1로 보내는 `SortCommand` 전송 인터페이스는 아직 없다.
- `SortCommand`의 topic·service·action 선택과 QoS는 `TBD`다.

`/quality/classifications`와 `/sorting/pusher_command`는 현재
`docs/architecture/ros2_interfaces.md`에 정의된 계약이 아니므로 존재 여부를
합격 기준으로 확인하지 않는다. 계약 확정 전에는 임의의 토픽명이나 메시지 타입을
만들어 송신 시험을 수행하지 않는다.

## 22. 종료

모니터가 실행 중인 터미널에서 `Ctrl+C`를 누른다.

남은 노드를 확인한다.

```bash
ros2 node list
```

개인 PC2 시험용 노드가 남아 있지 않아야 한다.

## 23. 최종 합격 기준

- 두 패키지의 빌드가 성공한다.
- `colcon test-result --verbose`에 실패한 테스트가 없다.
- `/quality_monitor` 노드가 정상 실행된다.
- `/quality/results`의 HIGH, MEDIUM, LOW 결과가 정확하게 표시된다.
- `RECHECK`와 잘못된 ID가 정상 결과와 구분된다.
- 빈 재검사 요청 인수와 0 이하 wait timeout이 서비스 호출 전에 거부된다.
- 재검사 서비스 미가용과 응답 timeout이 서로 다른 오류로 표시된다.
- GPU PC 1 연동 환경에서는 재검사 승인과 거부가 구분되고, 승인된
  `new_inspection_id`가 원래 `apple_id`와 연결된다.
- 노드가 메시지 처리 중 예외로 종료되지 않는다.
- `/clock`이 있는 환경에서는 simulation time을 정상적으로 수신한다.

GPU PC 1의 재검사 서버가 없는 로컬 시험에서는 입력 검증과 서비스 미가용 처리까지만
판정한다. 승인·거부·응답 timeout은 통합 시험 항목으로 남기며, 실행하지 않은 항목을
통과로 기록하지 않는다.

`SortCommand` 송신은 현재 구현의 합격 기준에 포함하지 않는다.
해당 기능을 시험하려면 전송 방식, 필드 및 QoS의 공유 계약을 먼저 확정하고,
승인된 공유 인터페이스와 개인 PC 2 송신 노드를 구현해야 한다.
