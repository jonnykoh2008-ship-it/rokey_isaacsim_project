# 개인 PC 2 작업 지시서

## 1. 목적

개인 PC 2는 품질검사 결과와 컨베이어 상태를 모니터링하고, 운영자에게 결과를 표시하며, 필요한 경우 품질검사 재시도를 요청한다. 2차 개발에서는 정상 품질 결과에 따라 사용할 푸셔를 선택한다.

이 문서는 개인 PC 2의 구현 범위, ROS 2 입출력, 처리 규칙, 다른 PC와의 책임 경계 및 완료 기준을 정의한다.

## 2. 기준 환경

- 운영체제: Ubuntu 24.04
- ROS 2: Jazzy
- DDS: Fast DDS
- 시뮬레이터: NVIDIA Isaac Sim 5.1.0
- 모든 ROS 2 노드: `use_sim_time=true`
- 공정 시간과 deadline: Isaac Sim의 `/clock` 기준 simulation time
- 네트워크 노드 생존 확인이 필요한 경우: simulation time과 분리된 wall time 사용

## 3. 개인 PC 2 담당 범위

### 3.1 모니터링

- 품질검사 결과 수신 상태를 감시한다.
- 컨베이어 체크포인트 진입·이탈 이벤트를 감시한다.
- `inspection_id`와 `apple_id` 연결의 일관성을 확인한다.
- 품질 결과 deadline과 지연 결과를 감시한다.
- 오류와 예외 상태를 운영자가 확인할 수 있도록 표시한다.

### 3.2 결과 표시

다음 품질 결과 정보를 로그 또는 향후 사용자 화면에 표시한다.

- `inspection_id`
- `apple_id`
- `grade`
- `status`
- `confidence`
- `color_ratio`
- `diameter_mm`
- `damage_area_cm2`
- `frames_used`
- `frame_indices`

### 3.3 재검사 요청

- 운영자 요청 또는 재검사 필요 판단에 따라 GPU PC 1의 `/quality/retry_inspection` 서비스를 호출한다.
- 요청에는 `inspection_id`, `apple_id`, `reason`을 포함한다.
- 빈 식별자나 빈 사유를 전송하지 않는다.
- 서비스 승인 여부와 새 검사 ID를 운영자에게 표시한다.

### 3.4 2차 개발 푸셔 선택

- `QualityResult`의 등급과 상태를 확인해 사용할 푸셔를 선택한다.
- `VALID` 상태의 정상 품질 결과만 푸셔 선택 대상으로 사용한다.
- `TIMEOUT`, `LATE_RESULT`, `RECHECK`, `UNCLASSIFIED`, `ID_MISMATCH`, `INSUFFICIENT_VIEWS` 및 놓친 사과는 푸셔와 연결하지 않고 라인 끝으로 통과시킨다.
- 푸셔 선택 결과는 향후 `SortCommand` 계약에 따라 GPU PC 1로 전달한다.
- `SortCommand`의 전송 방식과 QoS가 확정되기 전에는 임의의 ROS 2 인터페이스를 구현하지 않는다.

## 4. 다른 PC와의 책임 경계

| PC | 담당 기능 | 개인 PC 2와의 관계 |
|---|---|---|
| GPU PC 1 | Isaac Sim, 센서, 컨베이어 이벤트, 재검사 실행, 실제 푸셔 구동 | 개인 PC 2에 체크포인트를 제공하고 재검사·푸셔 명령을 실행한다. |
| GPU PC 2 | 품질 이미지 추론 및 사과 단위 결과 통합 | 개인 PC 2에 `QualityResult`를 제공한다. |
| 개인 PC 1 | 수확 조율, waypoint 계획 및 로봇 Goal 순서 관리 | 개인 PC 2의 품질 모니터링 소스를 실행하거나 유지하지 않는다. |
| 개인 PC 2 | 모니터링, 결과 표시, 재검사 요청 및 푸셔 선택 | 실제 추론·물리 동작을 직접 실행하지 않는다. |

