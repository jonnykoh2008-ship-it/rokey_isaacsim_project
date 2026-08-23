// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:msg/InspectionImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/inspection_image.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/msg/detail/inspection_image__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'image'
#include "sensor_msgs/msg/detail/compressed_image__traits.hpp"

namespace appleproj_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const InspectionImage & msg,
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

  // member: frame_index
  {
    out << "frame_index: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_index, out);
    out << ", ";
  }

  // member: total_frames
  {
    out << "total_frames: ";
    rosidl_generator_traits::value_to_yaml(msg.total_frames, out);
    out << ", ";
  }

  // member: image
  {
    out << "image: ";
    to_flow_style_yaml(msg.image, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const InspectionImage & msg,
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

  // member: frame_index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame_index: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_index, out);
    out << "\n";
  }

  // member: total_frames
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "total_frames: ";
    rosidl_generator_traits::value_to_yaml(msg.total_frames, out);
    out << "\n";
  }

  // member: image
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image:\n";
    to_block_style_yaml(msg.image, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const InspectionImage & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::msg::InspectionImage & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::msg::InspectionImage & msg)
{
  return appleproj_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::msg::InspectionImage>()
{
  return "appleproj_interfaces::msg::InspectionImage";
}

template<>
inline const char * name<appleproj_interfaces::msg::InspectionImage>()
{
  return "appleproj_interfaces/msg/InspectionImage";
}

template<>
struct has_fixed_size<appleproj_interfaces::msg::InspectionImage>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::msg::InspectionImage>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::msg::InspectionImage>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__TRAITS_HPP_
