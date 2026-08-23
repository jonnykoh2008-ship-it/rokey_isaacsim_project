// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "appleproj_interfaces/msg/detail/planning_scene__rosidl_typesupport_introspection_c.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"
#include "appleproj_interfaces/msg/detail/planning_scene__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `robot_base_pose`
// Member `robot_tcp_pose`
#include "geometry_msgs/msg/pose_stamped.h"
// Member `robot_base_pose`
// Member `robot_tcp_pose`
#include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"
// Member `obstacles`
#include "appleproj_interfaces/msg/obstacle_proxy.h"
// Member `obstacles`
#include "appleproj_interfaces/msg/detail/obstacle_proxy__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  appleproj_interfaces__msg__PlanningScene__init(message_memory);
}

void appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_fini_function(void * message_memory)
{
  appleproj_interfaces__msg__PlanningScene__fini(message_memory);
}

size_t appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__size_function__PlanningScene__obstacles(
  const void * untyped_member)
{
  const appleproj_interfaces__msg__ObstacleProxy__Sequence * member =
    (const appleproj_interfaces__msg__ObstacleProxy__Sequence *)(untyped_member);
  return member->size;
}

const void * appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__get_const_function__PlanningScene__obstacles(
  const void * untyped_member, size_t index)
{
  const appleproj_interfaces__msg__ObstacleProxy__Sequence * member =
    (const appleproj_interfaces__msg__ObstacleProxy__Sequence *)(untyped_member);
  return &member->data[index];
}

void * appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__get_function__PlanningScene__obstacles(
  void * untyped_member, size_t index)
{
  appleproj_interfaces__msg__ObstacleProxy__Sequence * member =
    (appleproj_interfaces__msg__ObstacleProxy__Sequence *)(untyped_member);
  return &member->data[index];
}

void appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__fetch_function__PlanningScene__obstacles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const appleproj_interfaces__msg__ObstacleProxy * item =
    ((const appleproj_interfaces__msg__ObstacleProxy *)
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__get_const_function__PlanningScene__obstacles(untyped_member, index));
  appleproj_interfaces__msg__ObstacleProxy * value =
    (appleproj_interfaces__msg__ObstacleProxy *)(untyped_value);
  *value = *item;
}

void appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__assign_function__PlanningScene__obstacles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  appleproj_interfaces__msg__ObstacleProxy * item =
    ((appleproj_interfaces__msg__ObstacleProxy *)
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__get_function__PlanningScene__obstacles(untyped_member, index));
  const appleproj_interfaces__msg__ObstacleProxy * value =
    (const appleproj_interfaces__msg__ObstacleProxy *)(untyped_value);
  *item = *value;
}

bool appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__resize_function__PlanningScene__obstacles(
  void * untyped_member, size_t size)
{
  appleproj_interfaces__msg__ObstacleProxy__Sequence * member =
    (appleproj_interfaces__msg__ObstacleProxy__Sequence *)(untyped_member);
  appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(member);
  return appleproj_interfaces__msg__ObstacleProxy__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_member_array[6] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__PlanningScene, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reset_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__PlanningScene, reset_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "scene_version",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__PlanningScene, scene_version),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "robot_base_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__PlanningScene, robot_base_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "robot_tcp_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__PlanningScene, robot_tcp_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "obstacles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__PlanningScene, obstacles),  // bytes offset in struct
    NULL,  // default value
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__size_function__PlanningScene__obstacles,  // size() function pointer
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__get_const_function__PlanningScene__obstacles,  // get_const(index) function pointer
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__get_function__PlanningScene__obstacles,  // get(index) function pointer
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__fetch_function__PlanningScene__obstacles,  // fetch(index, &value) function pointer
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__assign_function__PlanningScene__obstacles,  // assign(index, value) function pointer
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__resize_function__PlanningScene__obstacles  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_members = {
  "appleproj_interfaces__msg",  // message namespace
  "PlanningScene",  // message name
  6,  // number of fields
  sizeof(appleproj_interfaces__msg__PlanningScene),
  false,  // has_any_key_member_
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_member_array,  // message members
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_init_function,  // function to initialize message memory (memory has to be allocated)
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_type_support_handle = {
  0,
  &appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_members,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__PlanningScene__get_type_hash,
  &appleproj_interfaces__msg__PlanningScene__get_type_description,
  &appleproj_interfaces__msg__PlanningScene__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_appleproj_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, msg, PlanningScene)() {
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, msg, ObstacleProxy)();
  if (!appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_type_support_handle.typesupport_identifier) {
    appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &appleproj_interfaces__msg__PlanningScene__rosidl_typesupport_introspection_c__PlanningScene_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
