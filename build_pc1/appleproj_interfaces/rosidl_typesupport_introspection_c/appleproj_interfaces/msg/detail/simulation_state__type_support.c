// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from appleproj_interfaces:msg/SimulationState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "appleproj_interfaces/msg/detail/simulation_state__rosidl_typesupport_introspection_c.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "appleproj_interfaces/msg/detail/simulation_state__functions.h"
#include "appleproj_interfaces/msg/detail/simulation_state__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  appleproj_interfaces__msg__SimulationState__init(message_memory);
}

void appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_fini_function(void * message_memory)
{
  appleproj_interfaces__msg__SimulationState__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_member_array[5] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__SimulationState, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__SimulationState, state),  // bytes offset in struct
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
    offsetof(appleproj_interfaces__msg__SimulationState, reset_id),  // bytes offset in struct
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
    offsetof(appleproj_interfaces__msg__SimulationState, scene_version),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__SimulationState, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_members = {
  "appleproj_interfaces__msg",  // message namespace
  "SimulationState",  // message name
  5,  // number of fields
  sizeof(appleproj_interfaces__msg__SimulationState),
  false,  // has_any_key_member_
  appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_member_array,  // message members
  appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_init_function,  // function to initialize message memory (memory has to be allocated)
  appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_type_support_handle = {
  0,
  &appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_members,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__SimulationState__get_type_hash,
  &appleproj_interfaces__msg__SimulationState__get_type_description,
  &appleproj_interfaces__msg__SimulationState__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_appleproj_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, msg, SimulationState)() {
  appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_type_support_handle.typesupport_identifier) {
    appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &appleproj_interfaces__msg__SimulationState__rosidl_typesupport_introspection_c__SimulationState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
