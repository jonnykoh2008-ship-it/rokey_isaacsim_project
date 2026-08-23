// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/ObstacleProxy.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/obstacle_proxy.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'SHAPE_SPHERE'.
enum
{
  appleproj_interfaces__msg__ObstacleProxy__SHAPE_SPHERE = 1
};

/// Constant 'SHAPE_BOX'.
enum
{
  appleproj_interfaces__msg__ObstacleProxy__SHAPE_BOX = 2
};

/// Constant 'SHAPE_CAPSULE'.
enum
{
  appleproj_interfaces__msg__ObstacleProxy__SHAPE_CAPSULE = 3
};

/// Constant 'CLASS_TRUNK'.
enum
{
  appleproj_interfaces__msg__ObstacleProxy__CLASS_TRUNK = 1
};

/// Constant 'CLASS_BRANCH'.
enum
{
  appleproj_interfaces__msg__ObstacleProxy__CLASS_BRANCH = 2
};

// Include directives for member types
// Member 'obstacle_id'
#include "rosidl_runtime_c/string.h"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'dimensions'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/ObstacleProxy in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__ObstacleProxy
{
  rosidl_runtime_c__String obstacle_id;
  uint8_t shape;
  uint8_t obstacle_class;
  geometry_msgs__msg__Pose pose;
  geometry_msgs__msg__Vector3 dimensions;
  double safety_margin;
} appleproj_interfaces__msg__ObstacleProxy;

// Struct for a sequence of appleproj_interfaces__msg__ObstacleProxy.
typedef struct appleproj_interfaces__msg__ObstacleProxy__Sequence
{
  appleproj_interfaces__msg__ObstacleProxy * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__ObstacleProxy__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__STRUCT_H_
