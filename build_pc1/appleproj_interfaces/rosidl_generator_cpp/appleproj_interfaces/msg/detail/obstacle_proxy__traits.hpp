// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:msg/ObstacleProxy.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/obstacle_proxy.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/msg/detail/obstacle_proxy__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'dimensions'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace appleproj_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObstacleProxy & msg,
  std::ostream & out)
{
  out << "{";
  // member: obstacle_id
  {
    out << "obstacle_id: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_id, out);
    out << ", ";
  }

  // member: shape
  {
    out << "shape: ";
    rosidl_generator_traits::value_to_yaml(msg.shape, out);
    out << ", ";
  }

  // member: obstacle_class
  {
    out << "obstacle_class: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_class, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: dimensions
  {
    out << "dimensions: ";
    to_flow_style_yaml(msg.dimensions, out);
    out << ", ";
  }

  // member: safety_margin
  {
    out << "safety_margin: ";
    rosidl_generator_traits::value_to_yaml(msg.safety_margin, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObstacleProxy & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: obstacle_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obstacle_id: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_id, out);
    out << "\n";
  }

  // member: shape
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "shape: ";
    rosidl_generator_traits::value_to_yaml(msg.shape, out);
    out << "\n";
  }

  // member: obstacle_class
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obstacle_class: ";
    rosidl_generator_traits::value_to_yaml(msg.obstacle_class, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: dimensions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "dimensions:\n";
    to_block_style_yaml(msg.dimensions, out, indentation + 2);
  }

  // member: safety_margin
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "safety_margin: ";
    rosidl_generator_traits::value_to_yaml(msg.safety_margin, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObstacleProxy & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::msg::ObstacleProxy & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::msg::ObstacleProxy & msg)
{
  return appleproj_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::msg::ObstacleProxy>()
{
  return "appleproj_interfaces::msg::ObstacleProxy";
}

template<>
inline const char * name<appleproj_interfaces::msg::ObstacleProxy>()
{
  return "appleproj_interfaces/msg/ObstacleProxy";
}

template<>
struct has_fixed_size<appleproj_interfaces::msg::ObstacleProxy>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::msg::ObstacleProxy>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::msg::ObstacleProxy>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__TRAITS_HPP_
