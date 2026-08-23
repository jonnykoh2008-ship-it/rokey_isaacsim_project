// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/SimulationState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/simulation_state.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'STOPPED'.
enum
{
  appleproj_interfaces__msg__SimulationState__STOPPED = 0
};

/// Constant 'INITIALIZING'.
enum
{
  appleproj_interfaces__msg__SimulationState__INITIALIZING = 1
};

/// Constant 'READY'.
enum
{
  appleproj_interfaces__msg__SimulationState__READY = 2
};

/// Constant 'PLAYING'.
enum
{
  appleproj_interfaces__msg__SimulationState__PLAYING = 3
};

/// Constant 'PAUSED'.
enum
{
  appleproj_interfaces__msg__SimulationState__PAUSED = 4
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SimulationState in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__SimulationState
{
  std_msgs__msg__Header header;
  uint8_t state;
  uint64_t reset_id;
  uint64_t scene_version;
  rosidl_runtime_c__String message;
} appleproj_interfaces__msg__SimulationState;

// Struct for a sequence of appleproj_interfaces__msg__SimulationState.
typedef struct appleproj_interfaces__msg__SimulationState__Sequence
{
  appleproj_interfaces__msg__SimulationState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__SimulationState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__STRUCT_H_
