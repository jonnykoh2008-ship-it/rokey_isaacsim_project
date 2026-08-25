# 개인 PC 2 구현 변경 사항

## 범위

이 문서는 개인 PC 2가 담당하는 품질 결과 모니터링, 결과 표시 및 품질검사 재요청 구현의 기존 사항과 추가 수정 사항을 정리한다.

## 기존 구현 사항

### 품질 결과 및 체크포인트 모니터링

- `/quality/results`의 `QualityResult`를 수신해 검사 ID, 사과 ID, 등급, 상태, confidence 및 측정값을 표시한다.
- `/conveyor/checkpoint_events`의 `CheckpointEvent`를 수신해 사과별 체크포인트 진입·이탈을 추적한다.
- `inspection_id`와 `apple_id`의 연결을 관리하고 ID 변경을 `ID_MISMATCH`로 보고한다.
- 카메라 ROI 이탈을 나타내는 체크포인트가 설정된 경우 simulation time 기준 0.5초 deadline을 관리한다.
- deadline까지 결과가 없으면 `TIMEOUT`, deadline 이후 결과가 도착하면 `LATE_RESULT`로 보고한다.
- 모든 ROS 2 노드는 `use_sim_time=true`를 사용한다.

### 품질검사 재요청

- `/quality/retry_inspection`의 `RetryInspection` 서비스를 호출하는 일회성 CLI 클라이언트를 제공한다.
- 요청에 `inspection_id`, `apple_id`, `reason`을 전달한다.
- 서비스 대기 및 응답 제한시간은 wall time으로 관리한다.
- 응답의 승인 여부, 새 검사 ID 및 메시지를 로그로 출력한다.

### 테스트

- 체크포인트 이탈 후 deadline 시작과 일회성 timeout을 검증한다.
- deadline 이전 결과 수신 시 pending deadline 해제를 검증한다.
- timeout 이후 결과의 `LATE_RESULT` 처리를 검증한다.
- 동일한 `inspection_id`에 다른 `apple_id`가 연결되는 경우를 검증한다.
- 유효하지 않은 체크포인트 이벤트 거부를 검증한다.

## 이번 추가 수정 사항

### ID 불일치 시 상태 오염 방지

대상: `appleproj_personal_pc2/monitor_state.py`

- 이미 등록된 `inspection_id`가 다른 `apple_id`로 수신되면 `ID_MISMATCH`를 반환하고 즉시 처리를 중단하도록 변경했다.
- 불일치 결과가 다른 사과의 최신 검사 ID를 변경하거나 pending deadline을 제거하지 않도록 했다.
- 잘못 연결된 결과 때문에 정상 사과의 timeout 감시가 사라지는 문제를 방지한다.

### Deadline 경계 판정 보정

대상: `appleproj_personal_pc2/monitor_state.py`

- 결과 도착 시각이 deadline과 정확히 같은 경우도 `LATE_RESULT`로 판정하도록 비교 조건을 `>=`로 변경했다.
- "deadline까지 결과가 없으면 TIMEOUT"이라는 품질검사 시간 규칙과 경계 동작을 일치시켰다.

### 재검사 요청 입력 검증

대상: `appleproj_personal_pc2/retry_inspection.py`

- `inspection_id`, `apple_id`, `reason`이 빈 문자열 또는 공백만 포함하는 경우 요청 전에 CLI 오류로 거부한다.
- 유효하지 않은 식별자나 사유가 GPU PC 1의 재검사 서비스로 전달되는 것을 방지한다.

### 재검사 서비스 예외 처리

대상: `appleproj_personal_pc2/retry_inspection.py`

- 비동기 서비스 future가 예외로 완료된 경우 예외 메시지를 로그로 남기고 안전하게 종료하도록 처리했다.
- 예외가 발생한 future에서 응답을 직접 읽어 클라이언트가 비정상 종료되는 상황을 방지한다.

### 회귀 테스트 추가

대상: `test/test_monitor_state.py`

- deadline과 정확히 같은 시각에 도착한 결과가 `LATE_RESULT`인지 확인하는 테스트를 추가했다.
- ID 불일치 결과가 다른 사과의 pending deadline을 제거하지 않고 이후 `TIMEOUT`으로 유지되는지 확인하는 테스트를 추가했다.

### `AGENTS.md` 작업 규칙 반영

대상: `appleproj_personal_pc2/WORK_INSTRUCTIONS.md`

- 개인 PC 2 작업의 실행 PC와 파일 소유권을 수정 전에 확인하도록 작업 절차를 추가했다.
- 수정할 파일과 범위를 사전에 제시해 사용자의 명시적 승인을 받고, 승인 범위를 확대할 때는 추가 승인을 받도록 했다.
- 다른 PC 소유 소스는 직접 수정하지 않고 대상 파일·함수, 관찰된 문제, 제안 동작, 인터페이스 영향 및 검증 절차를 포함한 변경 검토 요청을 제출하도록 했다.
- `appleproj_interfaces/`, `docs/`, `README.md`, `AGENTS.md` 및 공통 빌드·네트워크 설정을 공유 파일로 명시하고, 정확한 파일·범위 승인과 영향받는 PC 보고 절차를 추가했다.
- 품질검사, 2차 푸셔, ROS 2·simulation time 및 다중 PC 네트워크 작업별 필수 문서 라우팅을 추가했다.
- 기능 문서와 단계 문서의 역할을 구분하고, 인터페이스·TF·시간·네트워크 규칙은 아키텍처 문서를 우선하도록 했다.
- 문서가 충돌하면 사용자에게 결정을 요청하고, 미확정 요구사항과 임시값은 승인 전까지 `TBD`로 유지하도록 했다.
- 작업지시서에 기존 지시 사항과 이번 변경 사항을 비교하는 표를 추가했다.

## 검증 상태

- 기존 코드 변경 내용과 수정 범위는 읽기 전용으로 확인했다.
- `WORK_INSTRUCTIONS.md`와 `CHANGELOG.md`의 문서 구조, 핵심 변경 항목 및 후행 공백을 확인했다.
- 이번 문서 개정에서는 소스 코드, ROS 2 인터페이스 및 런타임 설정을 변경하지 않았다.
- 문서 변경만 수행했으므로 테스트, 빌드, ROS 2 노드 및 launch 파일은 실행하지 않았다.
- `appleproj_personal_pc2/` 외부 파일은 수정하지 않았다.

## 미구현 및 TBD 사항

- 2차 개발의 푸셔 선택 결과를 GPU PC 1로 전달할 `SortCommand`의 토픽·서비스·액션 방식과 QoS가 아직 `TBD`다.
- 계약이 확정되기 전에는 임의의 ROS 2 인터페이스나 영구 값을 추가하지 않는다.
- 실제 푸셔 구동, trigger 검증 및 prismatic joint 제어는 GPU PC 1의 소유 범위다.
