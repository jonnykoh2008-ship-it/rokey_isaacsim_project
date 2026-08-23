// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/MotionStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/motion_status.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'current_state'
// Member 'error_code'
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/MotionStatus in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__MotionStatus
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String current_state;
  bool success;
  float progress;
  rosidl_runtime_c__String error_code;
  rosidl_runtime_c__String message;
} appleproj_interfaces__msg__MotionStatus;

// Struct for a sequence of appleproj_interfaces__msg__MotionStatus.
typedef struct appleproj_interfaces__msg__MotionStatus__Sequence
{
  appleproj_interfaces__msg__MotionStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__MotionStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__STRUCT_H_
