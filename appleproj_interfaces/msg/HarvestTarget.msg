# RGB-D 촬영 시각. Isaac Sim /clock 기준.
# frame_id는 항상 "world".
std_msgs/Header header

# 동일 reset_id 내 수확 대상 식별자.
# 품질검사용 apple_id와 lifecycle이 다르므로 target_id 사용.
string target_id

# 개인 PC 1이 마지막으로 확인한 SimulationState 세대.
uint64 reset_id
uint64 scene_version

# world 좌표계의 사과 중심.
# orientation은 GPU PC 1에서 계산.
geometry_msgs/Point position

# world 변환 전 카메라 좌표의 검출점.
# stamp는 header.stamp와 동일.
# frame_id는 원본 카메라 frame.
geometry_msgs/PointStamped source_point

# 범위 0.0~1.0.
float32 confidence

# 검출 영역 내 유효 depth 픽셀 비율. 범위 0.0~1.0.
float32 valid_depth_ratio

# 영상 timestamp와 사용한 TF timestamp의 절대 차이(초).
float32 tf_time_error_sec
