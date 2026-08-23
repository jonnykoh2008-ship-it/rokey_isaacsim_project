# 수확용 인식

## 목적

수확 대상 사과의 중심 pose와 접근에 필요한 장애물 정보를 수확 기능에 전달한다. 컨베이어 품질검사는 이 문서의 범위가 아니다.

## MVP

- 비전 모델을 사용하지 않는다.
- Isaac Sim ground-truth에서 사과 중심과 orientation을 얻는다.
- `geometry_msgs/msg/PoseStamped`로 전달한다.
- orientation 축은 월드 좌표계와 동일하게 시작한다.
- 굵은 가지의 ground-truth collider 또는 proxy를 계획 장애물로 사용한다.

## 실무/확장 흐름

```text
D455 RGB + Depth
  → YOLOv8/OpenCV 사과 검출
  → depth projection
  → 3D 중심 및 접근 방향 계산
  → world/robot_base 좌표 변환
  → 수확 계획에 전달
```

## 장애물 인식

- 굵은 가지: 로봇 전체 링크의 회피 대상
- 작은 가지: 그리퍼와 손목의 회피 대상
- 잎: 시각적 가림과 confidence 판단에는 사용하지만 planning obstacle에서는
  제외
- MVP에서는 ground-truth proxy를 사용한다.
- 실무 비전 단계에서는 굵은 가지 segmentation 또는 depth 기반 obstacle
  추출과 작은 가지 segmentation을 수행한다. 잎 segmentation은 occlusion 및
  confidence 판단에만 사용한다.
- RGB-D로 3D obstacle point cloud를 만들고 `world` 또는 `robot_base`로
  변환한 뒤 planning proxy로 단순화한다.
- 각 사과의 접근 방향 주변 free-space를 계산하고, 안전거리를 만족하지 않는
  후보는 수확 대상으로 발행하지 않는다.
- confidence가 낮거나 free-space가 부족하면 수확을 중단하거나 다른 접근 방향을 탐색한다.

작은 가지의 물리 collision 사용 여부는 perception 결과를 planning obstacle에
포함할지와 독립적으로 결정한다. 잎은 PhysX와 planning obstacle 양쪽에서
제외한다. MVP의 몸통·가지 obstacle은 USD visual mesh에서 생성한 ground-truth
proxy를 사용하고, D455 obstacle point cloud 전환 시에도 동일한 안전거리와
실패 규약을 유지한다.

## 다중 사과

- 사과별 `PoseStamped`와 ID를 연결한다.
- ID 메시지 규격과 tracker 연동은 TBD다.