개인 PC 2는 GPU PC 1의 Isaac Sim 소스, GPU PC 2의 추론 소스 또는 개인 PC 1의 수확 계획 소스를 수정하지 않는다.

작업 범위와 파일 소유권은 버그를 발견한 PC가 아니라 해당 기능을 실행하고 유지하는 PC를 기준으로 판단한다. 개인 PC 2에서 작업할 때는 모니터링, 결과 표시, 재검사 요청 및 2차 푸셔 선택 소스만 개인 PC 2 소유 범위로 취급한다. 수정 전에는 실행 PC가 개인 PC 2인지 확인하고, 대상 파일이 개인 PC 2 소유인지 확인한다. 소유권이 없거나 모호하면 수정하지 않고 사용자에게 확인한다.

다른 PC 소유 소스의 변경이 필요하면 직접 수정하지 않고 해당 PC 소유자에게 변경 검토를 요청한다. 변경 검토 요청에는 다음 내용을 포함한다.

- 대상 파일과 함수
- 관찰된 문제
- 제안하는 동작
- ROS 2 인터페이스 및 다른 PC에 미치는 영향
- 수정 후 검증 절차

`appleproj_interfaces/`, `docs/`, `README.md`, `AGENTS.md` 및 여러 PC가 함께 사용하는 빌드·네트워크 설정은 공유 계약 또는 공유 문서다. 공유 파일은 대상 파일과 변경 범위에 대한 사용자의 명시적 승인을 받은 경우에만 수정하고, 수정 후 영향받는 모든 PC를 보고한다.

## 5. ROS 2 입력

### 5.1 품질 결과

```text
토픽: /quality/results
타입: appleproj_interfaces/msg/QualityResult
송신: GPU PC 2
수신: 개인 PC 2
```

상태·결과 메시지는 신뢰성을 우선한다. 정확한 QoS는 저장소 계약상 `TBD`이므로 임의로 영구 확정하지 않는다.

### 5.2 컨베이어 체크포인트

```text
토픽: /conveyor/checkpoint_events
타입: appleproj_interfaces/msg/CheckpointEvent
송신: GPU PC 1
수신: 개인 PC 2
```

필수 확인 필드는 `header`, `apple_id`, `checkpoint_id`, `event`다. `event`는 `ENTER` 또는 `EXIT`만 허용한다.

### 5.3 시뮬레이션 시간

```text
토픽: /clock
타입: rosgraph_msgs/msg/Clock
송신: Isaac Sim
```

Timeline이 일시정지하면 simulation time 기반 deadline도 함께 정지해야 한다.

## 6. ROS 2 출력

### 6.1 품질검사 재요청

```text
서비스: /quality/retry_inspection
타입: appleproj_interfaces/srv/RetryInspection
서버: GPU PC 1
클라이언트: 개인 PC 2
```

Request:

- `inspection_id`
- `apple_id`
- `reason`

Response:

- `accepted`
- `new_inspection_id`
- `message`

`accepted=false`인 경우 `new_inspection_id`는 빈 문자열이어야 한다.

### 6.2 푸셔 선택 결과

2차 개발에서 개인 PC 2가 GPU PC 1로 `SortCommand`를 전달한다. 현재 확정된 후보 필드는 다음과 같다.

- `apple_id`
- `grade`
- `pusher_id`
- trigger 조건 또는 목표 simulation time

토픽·서비스·액션 선택과 QoS는 `TBD`다. 계약 확정 전에는 임의 구현하지 않는다.

## 7. 처리 규칙

### 7.1 ID 연결

- `apple_id`와 `inspection_id`는 한 처리 주기 동안 변경하지 않는다.
- 동일한 `inspection_id`가 다른 `apple_id`와 연결되면 `ID_MISMATCH`로 처리한다.
- ID 불일치 결과는 정상 사과의 최신 검사 정보나 pending deadline을 변경해서는 안 된다.
- 컨베이어 2 tracker의 `apple_id`와 컨베이어 3 checkpoint의 rigid body prim이 일치하지 않으면 `ID_MISMATCH`로 처리한다.

