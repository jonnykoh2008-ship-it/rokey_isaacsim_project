// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/quality_result.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/msg/detail/quality_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'result_timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace appleproj_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const QualityResult & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: inspection_id
  {
    out << "inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.inspection_id, out);
    out << ", ";
  }

  // member: apple_id
  {
    out << "apple_id: ";
    rosidl_generator_traits::value_to_yaml(msg.apple_id, out);
    out << ", ";
  }

  // member: grade
  {
    out << "grade: ";
    rosidl_generator_traits::value_to_yaml(msg.grade, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: color_ratio
  {
    out << "color_ratio: ";
    rosidl_generator_traits::value_to_yaml(msg.color_ratio, out);
    out << ", ";
  }

  // member: diameter_mm
  {
    out << "diameter_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.diameter_mm, out);
    out << ", ";
  }

  // member: damage_area_cm2
  {
    out << "damage_area_cm2: ";
    rosidl_generator_traits::value_to_yaml(msg.damage_area_cm2, out);
    out << ", ";
  }

  // member: frames_used
  {
    out << "frames_used: ";
    rosidl_generator_traits::value_to_yaml(msg.frames_used, out);
    out << ", ";
  }

  // member: frame_indices
  {
    if (msg.frame_indices.size() == 0) {
      out << "frame_indices: []";
    } else {
      out << "frame_indices: [";
      size_t pending_items = msg.frame_indices.size();
      for (auto item : msg.frame_indices) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: result_timestamp
  {
    out << "result_timestamp: ";
    to_flow_style_yaml(msg.result_timestamp, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const QualityResult & msg,
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

  // member: inspection_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.inspection_id, out);
    out << "\n";
  }

  // member: apple_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "apple_id: ";
    rosidl_generator_traits::value_to_yaml(msg.apple_id, out);
    out << "\n";
  }

  // member: grade
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "grade: ";
    rosidl_generator_traits::value_to_yaml(msg.grade, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: color_ratio
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "color_ratio: ";
    rosidl_generator_traits::value_to_yaml(msg.color_ratio, out);
    out << "\n";
  }

  // member: diameter_mm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "diameter_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.diameter_mm, out);
    out << "\n";
  }

  // member: damage_area_cm2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "damage_area_cm2: ";
    rosidl_generator_traits::value_to_yaml(msg.damage_area_cm2, out);
    out << "\n";
  }

  // member: frames_used
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frames_used: ";
    rosidl_generator_traits::value_to_yaml(msg.frames_used, out);
    out << "\n";
  }

  // member: frame_indices
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.frame_indices.size() == 0) {
      out << "frame_indices: []\n";
    } else {
      out << "frame_indices:\n";
      for (auto item : msg.frame_indices) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: result_timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result_timestamp:\n";
    to_block_style_yaml(msg.result_timestamp, out, indentation + 2);
  }

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const QualityResult & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::msg::QualityResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::msg::QualityResult & msg)
{
  return appleproj_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::msg::QualityResult>()
{
  return "appleproj_interfaces::msg::QualityResult";
}

template<>
inline const char * name<appleproj_interfaces::msg::QualityResult>()
{
  return "appleproj_interfaces/msg/QualityResult";
}

template<>
struct has_fixed_size<appleproj_interfaces::msg::QualityResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::msg::QualityResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::msg::QualityResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__TRAITS_HPP_
