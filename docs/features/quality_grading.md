# 품질 분류

## 범위

컨베이어 2 상단 D455 카메라 한 대로 사과 영상을 수집하고 상·중·하 등급을 산출한다. 수확용 사과 위치 인식과는 별도 기능이다.

## 검사 흐름

1. RGB 영상과 bounding box 검출을 상시 수행한다.
2. tracker가 `apple_id`를 유지한다.
3. ROI 진입 시 `inspection_id`를 생성하고 후보 프레임을 수집한다.
4. 후보 프레임 중 대표 프레임을 선택한다.
5. GPU PC 2가 프레임별 품질을 추론한다.
6. 프레임 결과를 사과 단위로 통합한다.
7. ROI 이탈 시 `QualityResult`를 확정한다.
8. ID가 유실·변경되거나 관측이 부족하면 `RECHECK`로 처리한다.

후보 12장 중 대표 4~6장을 사용하는 안을 우선 기록하며 최종 수량은 TBD다.

## 등급 규칙

### 상 (`HIGH`)

다음을 모두 만족해야 한다.

- 착색률 80% 이상
- 적도부 최대 직경 75mm 이상
- 손상 면적 1.0cm² 이하
- 부패나 심각한 형상 이상 없음

### 하 (`LOW`)

다음 상품성 상실 조건 중 하나라도 만족하면 적용한다.

- 착색률 60% 미만
- 적도부 최대 직경 60mm 미만
- 손상 면적 2.5cm² 초과
- 부패, 큰 멍 또는 심각한 형상 이상

### 중 (`MEDIUM`)

- 하에 해당하지 않으며 상의 모든 조건을 만족하지 않는 판매 가능한 사과

예: 착색률 90%, 직경 80mm, 손상 1.5cm²인 사과는 `MEDIUM`이다.

## 측정 정의

- 크기: 적도부 최대 직경
- MVP 손상 면적: 대표 프레임 중 가장 크게 관측된 손상 면적
- 확장: 다중 프레임 mask를 사과 표면 좌표계에 투영한 합집합 면적
- 실제 cm²를 depth로 산출할지 mask 비율로 근사할지는 TBD다.
- 착색률, 윤택 및 심각한 이상에 대한 데이터 annotation 규칙은 TBD다.

## 통신

```text
GPU PC 1
후보 프레임 수집 및 대표 프레임 선택
  → inspection_id + apple_id + frame_index + compressed image

GPU PC 2
이미지별 품질 추론 및 사과 단위 통합
  → QualityResult

개인 PC 2
등급별 푸셔 선택
  → GPU PC 1의 가상 푸셔 검증 또는 2차 실제 푸셔 작동
```

## 참고

- EU 공식 규격: <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R2429-20251004>
- 내부 참고: `TalkFile_apple_harvesting_quality_grading_design.md` (현재 저장소 존재 여부 확인 필요)

## 미확정 사항

- 품질 모델 구조와 최종 출력
- 후보 및 대표 프레임 수
- 대표 프레임 선택 알고리즘
- 컨베이어 카메라 depth 사용 여부
- 실제 손상 면적 계산 방식
- 프레임별 결과 통합 규칙
- inference deadline과 지연 결과 처리
- `RECHECK` 재검사 또는 라인 끝 처리 규칙
- 등급별 목표 정확도와 confidence threshold

