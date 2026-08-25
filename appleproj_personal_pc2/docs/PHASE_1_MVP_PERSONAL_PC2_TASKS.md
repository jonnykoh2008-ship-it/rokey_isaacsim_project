# 개인 PC 2 1차 개발(MVP) 작업 정리

## 1. 목적

개인 PC 2가 1차 개발 MVP에서 수행할 품질 결과 모니터링, 결과 표시, ID 연결 확인, 재검사 요청 지원 및 검증 범위를 정리한다.

이 문서는 실행 체크리스트다. 기능 동작은 `docs/features/quality_grading.md`와 `docs/features/conveyor.md`, 단계 범위는 `docs/phases/phase_1_mvp.md`, ROS 2·시간 계약은 아키텍처 문서를 기준으로 한다. 문서가 충돌하면 아키텍처 문서를 우선하고 충돌 내용을 사용자에게 보고한다.

## 2. MVP 전체 목표에서 개인 PC 2의 역할

1차 MVP는 사과 한 개의 ground-truth pose를 이용해 수확하고 컨베이어에 배치한 뒤, 품질 등급 산출과 `apple_id` 연결까지 확인하는 단계다.

개인 PC 2의 핵심 역할은 다음 흐름을 확인하는 것이다.

```text
GPU PC 2의 QualityResult 수신
  → inspection_id와 apple_id 검증
  → 등급·상태·측정값 표시
  → 컨베이어 checkpoint와 결과 연결 확인
  → 오류 상태 표시
  → 필요 시 GPU PC 1에 재검사 요청
```

## 3. 기준 환경

- 운영체제: Ubuntu 24.04
- ROS 2: Jazzy
- DDS: Fast DDS
- 시뮬레이터: NVIDIA Isaac Sim 5.1.0
- 모든 ROS 2 노드: `use_sim_time=true`
- 공정 시간과 deadline: Isaac Sim `/clock` 기준 simulation time
- 네트워크 서비스 가용성과 응답 대기: 공정 시간과 분리된 wall time

## 4. 작업 전 확인

- 실행 PC가 개인 PC 2인지 확인한다.
- 변경할 파일이 개인 PC 2의 실행·유지 범위에 속하는지 확인한다.
- 파일 생성·수정 전에는 대상 파일과 변경 범위에 대한 사용자의 명시적 승인을 받는다.
- 다른 PC 소스는 직접 수정하지 않는다.
- 공유 인터페이스나 공유 문서의 변경이 필요하면 정확한 파일과 범위를 승인받고 영향받는 PC를 보고한다.
- 미확정 요구사항과 임시값은 승인 전까지 `TBD`로 유지한다.

## 5. ROS 2 입출력

### 입력

| 이름 | 타입 | 송신 | 용도 |
|---|---|---|---|
| `/quality/results` | `appleproj_interfaces/msg/QualityResult` | GPU PC 2 | 품질 결과 수신과 표시 |
| `/conveyor/checkpoint_events` | `appleproj_interfaces/msg/CheckpointEvent` | GPU PC 1 | 컨베이어 진입·이탈 및 ID 연결 확인 |
| `/clock` | `rosgraph_msgs/msg/Clock` | Isaac Sim | 공정 deadline과 timestamp 기준 |

### 출력

| 이름 | 타입 | 수신 | 용도 |
|---|---|---|---|
| `/quality/retry_inspection` | `appleproj_interfaces/srv/RetryInspection` | GPU PC 1 | 운영상 필요한 품질검사 재시도 요청 |

재검사 요청은 MVP 전체 성공 기준의 핵심 단계가 아니라 운영 지원 기능이다.

## 6. 필수 작업

### 6.1 품질 결과 수신과 표시

- `/quality/results` 수신 여부를 확인한다.
- 다음 필드를 로그 또는 운영자 화면에 표시한다.
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
- 알 수 없는 등급이나 상태 값은 숨기지 않고 원시 값과 함께 표시한다.

### 6.2 컨베이어 checkpoint 감시

- `/conveyor/checkpoint_events`를 수신한다.
- 사과별 `ENTER`와 `EXIT` 순서를 확인한다.
- 중복 `ENTER`와 `ENTER` 없는 `EXIT`를 경고로 표시한다.
- 컨베이어 2 tracker의 `apple_id`와 컨베이어 3 checkpoint의 사과 ID 연결을 확인한다.

### 6.3 ID 무결성 확인

- `apple_id`와 `inspection_id`는 한 처리 주기 동안 변경하지 않는다.
- 동일한 `inspection_id`가 다른 `apple_id`와 연결되면 `ID_MISMATCH`로 처리한다.
- ID 불일치 결과가 정상 사과의 최신 검사 정보나 pending deadline을 변경하지 않도록 한다.
- 빈 `inspection_id`, `apple_id` 또는 `checkpoint_id`가 포함된 입력은 거부한다.

### 6.4 결과 상태 구분

| 상태 | 표시 및 처리 |
|---|---|
| `VALID` | 정상 품질 결과로 표시 |
| `RECHECK` | 재검사 필요 상태로 표시 |
| `UNCLASSIFIED` | 미분류 상태로 표시 |
| `TIMEOUT` | 결과 deadline 초과로 표시 |
| `LATE_RESULT` | 지연 결과로 표시 |
| `ID_MISMATCH` | ID 연결 오류로 표시 |
| `INSUFFICIENT_VIEWS` | 관측 프레임 부족으로 표시 |

