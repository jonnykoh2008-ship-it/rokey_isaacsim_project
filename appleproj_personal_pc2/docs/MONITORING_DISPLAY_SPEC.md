# 모니터링 및 결과 표시 설계

## 목적

개인 PC 2가 품질 결과와 컨베이어 이벤트를 운영자에게 일관되게 표시하기 위한 기준을 정의한다.

## 입력

- `/quality/results`: GPU PC 2의 `QualityResult`
- `/conveyor/checkpoint_events`: GPU PC 1의 `CheckpointEvent`
- `/clock`: Isaac Sim simulation time

## 개별 결과 표시

각 품질 결과에서 다음 정보를 표시한다.

- 검사 ID와 사과 ID
- 등급과 상태
- confidence
- 착색률
- 직경
- 손상 면적
- 사용 프레임 수와 인덱스
- 수신 당시 simulation time

알 수 없는 등급이나 상태 값은 숨기지 않고 원시 숫자와 함께 표시한다.

## 요약 표시

`result_summary.py`는 다음 집계를 ROS와 독립적으로 관리한다.

- 전체 수신 메시지 수
- 고유 inspection 수
- 중복 메시지 수
- 등급별 결과 수
- 상태별 결과 수
- 사과별 최신 결과

같은 `inspection_id`와 같은 `apple_id`가 다시 수신되면 중복으로 집계한다. 같은 `inspection_id`가 다른 `apple_id`로 수신되면 요약 상태에 반영하지 않고 오류로 처리한다.

## 경고 분류

| 코드 | 의미 | 표시 수준 |
|---|---|---|
| `DUPLICATE_ENTER` | 동일 사과와 checkpoint의 중복 진입 | 경고 |
| `EXIT_WITHOUT_ENTER` | 진입 기록 없는 이탈 | 경고 |
| `RESULT_WITHOUT_CHECKPOINT` | checkpoint 이전 결과 | 경고 |
| `TIMEOUT` | deadline까지 결과 없음 | 오류 |
| `LATE_RESULT` | deadline과 같거나 이후 결과 도착 | 경고 |
| `ID_MISMATCH` | inspection과 apple 연결 불일치 | 오류 |
| `INVALID_RESULT` | 결과 필수 ID 누락 | 오류 |
| `INVALID_CHECKPOINT` | checkpoint 필수 ID 누락 | 오류 |
| `INVALID_CHECKPOINT_EVENT` | 정의되지 않은 이벤트 값 | 오류 |

## 시간 규칙

- 공정 deadline은 `/clock`을 사용한다.
- Timeline Pause 중 deadline도 정지한다.
- 결과 수신 wall time은 네트워크 분석용으로만 별도 기록할 수 있다.
- simulation time과 wall time을 서로 대체하지 않는다.

## 현재 통합 상태

- `quality_monitor.py`는 개별 결과와 상태 경고를 로그로 표시한다.
- `result_summary.py`는 독립 모듈로 생성됐으나 기존 노드에는 아직 연결하지 않았다.
- 화면 UI의 형태와 갱신 주기는 `TBD`다.
- 요약 모듈 연결은 개인 PC 2 소스 변경에 해당하므로, 실행 PC와 대상 파일·함수·변경 범위를 제시해 사용자의 명시적 승인을 받은 후 진행한다.
- `quality_monitor.py` 외의 파일까지 변경 범위가 확대되면 해당 파일과 범위에 대한 추가 승인을 받는다.
- 연결 후에는 변경한 파일과 단위·통합 검증 결과를 보고한다.

## 완료 기준

- 정상·오류 상태를 운영자가 구분할 수 있다.
- 중복 메시지가 정상 검사 수를 부풀리지 않는다.
- ID 불일치가 다른 사과의 요약을 오염시키지 않는다.
- 요약값을 복사본으로 제공해 외부 코드가 내부 상태를 변경하지 못한다.
