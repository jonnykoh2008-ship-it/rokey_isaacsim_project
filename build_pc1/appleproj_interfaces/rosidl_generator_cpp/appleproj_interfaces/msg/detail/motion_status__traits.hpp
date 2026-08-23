// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:msg/MotionStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/motion_status.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/msg/detail/motion_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace appleproj_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotionStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: current_state
  {
    out << "current_state: ";
    rosidl_generator_traits::value_to_yaml(msg.current_state, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: progress
  {
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << ", ";
  }

  // member: error_code
  {
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotionStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: current_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_state: ";
    rosidl_generator_traits::value_to_yaml(msg.current_state, out);
    out << "\n";
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: progress
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << "\n";
  }

  // member: error_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotionStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace appleproj_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use appleproj_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const appleproj_interfaces::msg::MotionStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::msg::MotionStatus & msg)
{
  return appleproj_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::msg::MotionStatus>()
{
  return "appleproj_interfaces::msg::MotionStatus";
}

template<>
inline const char * name<appleproj_interfaces::msg::MotionStatus>()
{
  return "appleproj_interfaces/msg/MotionStatus";
}

template<>
struct has_fixed_size<appleproj_interfaces::msg::MotionStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::msg::MotionStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::msg::MotionStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__TRAITS_HPP_
