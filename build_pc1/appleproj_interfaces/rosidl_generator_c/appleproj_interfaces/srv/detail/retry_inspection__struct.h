// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:srv/RetryInspection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/retry_inspection.h"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__STRUCT_H_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'inspection_id'
// Member 'apple_id'
// Member 'reason'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/RetryInspection in the package appleproj_interfaces.
typedef struct appleproj_interfaces__srv__RetryInspection_Request
{
  rosidl_runtime_c__String inspection_id;
  rosidl_runtime_c__String apple_id;
  rosidl_runtime_c__String reason;
} appleproj_interfaces__srv__RetryInspection_Request;

// Struct for a sequence of appleproj_interfaces__srv__RetryInspection_Request.
typedef struct appleproj_interfaces__srv__RetryInspection_Request__Sequence
{
  appleproj_interfaces__srv__RetryInspection_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__srv__RetryInspection_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'new_inspection_id'
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/RetryInspection in the package appleproj_interfaces.
typedef struct appleproj_interfaces__srv__RetryInspection_Response
{
  bool accepted;
  rosidl_runtime_c__String new_inspection_id;
  rosidl_runtime_c__String message;
} appleproj_interfaces__srv__RetryInspection_Response;

// Struct for a sequence of appleproj_interfaces__srv__RetryInspection_Response.
typedef struct appleproj_interfaces__srv__RetryInspection_Response__Sequence
{
  appleproj_interfaces__srv__RetryInspection_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__srv__RetryInspection_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  appleproj_interfaces__srv__RetryInspection_Event__request__MAX_SIZE = 1
};
// response
enum
{
  appleproj_interfaces__srv__RetryInspection_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/RetryInspection in the package appleproj_interfaces.
typedef struct appleproj_interfaces__srv__RetryInspection_Event
{
  service_msgs__msg__ServiceEventInfo info;
  appleproj_interfaces__srv__RetryInspection_Request__Sequence request;
  appleproj_interfaces__srv__RetryInspection_Response__Sequence response;
} appleproj_interfaces__srv__RetryInspection_Event;

// Struct for a sequence of appleproj_interfaces__srv__RetryInspection_Event.
typedef struct appleproj_interfaces__srv__RetryInspection_Event__Sequence
{
  appleproj_interfaces__srv__RetryInspection_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__srv__RetryInspection_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__STRUCT_H_
