# 품질검사 재요청 작업 흐름

## 목적

개인 PC 2가 GPU PC 1에 품질검사 재시도를 안전하게 요청하고 결과를 운영자에게 전달하는 절차를 정의한다.

## 서비스 계약

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

## 책임 경계 및 계약 변경

- 개인 PC 2는 재검사 요청 클라이언트와 운영자 표시를 실행·유지한다.
- GPU PC 1은 `/quality/retry_inspection` 서비스 서버와 실제 재검사 실행을 소유한다.
- GPU PC 1 소스의 변경이 필요하면 직접 수정하지 않고 해당 소유자에게 변경 검토를 요청한다.
- 변경 검토 요청에는 대상 파일과 함수, 관찰된 문제, 제안 동작, 인터페이스 영향 및 검증 절차를 포함한다.
- `RetryInspection` 필드나 서비스 이름을 변경하려면 `appleproj_interfaces/`와 `docs/architecture/ros2_interfaces.md`의 정확한 변경 범위에 대해 사용자의 승인을 받는다.
- 공유 계약 변경 후에는 GPU PC 1과 개인 PC 2를 영향받는 PC로 보고하고 양쪽 인터페이스 재빌드·통합 검증 절차를 합의한다.
- 소유권이나 계약이 모호하면 임의로 구현하지 않고 사용자에게 확인한다.

## 요청 전 검증

- `inspection_id`가 비어 있지 않아야 한다.
- `apple_id`가 비어 있지 않아야 한다.
- `reason`이 비어 있지 않아야 한다.
- wait timeout은 양수여야 한다.
- 운영자는 요청 대상이 최근 오류 결과와 일치하는지 확인한다.

## 처리 흐름

1. CLI 입력을 파싱하고 필수 값을 검증한다.
2. `/quality/retry_inspection` 서비스 가용성을 wall time으로 기다린다.
3. 비동기 요청을 한 번 전송한다.
4. 지정된 wall-time 제한까지 응답을 기다린다.
5. 승인, 거부, timeout 또는 예외를 구분해 표시한다.
6. 승인 시 `new_inspection_id`를 원래 검사와 연결해 기록한다.

서비스 가용성과 응답 대기는 네트워크·노드 생존 확인을 위한 wall time을 사용한다. 품질 결과 deadline과 공정 상태 판단에는 wall time을 사용하지 않고 `/clock` 기준 simulation time을 사용한다.

## 결과 분류

| 결과 | 의미 | 운영자 조치 |
|---|---|---|
| 승인 | GPU PC 1이 재검사를 수락 | 새 검사 ID 결과 대기 |
| 거부 | 현재 조건에서 재검사 불가 | 응답 메시지 확인 |
| 서비스 미가용 | GPU PC 1 서버 미발견 | 네트워크·노드 상태 확인 |
| 응답 timeout | 요청 후 응답 없음 | 중복 요청 전에 서버 상태 확인 |
| future 예외 | 통신 또는 클라이언트 오류 | 예외 메시지 기록 |

## 중복 요청 정책

현재 클라이언트는 일회성 요청만 제공한다. 자동 반복 요청, 최대 재시도 횟수 및 동일 inspection의 중복 방지 정책은 `TBD`다. 정책이 확정되기 전에는 운영자가 응답을 확인한 뒤 다음 요청을 결정한다.

## 테스트 후보

- 빈 inspection ID
- 빈 apple ID
- 빈 reason
- 0 이하 wait timeout
- 서비스 미가용
- 응답 timeout
- 승인 응답
- 거부 응답
- future 예외
- 승인인데 새 검사 ID가 비어 있는 비정상 응답

## 완료 기준

- 잘못된 입력은 서비스 호출 전에 차단된다.
- 모든 응답 경로가 명확한 로그와 종료 상태를 갖는다.
- 승인된 재검사의 새 ID를 원래 사과와 추적할 수 있다.
