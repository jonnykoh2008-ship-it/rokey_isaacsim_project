// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from appleproj_interfaces:msg/InspectionImage.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "appleproj_interfaces/msg/detail/inspection_image__rosidl_typesupport_introspection_c.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "appleproj_interfaces/msg/detail/inspection_image__functions.h"
#include "appleproj_interfaces/msg/detail/inspection_image__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `inspection_id`
// Member `apple_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `image`
#include "sensor_msgs/msg/compressed_image.h"
// Member `image`
#include "sensor_msgs/msg/detail/compressed_image__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  appleproj_interfaces__msg__InspectionImage__init(message_memory);
}

void appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_fini_function(void * message_memory)
{
  appleproj_interfaces__msg__InspectionImage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_member_array[6] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__InspectionImage, header),  // bytes offset in struct
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
    offsetof(appleproj_interfaces__msg__InspectionImage, inspection_id),  // bytes offset in struct
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
    offsetof(appleproj_interfaces__msg__InspectionImage, apple_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frame_index",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__InspectionImage, frame_index),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "total_frames",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__InspectionImage, total_frames),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "image",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(appleproj_interfaces__msg__InspectionImage, image),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_members = {
  "appleproj_interfaces__msg",  // message namespace
  "InspectionImage",  // message name
  6,  // number of fields
  sizeof(appleproj_interfaces__msg__InspectionImage),
  false,  // has_any_key_member_
  appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_member_array,  // message members
  appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_init_function,  // function to initialize message memory (memory has to be allocated)
  appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_type_support_handle = {
  0,
  &appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_members,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__InspectionImage__get_type_hash,
  &appleproj_interfaces__msg__InspectionImage__get_type_description,
  &appleproj_interfaces__msg__InspectionImage__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_appleproj_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, msg, InspectionImage)() {
  appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, CompressedImage)();
  if (!appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_type_support_handle.typesupport_identifier) {
    appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &appleproj_interfaces__msg__InspectionImage__rosidl_typesupport_introspection_c__InspectionImage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
