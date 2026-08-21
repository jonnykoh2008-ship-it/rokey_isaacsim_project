uint8 HIGH=1
uint8 MEDIUM=2
uint8 LOW=3

uint8 VALID=1
uint8 RECHECK=2
uint8 UNCLASSIFIED=3
uint8 TIMEOUT=4
uint8 LATE_RESULT=5
uint8 ID_MISMATCH=6
uint8 INSUFFICIENT_VIEWS=7

std_msgs/Header header
string inspection_id
string apple_id
uint8 grade
float32 confidence
float32 color_ratio
float32 diameter_mm
float32 damage_area_cm2
uint16 frames_used
uint16[] frame_indices
builtin_interfaces/Time result_timestamp
uint8 status
