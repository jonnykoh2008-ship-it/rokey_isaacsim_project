// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/InspectionImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/inspection_image.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/inspection_image__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_InspectionImage_image
{
public:
  explicit Init_InspectionImage_image(::appleproj_interfaces::msg::InspectionImage & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::InspectionImage image(::appleproj_interfaces::msg::InspectionImage::_image_type arg)
  {
    msg_.image = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::InspectionImage msg_;
};

class Init_InspectionImage_total_frames
{
public:
  explicit Init_InspectionImage_total_frames(::appleproj_interfaces::msg::InspectionImage & msg)
  : msg_(msg)
  {}
  Init_InspectionImage_image total_frames(::appleproj_interfaces::msg::InspectionImage::_total_frames_type arg)
  {
    msg_.total_frames = std::move(arg);
    return Init_InspectionImage_image(msg_);
  }

private:
  ::appleproj_interfaces::msg::InspectionImage msg_;
};

class Init_InspectionImage_frame_index
{
public:
  explicit Init_InspectionImage_frame_index(::appleproj_interfaces::msg::InspectionImage & msg)
  : msg_(msg)
  {}
  Init_InspectionImage_total_frames frame_index(::appleproj_interfaces::msg::InspectionImage::_frame_index_type arg)
  {
    msg_.frame_index = std::move(arg);
    return Init_InspectionImage_total_frames(msg_);
  }

private:
  ::appleproj_interfaces::msg::InspectionImage msg_;
};

class Init_InspectionImage_apple_id
{
public:
  explicit Init_InspectionImage_apple_id(::appleproj_interfaces::msg::InspectionImage & msg)
  : msg_(msg)
  {}
  Init_InspectionImage_frame_index apple_id(::appleproj_interfaces::msg::InspectionImage::_apple_id_type arg)
  {
    msg_.apple_id = std::move(arg);
    return Init_InspectionImage_frame_index(msg_);
  }

private:
  ::appleproj_interfaces::msg::InspectionImage msg_;
};

class Init_InspectionImage_inspection_id
{
public:
  explicit Init_InspectionImage_inspection_id(::appleproj_interfaces::msg::InspectionImage & msg)
  : msg_(msg)
  {}
  Init_InspectionImage_apple_id inspection_id(::appleproj_interfaces::msg::InspectionImage::_inspection_id_type arg)
  {
    msg_.inspection_id = std::move(arg);
    return Init_InspectionImage_apple_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::InspectionImage msg_;
};

class Init_InspectionImage_header
{
public:
  Init_InspectionImage_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_InspectionImage_inspection_id header(::appleproj_interfaces::msg::InspectionImage::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_InspectionImage_inspection_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::InspectionImage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::InspectionImage>()
{
  return appleproj_interfaces::msg::builder::Init_InspectionImage_header();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__BUILDER_HPP_
