# 2차 개발 푸셔 선택 설계

## 목적

개인 PC 2가 `QualityResult`를 바탕으로 의미 기반 푸셔 대상을 선택한다. 실제 푸셔 joint 구동과 trigger 검증은 GPU PC 1이 담당한다.

## 책임 경계

개인 PC 2:

- 품질 결과의 ID, 등급 및 상태 확인
- 선택 대상 여부 판단
- 중복·충돌 결과 차단
- 향후 확정된 `SortCommand` 생성 및 송신

GPU PC 1:

- 해당 사과와 trigger의 일치 확인
- 푸셔 원점 복귀 확인
- 중복 동작 방지
- prismatic joint 구동
- push, retract 및 home 완료 확인

## 공유 계약 및 변경 절차

- `SortCommand`의 필드, 전송 방식, QoS와 실제 `pusher_id`가 확정되기 전에는 임의의 ROS 2 인터페이스나 영구 값을 만들지 않는다.
- 공유 계약을 변경할 때는 `appleproj_interfaces/`, `docs/architecture/ros2_interfaces.md` 및 관련 기능·단계 문서의 정확한 파일과 범위에 대해 사용자의 명시적 승인을 받는다.
- 계약 변경은 개인 PC 2의 선택·송신 코드와 GPU PC 1의 명령 수신·푸셔 실행 코드에 영향을 주므로 두 PC를 모두 영향 대상으로 보고한다.
- GPU PC 1 소스 변경이 필요하면 개인 PC 2가 직접 수정하지 않고, 대상 파일과 함수, 관찰된 문제, 제안 동작, 인터페이스 영향 및 검증 절차를 포함한 변경 검토를 요청한다.
- `pusher_selection.py`를 `quality_monitor.py` 또는 ROS 송신 코드에 연결할 때도 대상 파일과 변경 범위에 대한 승인을 먼저 받고, 변경 후 검증 결과를 보고한다.
- 계약 확정 전에는 의미 기반 내부 선택 결과만 유지하며 물리 푸셔 동작 성공을 가정하지 않는다.

## 선택 규칙

| status | grade | 의미 기반 대상 |
|---|---|---|
| `VALID` | `HIGH` | `HIGH_GRADE` |
| `VALID` | `MEDIUM` | `MEDIUM_GRADE` |
| `VALID` | `LOW` | `LOW_GRADE` |
| `VALID` | 알 수 없음 | 선택 없음 |
| `VALID` 이외 | 모든 등급 | 선택 없음, 라인 끝 통과 |

현재 내부 대상 이름은 공유 `pusher_id`가 아니다. 실제 ID 값은 공유 계약 확정 후 변환한다.

## 선택 제외 상태

- `RECHECK`
- `UNCLASSIFIED`
- `TIMEOUT`
- `LATE_RESULT`
- `ID_MISMATCH`
- `INSUFFICIENT_VIEWS`
- 놓친 사과

## 중복 및 충돌

- 같은 inspection의 동일 결과가 반복되면 중복으로 표시하고 새 명령을 만들지 않는다.
- 같은 inspection의 apple, grade 또는 status가 달라지면 충돌로 처리한다.
- 충돌 결과는 어떤 푸셔와도 연결하지 않는다.

## 현재 구현

`pusher_selection.py`는 ROS에 의존하지 않는 다음 기능을 제공한다.

- `decide_pusher`: 한 결과의 의미 기반 선택
- `SelectionRegistry`: inspection별 최초 결정 보관
- 중복 결정 표시
- 충돌 결과 거부

이 모듈은 아직 `quality_monitor.py` 또는 ROS 송신 코드에 연결하지 않았다.

## TBD

- 최종 `SortCommand` 필드
- 전송 방식: topic, service 또는 action
- QoS
- 실제 `pusher_id` 명칭과 값
- 명령 유효기간
- trigger 조건과 목표 simulation time 표현
- GPU PC 1의 성공·실패 응답 계약
- jam 및 다중 사과 queue 복구

## 완료 기준

- `VALID` 결과만 선택 대상이 된다.
- 세 정상 등급이 서로 다른 의미 기반 대상으로 매핑된다.
- 비정상 상태와 알 수 없는 등급은 선택되지 않는다.
- 동일 inspection의 중복·충돌이 구분된다.
- 공유 계약 확정 후에도 선택 로직과 전송 로직이 분리된다.
