# 모니터링 이벤트 이력 저장 설계

## 목적

통합시험에서 품질 결과, checkpoint 및 오류 발생 순서를 사후 분석할 수 있도록 개인 PC 2가 선택적으로 이벤트 이력을 남긴다.

## 형식

- 기본 후보 형식: JSON Lines
- 한 줄에 이벤트 한 건을 저장한다.
- UTF-8을 사용한다.
- 각 레코드는 독립적으로 파싱 가능해야 한다.

## 공통 필드

- `event_type`
- `simulation_time_ns`
- `received_wall_time_ns`
- `payload`

`simulation_time_ns`는 `/clock` 기준 공정 분석에 사용한다. `received_wall_time_ns`는 네트워크 지연과 노드 생존 분석에만 사용한다.

## 이벤트 종류 후보

- `QUALITY_RESULT`
- `CHECKPOINT_EVENT`
- `MONITOR_NOTICE`
- `RETRY_REQUEST`
- `RETRY_RESPONSE`
- `PUSHER_SELECTION`

이 명칭은 개인 PC 2 내부 기록용이며 공유 ROS 인터페이스가 아니다.

## 파일 정책

- 사용자가 명시한 경로에만 기록한다.
- 최초 생성이나 기존 파일 append 전에 정확한 경로와 수행할 파일 동작을 사용자에게 제시해 명시적 승인을 받는다.
- 승인된 경로를 변경하거나 생성·append 범위를 확대할 때는 추가 승인을 받는다.
- 기본 저장 경로는 아직 정하지 않는다.
- 기존 파일이 있으면 승인된 경우에만 JSON Lines 레코드를 추가하며 기존 내용을 truncate하거나 덮어쓰지 않는다.
- 상위 디렉터리를 자동 생성하지 않는다. 디렉터리 생성이 필요하면 대상 경로에 대한 별도 승인을 받는다.
- 테스트는 사용자가 승인한 임시 경로로 제한하고 운영 이력 파일을 사용하지 않는다.
- 기록 후에는 생성·변경된 파일과 append 검증 결과를 보고한다.
- 파일 회전, 최대 크기, 보관 기간 및 개인정보 정책은 `TBD`다.

## 오류 처리

- 빈 이벤트 종류는 거부한다.
- 음수 simulation time은 거부한다.
- JSON으로 직렬화할 수 없는 payload는 호출자 오류로 처리한다.
- 저장 실패가 발생했을 때 모니터 노드를 중단할지 경고만 남길지는 `TBD`다.

## 현재 구현

`event_history.py`의 `JsonlEventHistory`는 경로를 주입받아 단일 레코드를 append한다. 아직 `quality_monitor.py`나 재검사 클라이언트에는 연결하지 않았다.

## 완료 기준

- 한 이벤트가 한 JSON 레코드로 저장된다.
- simulation time과 wall time이 구분된다.
- 한글 payload가 UTF-8로 보존된다.
- 테스트용 임시 경로에서 기존 데이터 손상 없이 append된다.
