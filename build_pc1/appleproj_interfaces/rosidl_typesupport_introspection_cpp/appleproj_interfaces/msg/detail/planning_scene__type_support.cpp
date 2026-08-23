// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"
#include "appleproj_interfaces/msg/detail/planning_scene__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace appleproj_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanningScene_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) appleproj_interfaces::msg::PlanningScene(_init);
}

void PlanningScene_fini_function(void * message_memory)
{
  auto typed_message = static_cast<appleproj_interfaces::msg::PlanningScene *>(message_memory);
  typed_message->~PlanningScene();
}

size_t size_function__PlanningScene__obstacles(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<appleproj_interfaces::msg::ObstacleProxy> *>(untyped_member);
  return member->size();
}

const void * get_const_function__PlanningScene__obstacles(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<appleproj_interfaces::msg::ObstacleProxy> *>(untyped_member);
  return &member[index];
}

void * get_function__PlanningScene__obstacles(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<appleproj_interfaces::msg::ObstacleProxy> *>(untyped_member);
  return &member[index];
}

void fetch_function__PlanningScene__obstacles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const appleproj_interfaces::msg::ObstacleProxy *>(
    get_const_function__PlanningScene__obstacles(untyped_member, index));
  auto & value = *reinterpret_cast<appleproj_interfaces::msg::ObstacleProxy *>(untyped_value);
  value = item;
}

void assign_function__PlanningScene__obstacles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<appleproj_interfaces::msg::ObstacleProxy *>(
    get_function__PlanningScene__obstacles(untyped_member, index));
  const auto & value = *reinterpret_cast<const appleproj_interfaces::msg::ObstacleProxy *>(untyped_value);
  item = value;
}

void resize_function__PlanningScene__obstacles(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<appleproj_interfaces::msg::ObstacleProxy> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanningScene_message_member_array[6] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::PlanningScene, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "reset_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::PlanningScene, reset_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "scene_version",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::PlanningScene, scene_version),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "robot_base_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::PlanningScene, robot_base_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "robot_tcp_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::PlanningScene, robot_tcp_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "obstacles",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<appleproj_interfaces::msg::ObstacleProxy>(),  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::PlanningScene, obstacles),  // bytes offset in struct
    nullptr,  // default value
    size_function__PlanningScene__obstacles,  // size() function pointer
    get_const_function__PlanningScene__obstacles,  // get_const(index) function pointer
    get_function__PlanningScene__obstacles,  // get(index) function pointer
    fetch_function__PlanningScene__obstacles,  // fetch(index, &value) function pointer
    assign_function__PlanningScene__obstacles,  // assign(index, value) function pointer
    resize_function__PlanningScene__obstacles  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanningScene_message_members = {
  "appleproj_interfaces::msg",  // message namespace
  "PlanningScene",  // message name
  6,  // number of fields
  sizeof(appleproj_interfaces::msg::PlanningScene),
  false,  // has_any_key_member_
  PlanningScene_message_member_array,  // message members
  PlanningScene_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanningScene_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanningScene_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanningScene_message_members,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__PlanningScene__get_type_hash,
  &appleproj_interfaces__msg__PlanningScene__get_type_description,
  &appleproj_interfaces__msg__PlanningScene__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace appleproj_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<appleproj_interfaces::msg::PlanningScene>()
{
  return &::appleproj_interfaces::msg::rosidl_typesupport_introspection_cpp::PlanningScene_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, appleproj_interfaces, msg, PlanningScene)() {
  return &::appleproj_interfaces::msg::rosidl_typesupport_introspection_cpp::PlanningScene_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
