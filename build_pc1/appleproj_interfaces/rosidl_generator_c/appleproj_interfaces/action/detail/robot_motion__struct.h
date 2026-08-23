// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:action/RobotMotion.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/action/robot_motion.h"


#ifndef APPLEPROJ_INTERFACES__ACTION__DETAIL__ROBOT_MOTION__STRUCT_H_
#define APPLEPROJ_INTERFACES__ACTION__DETAIL__ROBOT_MOTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'APPROACH'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__APPROACH = 1
};

/// Constant 'GRASP'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__GRASP = 2
};

/// Constant 'TWIST'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__TWIST = 3
};

/// Constant 'PULL'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__PULL = 4
};

/// Constant 'TRANSPORT'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__TRANSPORT = 5
};

/// Constant 'PLACE'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__PLACE = 6
};

/// Constant 'RETRACT'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__RETRACT = 7
};

/// Constant 'RELEASE'.
enum
{
  appleproj_interfaces__action__RobotMotion_Goal__RELEASE = 8
};

// Include directives for member types
// Member 'target_pose'
// Member 'waypoints'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_Goal
{
  uint8_t motion_type;
  geometry_msgs__msg__PoseStamped target_pose;
  uint64_t reset_id;
  uint64_t scene_version;
  geometry_msgs__msg__PoseStamped__Sequence waypoints;
} appleproj_interfaces__action__RobotMotion_Goal;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_Goal.
typedef struct appleproj_interfaces__action__RobotMotion_Goal__Sequence
{
  appleproj_interfaces__action__RobotMotion_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'error_code'
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_Result
{
  bool success;
  rosidl_runtime_c__String error_code;
  rosidl_runtime_c__String message;
} appleproj_interfaces__action__RobotMotion_Result;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_Result.
typedef struct appleproj_interfaces__action__RobotMotion_Result__Sequence
{
  appleproj_interfaces__action__RobotMotion_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'current_state'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_Feedback
{
  rosidl_runtime_c__String current_state;
  float progress;
} appleproj_interfaces__action__RobotMotion_Feedback;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_Feedback.
typedef struct appleproj_interfaces__action__RobotMotion_Feedback__Sequence
{
  appleproj_interfaces__action__RobotMotion_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "appleproj_interfaces/action/detail/robot_motion__struct.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  appleproj_interfaces__action__RobotMotion_Goal goal;
} appleproj_interfaces__action__RobotMotion_SendGoal_Request;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_SendGoal_Request.
typedef struct appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence
{
  appleproj_interfaces__action__RobotMotion_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} appleproj_interfaces__action__RobotMotion_SendGoal_Response;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_SendGoal_Response.
typedef struct appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence
{
  appleproj_interfaces__action__RobotMotion_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  appleproj_interfaces__action__RobotMotion_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  appleproj_interfaces__action__RobotMotion_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence request;
  appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence response;
} appleproj_interfaces__action__RobotMotion_SendGoal_Event;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_SendGoal_Event.
typedef struct appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence
{
  appleproj_interfaces__action__RobotMotion_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} appleproj_interfaces__action__RobotMotion_GetResult_Request;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_GetResult_Request.
typedef struct appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence
{
  appleproj_interfaces__action__RobotMotion_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_GetResult_Response
{
  int8_t status;
  appleproj_interfaces__action__RobotMotion_Result result;
} appleproj_interfaces__action__RobotMotion_GetResult_Response;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_GetResult_Response.
typedef struct appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence
{
  appleproj_interfaces__action__RobotMotion_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  appleproj_interfaces__action__RobotMotion_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  appleproj_interfaces__action__RobotMotion_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence request;
  appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence response;
} appleproj_interfaces__action__RobotMotion_GetResult_Event;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_GetResult_Event.
typedef struct appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence
{
  appleproj_interfaces__action__RobotMotion_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"

/// Struct defined in action/RobotMotion in the package appleproj_interfaces.
typedef struct appleproj_interfaces__action__RobotMotion_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  appleproj_interfaces__action__RobotMotion_Feedback feedback;
} appleproj_interfaces__action__RobotMotion_FeedbackMessage;

// Struct for a sequence of appleproj_interfaces__action__RobotMotion_FeedbackMessage.
typedef struct appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence
{
  appleproj_interfaces__action__RobotMotion_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__ACTION__DETAIL__ROBOT_MOTION__STRUCT_H_
