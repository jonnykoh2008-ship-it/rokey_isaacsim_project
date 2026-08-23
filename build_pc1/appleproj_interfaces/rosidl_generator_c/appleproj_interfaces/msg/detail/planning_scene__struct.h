// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/planning_scene.h"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__STRUCT_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__STRUCT_H_

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
// Member 'robot_base_pose'
// Member 'robot_tcp_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"
// Member 'obstacles'
#include "appleproj_interfaces/msg/detail/obstacle_proxy__struct.h"

/// Struct defined in msg/PlanningScene in the package appleproj_interfaces.
typedef struct appleproj_interfaces__msg__PlanningScene
{
  std_msgs__msg__Header header;
  uint64_t reset_id;
  uint64_t scene_version;
  geometry_msgs__msg__PoseStamped robot_base_pose;
  geometry_msgs__msg__PoseStamped robot_tcp_pose;
  appleproj_interfaces__msg__ObstacleProxy__Sequence obstacles;
} appleproj_interfaces__msg__PlanningScene;

// Struct for a sequence of appleproj_interfaces__msg__PlanningScene.
typedef struct appleproj_interfaces__msg__PlanningScene__Sequence
{
  appleproj_interfaces__msg__PlanningScene * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} appleproj_interfaces__msg__PlanningScene__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__STRUCT_H_
