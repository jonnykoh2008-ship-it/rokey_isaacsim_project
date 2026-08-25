std_msgs/Header header

uint8 WAITING=0
uint8 ARMED=1
uint8 APPLE_CONFIRMED=2
uint8 EXTENDING=3
uint8 PUSH_CONFIRMED=4
uint8 RETRACTING=5
uint8 HOME_CONFIRMED=6
uint8 COMPLETED=7
uint8 FAILED=8
uint8 CANCELLED=9

string command_id
string apple_id
string inspection_id
uint8 grade
uint8 pusher_id
string trigger_checkpoint_id
uint8 state
float32 progress
string error_code
string message
