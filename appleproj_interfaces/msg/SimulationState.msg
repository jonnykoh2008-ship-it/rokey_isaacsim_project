uint8 STOPPED=0
uint8 INITIALIZING=1
uint8 READY=2
uint8 PLAYING=3
uint8 PAUSED=4

std_msgs/Header header
uint8 state
uint64 reset_id
uint64 scene_version
string message