### 7.2 결과 deadline

- 품질 결과 deadline은 카메라 ROI 이탈 후 simulation time 0.5초다.
- deadline 전에 결과가 도착하면 정상 처리한다.
- deadline까지 결과가 없으면 `TIMEOUT`으로 처리한다.
- deadline과 같거나 이후에 도착한 결과는 `LATE_RESULT`로 기록한다.
- 같은 deadline에 대해 timeout을 반복해서 보고하지 않는다.
- deadline 시작에 사용할 구체적인 `checkpoint_id`는 현재 `TBD`이므로 설정하지 않은 상태에서는 로컬 deadline 감지를 비활성화한다.

### 7.3 잘못된 입력

- 빈 `inspection_id` 또는 `apple_id`가 포함된 품질 결과는 거부한다.
- 빈 `apple_id` 또는 `checkpoint_id`가 포함된 체크포인트는 거부한다.
- `ENTER`, `EXIT` 이외의 체크포인트 이벤트는 거부한다.
- 재검사 요청의 ID 또는 사유가 비어 있으면 서비스 호출 전에 거부한다.

### 7.4 결과 상태와 푸셔

| 결과 상태 | 모니터링 | 푸셔 선택 |
|---|---|---|
| `VALID` | 정상 결과로 표시 | 2차 개발에서 등급에 따라 선택 |
| `RECHECK` | 재검사 필요로 표시 | 선택하지 않음 |
| `UNCLASSIFIED` | 미분류로 표시 | 선택하지 않음 |
| `TIMEOUT` | deadline 초과로 표시 | 선택하지 않음 |
| `LATE_RESULT` | 지연 결과로 표시 | 선택하지 않음 |
| `ID_MISMATCH` | ID 오류로 표시 | 선택하지 않음 |
| `INSUFFICIENT_VIEWS` | 관측 부족으로 표시 | 선택하지 않음 |

## 8. 현재 소스 구성

| 파일 | 역할 |
|---|---|
| `appleproj_personal_pc2/quality_monitor.py` | 품질 결과와 체크포인트를 구독하고 상태를 표시하는 ROS 2 노드 |
| `appleproj_personal_pc2/monitor_state.py` | ROS에 의존하지 않는 ID 및 deadline 상태 관리 |
| `appleproj_personal_pc2/retry_inspection.py` | 품질검사 재요청 CLI 클라이언트 |
| `launch/personal_pc2.launch.py` | 개인 PC 2 모니터 노드 실행 설정 |
| `test/test_monitor_state.py` | 모니터 상태 단위 테스트 |
| `CHANGELOG.md` | 기존 구현과 추가 수정 내역 |

## 9. 단계별 작업 지시

### 작업 전 공통 절차

1. 분석·검토·계획·읽기 요청은 파일 수정 승인으로 간주하지 않는다.
2. 수정 전에 실행 PC가 개인 PC 2임을 명시하고, 변경할 파일과 변경 범위를 사용자에게 제시해 해당 범위의 명시적 승인을 받는다.
3. 승인된 파일과 범위를 넘어서는 변경이 필요하면 작업을 중단하고 추가 승인을 받는다.
4. 관련 문서가 충돌하면 임의로 하나를 선택하지 않고 충돌 내용을 보고해 결정을 요청한다.
5. 미확정 요구사항은 `TBD`로 유지한다. 임시값도 사용자의 명시적 승인 없이 확정하거나 구현하지 않는다.
6. 수정 후에는 변경한 파일과 수행한 검증을 보고한다.

### 단계 1: 인터페이스 확인

