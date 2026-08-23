// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from appleproj_interfaces:msg/SimulationState.idl
// generated code does not contain a copyright notice

#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "appleproj_interfaces/msg/detail/simulation_state__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace appleproj_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
cdr_serialize(
  const appleproj_interfaces::msg::SimulationState & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  appleproj_interfaces::msg::SimulationState & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
get_serialized_size(
  const appleproj_interfaces::msg::SimulationState & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
max_serialized_size_SimulationState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
cdr_serialize_key(
  const appleproj_interfaces::msg::SimulationState & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
get_serialized_size_key(
  const appleproj_interfaces::msg::SimulationState & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
max_serialized_size_key_SimulationState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_appleproj_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, appleproj_interfaces, msg, SimulationState)();

#ifdef __cplusplus
}
#endif

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
