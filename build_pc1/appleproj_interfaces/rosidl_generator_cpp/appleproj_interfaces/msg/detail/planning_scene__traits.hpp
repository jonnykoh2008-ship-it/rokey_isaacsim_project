// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/planning_scene.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/msg/detail/planning_scene__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'robot_base_pose'
// Member 'robot_tcp_pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"
// Member 'obstacles'
#include "appleproj_interfaces/msg/detail/obstacle_proxy__traits.hpp"

namespace appleproj_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const PlanningScene & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
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

  // member: robot_base_pose
  {
    out << "robot_base_pose: ";
    to_flow_style_yaml(msg.robot_base_pose, out);
    out << ", ";
  }

  // member: robot_tcp_pose
  {
    out << "robot_tcp_pose: ";
    to_flow_style_yaml(msg.robot_tcp_pose, out);
    out << ", ";
  }

  // member: obstacles
  {
    if (msg.obstacles.size() == 0) {
      out << "obstacles: []";
    } else {
      out << "obstacles: [";
      size_t pending_items = msg.obstacles.size();
      for (auto item : msg.obstacles) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlanningScene & msg,
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

  // member: robot_base_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_base_pose:\n";
    to_block_style_yaml(msg.robot_base_pose, out, indentation + 2);
  }

  // member: robot_tcp_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_tcp_pose:\n";
    to_block_style_yaml(msg.robot_tcp_pose, out, indentation + 2);
  }

  // member: obstacles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.obstacles.size() == 0) {
      out << "obstacles: []\n";
    } else {
      out << "obstacles:\n";
      for (auto item : msg.obstacles) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlanningScene & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::msg::PlanningScene & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::msg::PlanningScene & msg)
{
  return appleproj_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::msg::PlanningScene>()
{
  return "appleproj_interfaces::msg::PlanningScene";
}

template<>
inline const char * name<appleproj_interfaces::msg::PlanningScene>()
{
  return "appleproj_interfaces/msg/PlanningScene";
}

template<>
struct has_fixed_size<appleproj_interfaces::msg::PlanningScene>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::msg::PlanningScene>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::msg::PlanningScene>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__TRAITS_HPP_