1. 작업 범위에 따라 다음 필수 문서를 모두 읽는다.
   - 품질검사·등급 및 모니터링: `docs/features/quality_grading.md`, `docs/features/conveyor.md`, `docs/architecture/ros2_interfaces.md`
   - 2차 푸셔 선택: `docs/phases/phase_2_pusher.md`, `docs/features/conveyor.md`, `docs/features/quality_grading.md`, `docs/architecture/ros2_interfaces.md`
   - ROS 2 토픽·메시지·QoS 또는 simulation time: `docs/architecture/ros2_interfaces.md`, `docs/architecture/tf_frames.md`
   - 다중 PC·네트워크 설정: `docs/architecture/hardware_network.md`, `docs/architecture/ros2_interfaces.md`
2. 기능 문서는 기능 동작을, 단계 문서는 구현 시점과 범위를 정의한다. 인터페이스·TF·시간·네트워크 내용은 아키텍처 문서를 우선한다.
3. `appleproj_interfaces`가 빌드되어 있는지 확인한다.
4. `QualityResult`, `CheckpointEvent`, `RetryInspection` 필드가 `docs/architecture/ros2_interfaces.md`와 일치하는지 확인한다.
5. 인터페이스가 다르면 개인 PC 2 소스에 임시 우회 코드를 넣지 말고 공유 계약 변경을 먼저 협의한다.

### 단계 2: 모니터 시작 전 확인

1. ROS 2 Jazzy와 Fast DDS 환경을 확인한다.
2. 모든 참여 PC의 ROS domain 및 네트워크 설정이 일치하는지 확인한다.
3. Isaac Sim이 `/clock`을 발행하는지 확인한다.
4. 개인 PC 2 노드의 `use_sim_time`이 `true`인지 확인한다.
5. deadline용 checkpoint ID가 확정되지 않았다면 빈 값으로 유지한다.

### 단계 3: 결과 모니터링 확인

1. `/quality/results` 수신 여부를 확인한다.
2. 등급과 상태 문자열이 메시지 상수에 맞게 표시되는지 확인한다.
3. `inspection_id`, `apple_id`, 사용 프레임 및 측정값이 함께 표시되는지 확인한다.
4. 알 수 없는 등급·상태 값이 수신되면 오류를 숨기지 않고 원시 값을 표시한다.

### 단계 4: 체크포인트 및 deadline 확인

1. 사과별 `ENTER`와 `EXIT` 순서를 확인한다.
2. 중복 `ENTER`와 `ENTER` 없는 `EXIT`를 경고로 표시한다.
3. 확정된 ROI 이탈 checkpoint에서만 deadline을 시작한다.
4. 정상 결과, timeout 및 지연 결과 시나리오를 각각 확인한다.
5. Timeline Pause 중 deadline이 진행되지 않는지 확인한다.

### 단계 5: 재검사 요청 확인

1. 유효한 `inspection_id`, `apple_id`, `reason`으로 서비스를 요청한다.
2. 서비스 미가용, 응답 timeout, future 예외 및 요청 거부를 각각 확인한다.
3. 승인 시 `new_inspection_id`를 표시한다.
4. 재요청 결과가 원래 사과 ID와 올바르게 연결되는지 확인한다.

### 단계 6: 2차 푸셔 선택

1. `SortCommand` 공유 계약이 확정됐는지 먼저 확인한다.
2. `VALID` 결과만 등급별 푸셔 선택 대상으로 사용한다.
3. 푸셔 명령에는 원래 `apple_id`를 유지한다.
4. GPU PC 1이 해당 푸셔 trigger와 원점 복귀 상태를 최종 검증하도록 한다.
5. 개인 PC 2는 물리 푸셔 동작 성공을 임의로 가정하지 않고 GPU PC 1의 결과를 기다린다.

## 10. 검증 기준

### 단위 검증

- checkpoint 이탈 후 deadline이 한 번만 시작된다.
- deadline 이전 결과가 pending 상태를 해제한다.
- deadline과 같거나 이후인 결과가 `LATE_RESULT`가 된다.
- timeout은 같은 pending 결과에 대해 한 번만 발생한다.
- 동일 inspection의 ID 변경이 `ID_MISMATCH`가 된다.
- ID 불일치 결과가 다른 사과의 deadline을 제거하지 않는다.
- 잘못된 checkpoint event가 거부된다.
- 빈 재검사 요청 인수가 거부된다.

