// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/CheckpointEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/checkpoint_event.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'ENTER'.
enum
{
  appleproj_interfaces__msg__CheckpointEvent__ENTER = 1
};

/// Constant 'EXIT'.
enum
{
  appleproj_interfaces__msg__CheckpointEvent__EXIT = 2
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'apple_id'
// Member 'checkpoint_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/CheckpointEvent in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__CheckpointEvent
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String apple_id;
  rosidl_runtime_c__String checkpoint_id;
  uint8_t event;
} appleproj_interfaces__msg__CheckpointEvent;

// Struct for a sequence of appleproj_interfaces__msg__CheckpointEvent.
typedef struct appleproj_interfaces__msg__CheckpointEvent__Sequence
{
  appleproj_interfaces__msg__CheckpointEvent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__CheckpointEvent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__STRUCT_H_
