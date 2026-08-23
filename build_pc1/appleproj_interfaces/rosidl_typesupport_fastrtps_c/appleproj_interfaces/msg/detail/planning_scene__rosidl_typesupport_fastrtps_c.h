// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice
#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "appleproj_interfaces/msg/detail/planning_scene__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
bool cdr_serialize_appleproj_interfaces__msg__PlanningScene(
  const appleproj_interfaces__msg__PlanningScene * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
bool cdr_deserialize_appleproj_interfaces__msg__PlanningScene(
  eprosima::fastcdr::Cdr &,
  appleproj_interfaces__msg__PlanningScene * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t get_serialized_size_appleproj_interfaces__msg__PlanningScene(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t max_serialized_size_appleproj_interfaces__msg__PlanningScene(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
bool cdr_serialize_key_appleproj_interfaces__msg__PlanningScene(
  const appleproj_interfaces__msg__PlanningScene * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t get_serialized_size_key_appleproj_interfaces__msg__PlanningScene(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t max_serialized_size_key_appleproj_interfaces__msg__PlanningScene(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, msg, PlanningScene)();

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
