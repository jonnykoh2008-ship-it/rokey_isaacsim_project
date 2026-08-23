// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "appleproj_interfaces/msg/detail/quality_result__struct.h"
#include "appleproj_interfaces/msg/detail/quality_result__type_support.h"
#include "appleproj_interfaces/msg/detail/quality_result__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace msg
{

namespace rosidl_typesupport_c
{

typedef struct _QualityResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _QualityResult_type_support_ids_t;

static const _QualityResult_type_support_ids_t _QualityResult_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _QualityResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _QualityResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _QualityResult_type_support_symbol_names_t _QualityResult_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, msg, QualityResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, msg, QualityResult)),
  }
};

typedef struct _QualityResult_type_support_data_t
{
  void * data[2];
} _QualityResult_type_support_data_t;

static _QualityResult_type_support_data_t _QualityResult_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _QualityResult_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_QualityResult_message_typesupport_ids.typesupport_identifier[0],
  &_QualityResult_message_typesupport_symbol_names.symbol_name[0],
  &_QualityResult_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t QualityResult_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_QualityResult_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__QualityResult__get_type_hash,
  &appleproj_interfaces__msg__QualityResult__get_type_description,
  &appleproj_interfaces__msg__QualityResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace msg

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, msg, QualityResult)() {
  return &::appleproj_interfaces::msg::rosidl_typesupport_c::QualityResult_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
