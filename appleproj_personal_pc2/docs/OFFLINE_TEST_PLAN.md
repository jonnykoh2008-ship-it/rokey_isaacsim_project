# 개인 PC 2 오프라인 시험 계획

## 목적

GPU PC 1과 GPU PC 2가 없는 상황에서도 개인 PC 2의 수신, 표시 및 상태 처리 준비를 확인한다.

## 원칙

- 개발 전용 mock 발행기는 실제 GPU 발행기와 동시에 사용하지 않는다.
- mock 결과는 기능 확인용이며 품질 모델 정확도 평가에 사용하지 않는다.
- `/clock`을 사용하는 시험은 Isaac Sim 또는 별도 승인된 clock source가 있을 때만 수행한다.
- 구체적인 ROI checkpoint ID가 확정되지 않았다면 임의 값을 운영 설정으로 저장하지 않는다.

## 시험 도구

`mock_quality_source.py`는 기존 공유 인터페이스를 사용해 다음을 한 번 발행할 수 있다.

- `QualityResult`
- 선택적인 `CheckpointEvent`

이 도구는 패키지 실행 엔트리로 아직 등록하지 않았으며 개발용 모듈로만 존재한다.

## 정적 검토 시나리오

1. 모든 노드가 `use_sim_time=true`를 사용하는지 확인한다.
2. 토픽과 서비스 이름이 공유 계약과 일치하는지 확인한다.
3. 메시지 상수가 현재 `appleproj_interfaces`와 일치하는지 확인한다.
4. `SortCommand`가 임의 구현되지 않았는지 확인한다.

## 단위 시나리오

### 정상 결과

- 새로운 inspection과 apple 조합
- `VALID`와 `HIGH`, `MEDIUM`, `LOW`
- 요약 집계 1 증가
- 의미 기반 푸셔 대상 선택

### 중복 결과

- 동일 inspection, apple, grade, status 반복
- 고유 검사 수 유지
- 중복 수 증가
- 두 번째 푸셔 명령 생성 금지

### ID 불일치

- 동일 inspection에 다른 apple 입력
- `ID_MISMATCH` 또는 충돌 오류
- 다른 사과의 deadline과 요약 보존

### 비정상 상태

- `RECHECK`
- `UNCLASSIFIED`
- `TIMEOUT`
- `LATE_RESULT`
- `ID_MISMATCH`
- `INSUFFICIENT_VIEWS`

모든 경우 푸셔 선택이 없어야 한다.

### 체크포인트 순서

- 정상 `ENTER → EXIT`
- 중복 `ENTER`
- `ENTER` 없는 `EXIT`
- 알 수 없는 event 값
- 여러 사과의 checkpoint 교차

### Deadline

- deadline 직전 결과
- deadline과 같은 시각의 결과
- deadline 이후 결과
- 결과 없는 timeout
- Timeline Pause 중 deadline 정지

## ROS 연동 시나리오

실행 승인을 받은 뒤 다음을 확인한다.

1. 개인 PC 2 모니터만 시작한다.
2. 실제 GPU 발행기가 실행 중이 아닌지 확인한다.
3. mock 결과 한 건을 발행한다.
4. 모니터 로그의 ID, 등급, 상태 및 측정값을 확인한다.
5. 선택적으로 checkpoint를 발행해 순서 경고를 확인한다.
6. 시험 후 mock 노드를 종료하고 실제 환경과 혼동되는 프로세스가 없는지 확인한다.

## 기록할 결과

- 시험 시각
- 사용한 Git revision
- ROS domain
- scenario와 입력값
- 예상 결과
- 실제 결과
- 통과 여부
- 발견된 문제와 담당 PC

## 완료 기준

- 모든 ROS 독립 단위 시나리오가 통과한다.
- mock과 실제 발행기의 동시 실행 방지 절차가 확인된다.
- simulation time이 없는 환경에서는 deadline 시험을 통과로 오판하지 않는다.
- 다른 PC 소스 변경 없이 개인 PC 2의 준비 상태를 설명할 수 있다.
