// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/quality_result.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/quality_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_QualityResult_status
{
public:
  explicit Init_QualityResult_status(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::QualityResult status(::appleproj_interfaces::msg::QualityResult::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_result_timestamp
{
public:
  explicit Init_QualityResult_result_timestamp(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_status result_timestamp(::appleproj_interfaces::msg::QualityResult::_result_timestamp_type arg)
  {
    msg_.result_timestamp = std::move(arg);
    return Init_QualityResult_status(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_frame_indices
{
public:
  explicit Init_QualityResult_frame_indices(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_result_timestamp frame_indices(::appleproj_interfaces::msg::QualityResult::_frame_indices_type arg)
  {
    msg_.frame_indices = std::move(arg);
    return Init_QualityResult_result_timestamp(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_frames_used
{
public:
  explicit Init_QualityResult_frames_used(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_frame_indices frames_used(::appleproj_interfaces::msg::QualityResult::_frames_used_type arg)
  {
    msg_.frames_used = std::move(arg);
    return Init_QualityResult_frame_indices(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_damage_area_cm2
{
public:
  explicit Init_QualityResult_damage_area_cm2(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_frames_used damage_area_cm2(::appleproj_interfaces::msg::QualityResult::_damage_area_cm2_type arg)
  {
    msg_.damage_area_cm2 = std::move(arg);
    return Init_QualityResult_frames_used(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_diameter_mm
{
public:
  explicit Init_QualityResult_diameter_mm(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_damage_area_cm2 diameter_mm(::appleproj_interfaces::msg::QualityResult::_diameter_mm_type arg)
  {
    msg_.diameter_mm = std::move(arg);
    return Init_QualityResult_damage_area_cm2(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_color_ratio
{
public:
  explicit Init_QualityResult_color_ratio(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_diameter_mm color_ratio(::appleproj_interfaces::msg::QualityResult::_color_ratio_type arg)
  {
    msg_.color_ratio = std::move(arg);
    return Init_QualityResult_diameter_mm(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_confidence
{
public:
  explicit Init_QualityResult_confidence(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_color_ratio confidence(::appleproj_interfaces::msg::QualityResult::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_QualityResult_color_ratio(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_grade
{
public:
  explicit Init_QualityResult_grade(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_confidence grade(::appleproj_interfaces::msg::QualityResult::_grade_type arg)
  {
    msg_.grade = std::move(arg);
    return Init_QualityResult_confidence(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_apple_id
{
public:
  explicit Init_QualityResult_apple_id(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_grade apple_id(::appleproj_interfaces::msg::QualityResult::_apple_id_type arg)
  {
    msg_.apple_id = std::move(arg);
    return Init_QualityResult_grade(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_inspection_id
{
public:
  explicit Init_QualityResult_inspection_id(::appleproj_interfaces::msg::QualityResult & msg)
  : msg_(msg)
  {}
  Init_QualityResult_apple_id inspection_id(::appleproj_interfaces::msg::QualityResult::_inspection_id_type arg)
  {
    msg_.inspection_id = std::move(arg);
    return Init_QualityResult_apple_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

class Init_QualityResult_header
{
public:
  Init_QualityResult_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QualityResult_inspection_id header(::appleproj_interfaces::msg::QualityResult::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_QualityResult_inspection_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::QualityResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::QualityResult>()
{
  return appleproj_interfaces::msg::builder::Init_QualityResult_header();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__BUILDER_HPP_
