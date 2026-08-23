// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/MotionStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/motion_status.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/motion_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_MotionStatus_message
{
public:
  explicit Init_MotionStatus_message(::appleproj_interfaces::msg::MotionStatus & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::MotionStatus message(::appleproj_interfaces::msg::MotionStatus::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::MotionStatus msg_;
};

class Init_MotionStatus_error_code
{
public:
  explicit Init_MotionStatus_error_code(::appleproj_interfaces::msg::MotionStatus & msg)
  : msg_(msg)
  {}
  Init_MotionStatus_message error_code(::appleproj_interfaces::msg::MotionStatus::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_MotionStatus_message(msg_);
  }

private:
  ::appleproj_interfaces::msg::MotionStatus msg_;
};

class Init_MotionStatus_progress
{
public:
  explicit Init_MotionStatus_progress(::appleproj_interfaces::msg::MotionStatus & msg)
  : msg_(msg)
  {}
  Init_MotionStatus_error_code progress(::appleproj_interfaces::msg::MotionStatus::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_MotionStatus_error_code(msg_);
  }

private:
  ::appleproj_interfaces::msg::MotionStatus msg_;
};

class Init_MotionStatus_success
{
public:
  explicit Init_MotionStatus_success(::appleproj_interfaces::msg::MotionStatus & msg)
  : msg_(msg)
  {}
  Init_MotionStatus_progress success(::appleproj_interfaces::msg::MotionStatus::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MotionStatus_progress(msg_);
  }

private:
  ::appleproj_interfaces::msg::MotionStatus msg_;
};

class Init_MotionStatus_current_state
{
public:
  explicit Init_MotionStatus_current_state(::appleproj_interfaces::msg::MotionStatus & msg)
  : msg_(msg)
  {}
  Init_MotionStatus_success current_state(::appleproj_interfaces::msg::MotionStatus::_current_state_type arg)
  {
    msg_.current_state = std::move(arg);
    return Init_MotionStatus_success(msg_);
  }

private:
  ::appleproj_interfaces::msg::MotionStatus msg_;
};

class Init_MotionStatus_header
{
public:
  Init_MotionStatus_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotionStatus_current_state header(::appleproj_interfaces::msg::MotionStatus::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_MotionStatus_current_state(msg_);
  }

private:
  ::appleproj_interfaces::msg::MotionStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::MotionStatus>()
{
  return appleproj_interfaces::msg::builder::Init_MotionStatus_header();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__BUILDER_HPP_
