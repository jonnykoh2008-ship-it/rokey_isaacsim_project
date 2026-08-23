// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "appleproj_interfaces/msg/detail/quality_result__rosidl_typesupport_introspection_c.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "appleproj_interfaces/msg/detail/quality_result__functions.h"
#include "appleproj_interfaces/msg/detail/quality_result__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `inspection_id`
// Member `apple_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `frame_indices`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `result_timestamp`
#include "builtin_interfaces/msg/time.h"
// Member `result_timestamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  appleproj_interfaces__msg__QualityResult__init(message_memory);
}

void appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_fini_function(void * message_memory)
{
  appleproj_interfaces__msg__QualityResult__fini(message_memory);
}

size_t appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__size_function__QualityResult__frame_indices(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint16__Sequence * member =
    (const rosidl_runtime_c__uint16__Sequence *)(untyped_member);
  return member->size;
}

const void * appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__get_const_function__QualityResult__frame_indices(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint16__Sequence * member =
    (const rosidl_runtime_c__uint16__Sequence *)(untyped_member);
  return &member->data[index];
}

void * appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__get_function__QualityResult__frame_indices(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint16__Sequence * member =
    (rosidl_runtime_c__uint16__Sequence *)(untyped_member);
  return &member->data[index];
}

void appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__fetch_function__QualityResult__frame_indices(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint16_t * item =
    ((const uint16_t *)
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__get_const_function__QualityResult__frame_indices(untyped_member, index));
  uint16_t * value =
    (uint16_t *)(untyped_value);
  *value = *item;
}

void appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__assign_function__QualityResult__frame_indices(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint16_t * item =
    ((uint16_t *)
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__get_function__QualityResult__frame_indices(untyped_member, index));
  const uint16_t * value =
    (const uint16_t *)(untyped_value);
  *item = *value;
}

bool appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__resize_function__QualityResult__frame_indices(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint16__Sequence * member =
    (rosidl_runtime_c__uint16__Sequence *)(untyped_member);
  rosidl_runtime_c__uint16__Sequence__fini(member);
  return rosidl_runtime_c__uint16__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_member_array[12] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "inspection_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, inspection_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "apple_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, apple_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "grade",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, grade),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color_ratio",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, color_ratio),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "diameter_mm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, diameter_mm),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "damage_area_cm2",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, damage_area_cm2),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frames_used",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, frames_used),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frame_indices",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, frame_indices),  // bytes offset in struct
    NULL,  // default value
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__size_function__QualityResult__frame_indices,  // size() function pointer
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__get_const_function__QualityResult__frame_indices,  // get_const(index) function pointer
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__get_function__QualityResult__frame_indices,  // get(index) function pointer
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__fetch_function__QualityResult__frame_indices,  // fetch(index, &value) function pointer
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__assign_function__QualityResult__frame_indices,  // assign(index, value) function pointer
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__resize_function__QualityResult__frame_indices  // resize(index) function pointer
  },
  {
    "result_timestamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, result_timestamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__QualityResult, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_members = {
  "appleproj_interfaces__msg",  // message namespace
  "QualityResult",  // message name
  12,  // number of fields
  sizeof(appleproj_interfaces__msg__QualityResult),
  false,  // has_any_key_member_
  appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_member_array,  // message members
  appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_init_function,  // function to initialize message memory (memory has to be allocated)
  appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_type_support_handle = {
  0,
  &appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_members,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__QualityResult__get_type_hash,
  &appleproj_interfaces__msg__QualityResult__get_type_description,
  &appleproj_interfaces__msg__QualityResult__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_appleproj_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, msg, QualityResult)() {
  appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_member_array[10].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_type_support_handle.typesupport_identifier) {
    appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &appleproj_interfaces__msg__QualityResult__rosidl_typesupport_introspection_c__QualityResult_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
