// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/quality_result.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'HIGH'.
enum
{
  appleproj_interfaces__msg__QualityResult__HIGH = 1
};

/// Constant 'MEDIUM'.
enum
{
  appleproj_interfaces__msg__QualityResult__MEDIUM = 2
};

/// Constant 'LOW'.
enum
{
  appleproj_interfaces__msg__QualityResult__LOW = 3
};

/// Constant 'VALID'.
enum
{
  appleproj_interfaces__msg__QualityResult__VALID = 1
};

/// Constant 'RECHECK'.
enum
{
  appleproj_interfaces__msg__QualityResult__RECHECK = 2
};

/// Constant 'UNCLASSIFIED'.
enum
{
  appleproj_interfaces__msg__QualityResult__UNCLASSIFIED = 3
};

/// Constant 'TIMEOUT'.
enum
{
  appleproj_interfaces__msg__QualityResult__TIMEOUT = 4
};

/// Constant 'LATE_RESULT'.
enum
{
  appleproj_interfaces__msg__QualityResult__LATE_RESULT = 5
};

/// Constant 'ID_MISMATCH'.
enum
{
  appleproj_interfaces__msg__QualityResult__ID_MISMATCH = 6
};

/// Constant 'INSUFFICIENT_VIEWS'.
enum
{
  appleproj_interfaces__msg__QualityResult__INSUFFICIENT_VIEWS = 7
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'inspection_id'
// Member 'apple_id'
#include "rosidl_runtime_c/string.h"
// Member 'frame_indices'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'result_timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/QualityResult in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__QualityResult
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String inspection_id;
  rosidl_runtime_c__String apple_id;
  uint8_t grade;
  float confidence;
  float color_ratio;
  float diameter_mm;
  float damage_area_cm2;
  uint16_t frames_used;
  rosidl_runtime_c__uint16__Sequence frame_indices;
  builtin_interfaces__msg__Time result_timestamp;
  uint8_t status;
} appleproj_interfaces__msg__QualityResult;

// Struct for a sequence of appleproj_interfaces__msg__QualityResult.
typedef struct appleproj_interfaces__msg__QualityResult__Sequence
{
  appleproj_interfaces__msg__QualityResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__QualityResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__STRUCT_H_
