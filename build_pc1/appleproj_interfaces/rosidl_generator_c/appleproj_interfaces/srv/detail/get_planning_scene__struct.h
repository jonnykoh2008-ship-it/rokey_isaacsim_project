// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:srv/GetPlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/get_planning_scene.h"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__STRUCT_H_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetPlanningScene in the package appleproj_interfaces.
typedef struct appleproj_interfaces__srv__GetPlanningScene_Request
{
  uint8_t structure_needs_at_least_one_member;
} appleproj_interfaces__srv__GetPlanningScene_Request;

// Struct for a sequence of appleproj_interfaces__srv__GetPlanningScene_Request.
typedef struct appleproj_interfaces__srv__GetPlanningScene_Request__Sequence
{
  appleproj_interfaces__srv__GetPlanningScene_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__srv__GetPlanningScene_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'scene'
#include "appleproj_interfaces/msg/detail/planning_scene__struct.h"
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetPlanningScene in the package appleproj_interfaces.
typedef struct appleproj_interfaces__srv__GetPlanningScene_Response
{
  bool success;
  appleproj_interfaces__msg__PlanningScene scene;
  rosidl_runtime_c__String message;
} appleproj_interfaces__srv__GetPlanningScene_Response;

// Struct for a sequence of appleproj_interfaces__srv__GetPlanningScene_Response.
typedef struct appleproj_interfaces__srv__GetPlanningScene_Response__Sequence
{
  appleproj_interfaces__srv__GetPlanningScene_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__srv__GetPlanningScene_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  appleproj_interfaces__srv__GetPlanningScene_Event__request__MAX_SIZE = 1
};
// response
enum
{
  appleproj_interfaces__srv__GetPlanningScene_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/GetPlanningScene in the package appleproj_interfaces.
typedef struct appleproj_interfaces__srv__GetPlanningScene_Event
{
  service_msgs__msg__ServiceEventInfo info;
  appleproj_interfaces__srv__GetPlanningScene_Request__Sequence request;
  appleproj_interfaces__srv__GetPlanningScene_Response__Sequence response;
} appleproj_interfaces__srv__GetPlanningScene_Event;

// Struct for a sequence of appleproj_interfaces__srv__GetPlanningScene_Event.
typedef struct appleproj_interfaces__srv__GetPlanningScene_Event__Sequence
{
  appleproj_interfaces__srv__GetPlanningScene_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__srv__GetPlanningScene_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__STRUCT_H_
