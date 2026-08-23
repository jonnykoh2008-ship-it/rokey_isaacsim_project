// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/CheckpointEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/checkpoint_event.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/checkpoint_event__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_CheckpointEvent_event
{
public:
  explicit Init_CheckpointEvent_event(::appleproj_interfaces::msg::CheckpointEvent & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::CheckpointEvent event(::appleproj_interfaces::msg::CheckpointEvent::_event_type arg)
  {
    msg_.event = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::CheckpointEvent msg_;
};

class Init_CheckpointEvent_checkpoint_id
{
public:
  explicit Init_CheckpointEvent_checkpoint_id(::appleproj_interfaces::msg::CheckpointEvent & msg)
  : msg_(msg)
  {}
  Init_CheckpointEvent_event checkpoint_id(::appleproj_interfaces::msg::CheckpointEvent::_checkpoint_id_type arg)
  {
    msg_.checkpoint_id = std::move(arg);
    return Init_CheckpointEvent_event(msg_);
  }

private:
  ::appleproj_interfaces::msg::CheckpointEvent msg_;
};

class Init_CheckpointEvent_apple_id
{
public:
  explicit Init_CheckpointEvent_apple_id(::appleproj_interfaces::msg::CheckpointEvent & msg)
  : msg_(msg)
  {}
  Init_CheckpointEvent_checkpoint_id apple_id(::appleproj_interfaces::msg::CheckpointEvent::_apple_id_type arg)
  {
    msg_.apple_id = std::move(arg);
    return Init_CheckpointEvent_checkpoint_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::CheckpointEvent msg_;
};

class Init_CheckpointEvent_header
{
public:
  Init_CheckpointEvent_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CheckpointEvent_apple_id header(::appleproj_interfaces::msg::CheckpointEvent::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_CheckpointEvent_apple_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::CheckpointEvent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::CheckpointEvent>()
{
  return appleproj_interfaces::msg::builder::Init_CheckpointEvent_header();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__BUILDER_HPP_
