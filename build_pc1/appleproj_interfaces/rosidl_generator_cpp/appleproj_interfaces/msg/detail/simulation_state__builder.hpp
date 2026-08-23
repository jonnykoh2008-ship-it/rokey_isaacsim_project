// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/SimulationState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/simulation_state.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/simulation_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_SimulationState_message
{
public:
  explicit Init_SimulationState_message(::appleproj_interfaces::msg::SimulationState & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::SimulationState message(::appleproj_interfaces::msg::SimulationState::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::SimulationState msg_;
};

class Init_SimulationState_scene_version
{
public:
  explicit Init_SimulationState_scene_version(::appleproj_interfaces::msg::SimulationState & msg)
  : msg_(msg)
  {}
  Init_SimulationState_message scene_version(::appleproj_interfaces::msg::SimulationState::_scene_version_type arg)
  {
    msg_.scene_version = std::move(arg);
    return Init_SimulationState_message(msg_);
  }

private:
  ::appleproj_interfaces::msg::SimulationState msg_;
};

class Init_SimulationState_reset_id
{
public:
  explicit Init_SimulationState_reset_id(::appleproj_interfaces::msg::SimulationState & msg)
  : msg_(msg)
  {}
  Init_SimulationState_scene_version reset_id(::appleproj_interfaces::msg::SimulationState::_reset_id_type arg)
  {
    msg_.reset_id = std::move(arg);
    return Init_SimulationState_scene_version(msg_);
  }

private:
  ::appleproj_interfaces::msg::SimulationState msg_;
};

class Init_SimulationState_state
{
public:
  explicit Init_SimulationState_state(::appleproj_interfaces::msg::SimulationState & msg)
  : msg_(msg)
  {}
  Init_SimulationState_reset_id state(::appleproj_interfaces::msg::SimulationState::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_SimulationState_reset_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::SimulationState msg_;
};

class Init_SimulationState_header
{
public:
  Init_SimulationState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SimulationState_state header(::appleproj_interfaces::msg::SimulationState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_SimulationState_state(msg_);
  }

private:
  ::appleproj_interfaces::msg::SimulationState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::SimulationState>()
{
  return appleproj_interfaces::msg::builder::Init_SimulationState_header();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__BUILDER_HPP_
