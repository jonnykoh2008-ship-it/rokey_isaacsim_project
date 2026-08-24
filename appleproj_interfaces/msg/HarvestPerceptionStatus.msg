uint8 OK=0
uint8 NO_DETECTION=1
uint8 DEPTH_INVALID=2
uint8 TF_UNAVAILABLE=3
uint8 STALE_FRAME=4
uint8 LOW_CONFIDENCE=5
uint8 RESET_MISMATCH=6
uint8 SIMULATION_NOT_READY=7
uint8 INPUT_NOT_SYNCHRONIZED=8
uint8 INTERNAL_ERROR=255

# 검사 대상 RGB-D 프레임의 촬영 시각과 카메라 frame.
std_msgs/Header header

uint8 status

# target 생성 전 실패한 경우 빈 문자열.
string target_id

uint64 reset_id
uint64 scene_version

# 계산할 수 없는 항목은 NaN.
float32 confidence
float32 valid_depth_ratio
float32 tf_time_error_sec

# 사람 확인용 설명. 로직 분기에 사용하지 않음.
string message
