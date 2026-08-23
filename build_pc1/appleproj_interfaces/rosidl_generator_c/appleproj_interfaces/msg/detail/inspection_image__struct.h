// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/InspectionImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/inspection_image.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__STRUCT_H_

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
// Member 'inspection_id'
// Member 'apple_id'
#include "rosidl_runtime_c/string.h"
// Member 'image'
#include "sensor_msgs/msg/detail/compressed_image__struct.h"

/// Struct defined in msg/InspectionImage in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__InspectionImage
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String inspection_id;
  rosidl_runtime_c__String apple_id;
  uint16_t frame_index;
  uint16_t total_frames;
  sensor_msgs__msg__CompressedImage image;
} appleproj_interfaces__msg__InspectionImage;

// Struct for a sequence of appleproj_interfaces__msg__InspectionImage.
typedef struct appleproj_interfaces__msg__InspectionImage__Sequence
{
  appleproj_interfaces__msg__InspectionImage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__InspectionImage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__STRUCT_H_
