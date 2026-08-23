// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:msg/SimulationState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/simulation_state.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/msg/detail/simulation_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace appleproj_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const SimulationState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << ", ";
  }

  // member: reset_id
  {
    out << "reset_id: ";
    rosidl_generator_traits::value_to_yaml(msg.reset_id, out);
    out << ", ";
  }

  // member: scene_version
  {
    out << "scene_version: ";
    rosidl_generator_traits::value_to_yaml(msg.scene_version, out);
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
  const SimulationState & msg,
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

  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }

  // member: reset_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reset_id: ";
    rosidl_generator_traits::value_to_yaml(msg.reset_id, out);
    out << "\n";
  }

  // member: scene_version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scene_version: ";
    rosidl_generator_traits::value_to_yaml(msg.scene_version, out);
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

inline std::string to_yaml(const SimulationState & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::msg::SimulationState & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::msg::SimulationState & msg)
{
  return appleproj_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::msg::SimulationState>()
{
  return "appleproj_interfaces::msg::SimulationState";
}

template<>
inline const char * name<appleproj_interfaces::msg::SimulationState>()
{
  return "appleproj_interfaces/msg/SimulationState";
}

template<>
struct has_fixed_size<appleproj_interfaces::msg::SimulationState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::msg::SimulationState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::msg::SimulationState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__TRAITS_HPP_
