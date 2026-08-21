# ROS 2 인터페이스

이 문서는 노드 간 데이터 계약의 기준이다. 실제 토픽 이름과 custom message 패키지는 구현 승인 후 확정한다.

## 공통 규칙

- 모든 header timestamp는 `/clock` 기준이다.
- 모든 노드는 `use_sim_time:=true`를 사용한다.
- `apple_id`와 `inspection_id`는 한 처리 주기 동안 변경하지 않는다.
- 센서 스트림에는 Sensor Data QoS를 기본 후보로 사용한다.
- 상태·결과 메시지는 신뢰성 우선 QoS를 사용한다. 정확한 QoS는 TBD다.

## MVP 사과 목표

```text
메시지: geometry_msgs/msg/PoseStamped
frame_id: world
의미: 사과 중심과 접근 orientation
```

다중 사과 단계의 ID 포함 메시지 구조는 TBD다.

## InspectionFrame

GPU PC 1에서 GPU PC 2로 전달한다.

필수 후보 필드:

- `inspection_id`
- `apple_id`
- `frame_index`
- `sim_timestamp`
- compressed RGB image
- 선택적인 depth 및 `CameraInfo`

정확한 custom message 정의와 토픽 이름은 TBD다.

## QualityResult

GPU PC 2에서 개인 PC 2로 전달한다.

필수 후보 필드:

- `inspection_id`
- `apple_id`
- `grade`: `HIGH`, `MEDIUM`, `LOW`
- `confidence`
- `color_ratio`
- `diameter_mm`
- `damage_area_cm2`
- `frames_used`
- `frame_indices`
- `result_timestamp`
- `status`: `VALID`, `RECHECK`, `UNCLASSIFIED`, `TIMEOUT`, `LATE_RESULT`, `ID_MISMATCH`, `INSUFFICIENT_VIEWS`

정확한 모델 출력과 custom message 정의는 TBD다.

카메라 ROI 이탈 후 simulation time 0.5초를 결과 deadline으로 사용한다. deadline까지 결과가 없으면 `TIMEOUT`, 이후 도착한 결과는 `LATE_RESULT`로 기록한다. 컨베이어 2의 tracker ID와 컨베이어 3 trigger의 rigid body prim이 일치하지 않으면 `ID_MISMATCH`로 처리한다.

## SortCommand

개인 PC 2에서 GPU PC 1로 전달한다. MVP에서는 사용하지 않으며, 2차 개발의 컨베이어 4 실제 푸셔 제어부터 사용한다.

필수 후보 필드:

- `apple_id`
- `grade`
- `pusher_id`
- trigger 조건 또는 목표 simulation time

토픽·서비스·액션 선택과 QoS는 TBD다.

## TriggerEvent

컨베이어 진입·이탈 검증에 사용한다.

- `apple_id`
- `trigger_id`
- `ENTER` 또는 `EXIT`
- simulation timestamp
