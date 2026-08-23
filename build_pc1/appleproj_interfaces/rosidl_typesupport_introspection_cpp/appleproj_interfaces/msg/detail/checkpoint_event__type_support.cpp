// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from appleproj_interfaces:msg/CheckpointEvent.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "appleproj_interfaces/msg/detail/checkpoint_event__functions.h"
#include "appleproj_interfaces/msg/detail/checkpoint_event__struct.hpp"
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

void CheckpointEvent_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) appleproj_interfaces::msg::CheckpointEvent(_init);
}

void CheckpointEvent_fini_function(void * message_memory)
{
  auto typed_message = static_cast<appleproj_interfaces::msg::CheckpointEvent *>(message_memory);
  typed_message->~CheckpointEvent();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember CheckpointEvent_message_member_array[4] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::CheckpointEvent, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "apple_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::CheckpointEvent, apple_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "checkpoint_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::CheckpointEvent, checkpoint_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "event",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces::msg::CheckpointEvent, event),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers CheckpointEvent_message_members = {
  "appleproj_interfaces::msg",  // message namespace
  "CheckpointEvent",  // message name
  4,  // number of fields
  sizeof(appleproj_interfaces::msg::CheckpointEvent),
  false,  // has_any_key_member_
  CheckpointEvent_message_member_array,  // message members
  CheckpointEvent_init_function,  // function to initialize message memory (memory has to be allocated)
  CheckpointEvent_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t CheckpointEvent_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &CheckpointEvent_message_members,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__CheckpointEvent__get_type_hash,
  &appleproj_interfaces__msg__CheckpointEvent__get_type_description,
  &appleproj_interfaces__msg__CheckpointEvent__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace appleproj_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<appleproj_interfaces::msg::CheckpointEvent>()
{
  return &::appleproj_interfaces::msg::rosidl_typesupport_introspection_cpp::CheckpointEvent_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, appleproj_interfaces, msg, CheckpointEvent)() {
  return &::appleproj_interfaces::msg::rosidl_typesupport_introspection_cpp::CheckpointEvent_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
