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
- 작은 가지와 잎: 그리퍼와 손목의 회피 대상
- MVP에서는 ground-truth proxy를 사용한다.
- 2차부터 RGB-D segmentation 또는 depth 기반 obstacle 추출을 검토한다.
- confidence가 낮거나 free-space가 부족하면 수확을 중단하거나 다른 접근 방향을 탐색한다.

## 다중 사과

- 사과별 `PoseStamped`와 ID를 연결한다.
- ID 메시지 규격과 tracker 연동은 TBD다.

