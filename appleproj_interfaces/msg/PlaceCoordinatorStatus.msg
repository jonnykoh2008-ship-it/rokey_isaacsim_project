std_msgs/Header header

uint8 IDLE=0
uint8 RESERVED=1
uint8 PLACING=2
uint8 LANDING_CHECK=3
uint8 COMPLETED=4
uint8 ERROR=5

uint8 state

string lock_owner_robot_id
string reservation_id
string apple_id
string place_position_id
string[] waiting_robot_ids

uint64 reset_id
uint64 scene_version

float32 lock_duration_sec
bool landing_confirmed

string error_code
string message