### 통합 검증

- 개인 PC 2가 GPU PC 2의 `/quality/results`를 수신한다.
- 개인 PC 2가 GPU PC 1의 `/conveyor/checkpoint_events`를 수신한다.
- 개인 PC 2가 GPU PC 1의 `/quality/retry_inspection` 서비스를 호출한다.
- 모든 header timestamp와 공정 deadline이 `/clock` 기준으로 해석된다.
- Timeline Pause 중 simulation time 기반 deadline이 멈춘다.

## 11. 완료 조건

- 정상 품질 결과가 ID와 측정값을 포함해 표시된다.
- 모든 정의된 예외 상태가 구분되어 표시된다.
- ID 불일치가 내부 상태를 오염시키지 않는다.
- 재검사 요청의 성공, 거부, 미가용 및 timeout이 구분된다.
- simulation time 기반 deadline 동작이 검증된다.
- 2차 개발에서는 확정된 공유 계약을 사용해 푸셔 선택 결과가 GPU PC 1에 전달된다.
- 개인 PC 2가 다른 PC 소유의 추론, 시뮬레이션 또는 로봇 제어 기능을 중복 구현하지 않는다.

## 12. 미확정 사항

다음 항목은 승인 또는 공유 계약 확정 전까지 `TBD`로 유지한다.

- deadline 시작에 사용할 구체적인 checkpoint ID
- 상태·결과 토픽의 정확한 QoS
- 네트워크 장애 감지용 wall-time timeout
- `SortCommand`의 최종 필드
- `SortCommand`의 토픽·서비스·액션 선택
- `SortCommand`의 QoS
- 푸셔 실패, jam 및 ID mismatch 복구 정책
- 다중 사과 queue 처리
- `RECHECK` 사과 보관 방식

## 13. 기존 지시 사항 대비 변경 사항

이번 개정은 개인 PC 2의 기술 기능 범위를 변경하지 않고, 최신 `AGENTS.md`의 작업 통제 규칙을 작업 지시서에 반영한다.

| 구분 | 기존 사항 | 변경된 사항 |
|---|---|---|
| 활성 작업 범위 | 개인 PC 2의 담당 기능과 타 PC 소스 수정 금지만 명시 | 작업 요청과 실제 실행 PC를 기준으로 활성 범위를 정하고, 수정 전 실행 PC와 파일 소유권을 확인하도록 추가 |
| 수정 승인 | 파일별 승인 절차가 작업 지시서에 없음 | 수정 전 대상 파일·범위를 제시해 명시적 승인을 받고, 범위 확대 시 추가 승인을 받도록 추가 |
| 타 PC 변경 | 다른 PC 소스를 수정하지 않는다고만 명시 | 대상 파일·함수, 문제, 제안 동작, 인터페이스 영향 및 검증 절차를 포함한 변경 검토 요청을 해당 PC 소유자에게 제출하도록 구체화 |
| 공유 파일 | 공유 계약 변경을 협의한다고만 명시 | 인터페이스·공통 문서·빌드·네트워크 설정은 정확한 파일과 범위의 승인을 받고, 영향받는 모든 PC를 보고하도록 추가 |
| 필수 문서 | 인터페이스 확인 단계에서 `ros2_interfaces.md` 중심으로 확인 | 품질검사, 푸셔, ROS 2·시간, 네트워크 작업별 필수 문서와 문서 우선순위를 명시 |
| 문서 충돌과 TBD | 개별 `TBD` 항목과 임의 인터페이스 구현 금지만 명시 | 문서 충돌을 보고해 결정을 요청하고, 임시값도 승인 없이 확정하거나 구현하지 않도록 추가 |
| 변경 후 보고 | 별도 절차 없음 | 변경 파일과 수행한 검증을 사용자에게 보고하도록 추가 |
