# 개인 PC 2 팀 회의 안건

## 회의 목표

개인 PC 2가 모니터링, 재검사 및 2차 푸셔 선택을 실제 시스템과 연결하기 전에 필요한 공유 계약과 운용 정책을 확정한다.

## 참석 역할

- GPU PC 1 담당자
- GPU PC 2 담당자
- 개인 PC 1 담당자
- 개인 PC 2 담당자

## 최우선 결정 사항

### 1. Deadline 시작 이벤트

- 카메라 ROI 이탈을 어떤 메시지로 전달할 것인가?
- 기존 `CheckpointEvent`를 사용한다면 정확한 `checkpoint_id`는 무엇인가?
- 해당 이벤트의 송신 주체는 GPU PC 1이 맞는가?
- reset 또는 Timeline 재시작 시 pending deadline을 어떻게 정리할 것인가?

결정 기록:

- checkpoint ID: `TBD`
- reset 처리: `TBD`

### 2. 품질 결과 QoS

- `/quality/results`의 reliability, durability 및 history depth는 무엇인가?
- `/conveyor/checkpoint_events`와 동일 QoS를 사용할 것인가?
- 늦게 접속한 모니터가 마지막 결과를 받아야 하는가?

결정 기록:

- QualityResult QoS: `TBD`
- CheckpointEvent QoS: `TBD`

### 3. 재검사 승인 정책

- GPU PC 1은 어떤 조건에서 요청을 승인 또는 거부하는가?
- 같은 inspection의 중복 요청은 어느 PC가 차단하는가?
- 최대 재검사 횟수는 필요한가?
- 승인 후 새 inspection과 원래 apple의 연결은 누가 유지하는가?

결정 기록:

- 승인 조건: `TBD`
- 중복 방지 책임: `TBD`
- 최대 횟수: `TBD`

### 4. SortCommand 계약

- topic, service 또는 action 중 무엇을 사용할 것인가?
- 필수 필드는 무엇인가?
- 실제 `pusher_id` 값과 명칭은 무엇인가?
- 명령 timestamp와 유효기간은 어떻게 표현하는가?
- GPU PC 1의 수신 확인과 실행 결과가 필요한가?

결정 기록:

- 전송 방식: `TBD`
- 필드: `TBD`
- pusher ID: `TBD`
- QoS: `TBD`

## 통합 운용 결정 사항

### 네트워크 장애

- wall-time heartbeat가 필요한가?
- 장애 판정 timeout은 얼마인가?
- GPU PC 2 결과 수신 단절과 GPU PC 1 단절을 어떻게 구분하는가?

### ID 복구

- 일시 누락 후 같은 `apple_id` 복구를 언제 허용하는가?
- ID switch와 tracker 재획득을 어떻게 구분하는가?
- 여러 사과가 겹칠 때 어떤 상태로 통과시키는가?

### 푸셔 실패

- jam, home 미복귀 및 trigger 미검출을 어떤 상태로 보고하는가?
- 실패 사과는 라인 끝 통과, 정지 또는 수동 회수 중 무엇을 적용하는가?
- 다음 사과의 명령을 언제 허용하는가?

### 결과 및 로그 보관

- 개인 PC 2가 JSONL 또는 CSV 이력을 저장해도 되는가?
- 저장 경로와 보관 기간은 무엇인가?
- 모든 PC의 로그 시각을 어떻게 맞춰 비교하는가?

## 개인 PC 2가 공유할 준비물

- 현재 모니터 로그 예시
- 상태 및 deadline 단위 테스트 목록
- 재검사 성공·실패 흐름
- 의미 기반 푸셔 선택 표
- mock 시험 시나리오
- 미확정 사항 목록

## PC별 확인 요청

### GPU PC 1에 확인

- checkpoint ID와 발생 시점
- 재검사 서비스의 실제 승인 조건
- 향후 SortCommand 수신 방식
- 푸셔 trigger 및 home 상태 제공 방식

### GPU PC 2에 확인

- QualityResult 발행 시점
- status별 grade 필드 사용 규칙
- 같은 inspection의 결과 재발행 가능성
- 결과 timestamp와 header timestamp의 의미 차이

### 개인 PC 1에 확인

- 수확과 품질검사 사이의 apple ID 전달 방식
- 수확 실패 또는 놓친 사과를 개인 PC 2가 알 필요가 있는지
- 전체 시스템 reset 시 개인 PC 2에 필요한 상태 정보

## 회의 종료 조건

- 각 `TBD` 항목의 결정 또는 담당자와 결정 기한이 기록된다.
- 공유 인터페이스 변경이 필요하면 영향받는 네 PC가 확인한다.
- 파일별 구현 담당자가 정해진다.
- 다음 통합시험의 입력, 기대 결과 및 성공 기준이 정해진다.
- 회의 결정 전 임시 값과 최종 계약을 명확히 구분한다.