MVP에서는 상태와 등급을 푸셔 또는 상자 분류에 연결하지 않는다.

### 6.5 시간과 deadline

- 품질 결과 deadline은 카메라 ROI 이탈 후 simulation time 0.5초다.
- deadline 전에 결과가 도착하면 정상 처리한다.
- deadline까지 결과가 없으면 `TIMEOUT`으로 처리한다.
- deadline과 같거나 이후에 도착한 결과는 `LATE_RESULT`로 기록한다.
- 같은 pending 결과의 timeout을 반복해서 보고하지 않는다.
- Timeline Pause 중에는 simulation time 기반 deadline도 정지한다.
- deadline 시작에 사용할 구체적인 checkpoint ID는 `TBD`다.
- checkpoint ID가 확정되지 않은 상태에서는 로컬 deadline 감지를 비활성화하고 임의의 값을 사용하지 않는다.

### 6.6 재검사 요청 지원

- `inspection_id`, `apple_id`, `reason`이 비어 있지 않은지 확인한다.
- GPU PC 1의 `/quality/retry_inspection` 서비스를 호출한다.
- 승인, 거부, 서비스 미가용, 응답 timeout 및 future 예외를 구분해 표시한다.
- 승인 시 `new_inspection_id`를 원래 `apple_id`와 연결해 표시한다.
- 자동 재요청 횟수와 중복 방지 정책은 확정 전까지 `TBD`로 유지한다.

## 7. 검증 항목

### 단위 검증

- checkpoint 이탈 후 deadline이 한 번만 시작된다.
- deadline 이전 결과가 pending 상태를 해제한다.
- deadline과 같거나 이후에 도착한 결과가 `LATE_RESULT`가 된다.
- timeout은 동일한 pending 결과에 대해 한 번만 발생한다.
- 동일 inspection의 ID 변경이 `ID_MISMATCH`가 된다.
- ID 불일치 결과가 다른 사과의 deadline을 제거하지 않는다.
- 잘못된 checkpoint event와 빈 ID 입력이 거부된다.
- 빈 재검사 요청 인수가 서비스 호출 전에 거부된다.

### 통합 검증

- 개인 PC 2가 GPU PC 2의 `/quality/results`를 수신한다.
- 개인 PC 2가 GPU PC 1의 `/conveyor/checkpoint_events`를 수신한다.
- 정상 결과에 `inspection_id`, `apple_id`, 등급, 상태 및 측정값이 표시된다.
- 컨베이어 3에서 `apple_id`와 품질 결과가 올바르게 연결된다.
- 모든 header timestamp와 공정 deadline이 `/clock` 기준으로 처리된다.
- Timeline Pause 중 simulation time 기반 deadline이 멈춘다.
- 운영 지원 시험에서는 `/quality/retry_inspection`의 성공·거부·미가용·timeout을 구분한다.

## 8. 개인 PC 2 완료 조건

- 정상 품질 결과를 ID와 측정값을 포함해 표시한다.
- 정의된 모든 예외 상태를 구분해 표시한다.
- ID 불일치가 다른 사과의 내부 상태를 오염시키지 않는다.
- 컨베이어 checkpoint와 품질 결과의 사과 ID 연결을 확인한다.
- simulation time 기반 deadline 동작을 검증한다.
- 개인 PC 2 노드가 메시지 처리 중 예외로 종료되지 않는다.
- 개인 PC 2가 다른 PC 소유의 추론, 시뮬레이션 또는 로봇 제어 기능을 중복 구현하지 않는다.

MVP 전체 완료 판정은 reset을 포함한 동일 초기조건 2회 실행 중 최소 1회 이상 수확부터 컨베이어 3 품질 결과 연결까지 전체 과정이 성공해야 한다.

## 9. 1차 MVP 제외 범위

- 실제 사과 검출 비전 모델
- 여러 사과의 동시 또는 queue 처리
- 기본 world `+Z` 이외의 접근 방향 탐색
- 컨베이어 4
- 가상 또는 실제 푸셔
- 등급별 상자 분류
- `SortCommand` 생성 및 송신
- 실제 `pusher_id` 결정
- GPU PC 1의 물리 푸셔·컨베이어 제어
- GPU PC 2의 품질 추론 정책 변경

`SortCommand`와 푸셔 선택·구동은 2차 개발 범위이므로 MVP 합격 기준에 포함하지 않는다.

## 10. 미확정 사항

- deadline 시작에 사용할 구체적인 checkpoint ID
- 상태·결과 토픽의 정확한 QoS
- 네트워크 장애 감지용 wall-time timeout
- 자동 재검사 및 중복 요청 정책

미확정 항목은 사용자 승인이나 공유 계약 확정 전까지 `TBD`로 유지한다.

## 11. 기준 문서

- `AGENTS.md`
- `docs/phases/phase_1_mvp.md`
- `docs/features/quality_grading.md`
- `docs/features/conveyor.md`
- `docs/architecture/ros2_interfaces.md`
- `docs/architecture/tf_frames.md`
- `docs/architecture/hardware_network.md`
- `appleproj_personal_pc2/WORK_INSTRUCTIONS.md`
