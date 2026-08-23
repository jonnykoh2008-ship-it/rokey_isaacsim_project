// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/ObstacleProxy.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/obstacle_proxy.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/obstacle_proxy__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_ObstacleProxy_safety_margin
{
public:
  explicit Init_ObstacleProxy_safety_margin(::appleproj_interfaces::msg::ObstacleProxy & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::ObstacleProxy safety_margin(::appleproj_interfaces::msg::ObstacleProxy::_safety_margin_type arg)
  {
    msg_.safety_margin = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::ObstacleProxy msg_;
};

class Init_ObstacleProxy_dimensions
{
public:
  explicit Init_ObstacleProxy_dimensions(::appleproj_interfaces::msg::ObstacleProxy & msg)
  : msg_(msg)
  {}
  Init_ObstacleProxy_safety_margin dimensions(::appleproj_interfaces::msg::ObstacleProxy::_dimensions_type arg)
  {
    msg_.dimensions = std::move(arg);
    return Init_ObstacleProxy_safety_margin(msg_);
  }

private:
  ::appleproj_interfaces::msg::ObstacleProxy msg_;
};

class Init_ObstacleProxy_pose
{
public:
  explicit Init_ObstacleProxy_pose(::appleproj_interfaces::msg::ObstacleProxy & msg)
  : msg_(msg)
  {}
  Init_ObstacleProxy_dimensions pose(::appleproj_interfaces::msg::ObstacleProxy::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_ObstacleProxy_dimensions(msg_);
  }

private:
  ::appleproj_interfaces::msg::ObstacleProxy msg_;
};

class Init_ObstacleProxy_obstacle_class
{
public:
  explicit Init_ObstacleProxy_obstacle_class(::appleproj_interfaces::msg::ObstacleProxy & msg)
  : msg_(msg)
  {}
  Init_ObstacleProxy_pose obstacle_class(::appleproj_interfaces::msg::ObstacleProxy::_obstacle_class_type arg)
  {
    msg_.obstacle_class = std::move(arg);
    return Init_ObstacleProxy_pose(msg_);
  }

private:
  ::appleproj_interfaces::msg::ObstacleProxy msg_;
};

class Init_ObstacleProxy_shape
{
public:
  explicit Init_ObstacleProxy_shape(::appleproj_interfaces::msg::ObstacleProxy & msg)
  : msg_(msg)
  {}
  Init_ObstacleProxy_obstacle_class shape(::appleproj_interfaces::msg::ObstacleProxy::_shape_type arg)
  {
    msg_.shape = std::move(arg);
    return Init_ObstacleProxy_obstacle_class(msg_);
  }

private:
  ::appleproj_interfaces::msg::ObstacleProxy msg_;
};

class Init_ObstacleProxy_obstacle_id
{
public:
  Init_ObstacleProxy_obstacle_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObstacleProxy_shape obstacle_id(::appleproj_interfaces::msg::ObstacleProxy::_obstacle_id_type arg)
  {
    msg_.obstacle_id = std::move(arg);
    return Init_ObstacleProxy_shape(msg_);
  }

private:
  ::appleproj_interfaces::msg::ObstacleProxy msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::ObstacleProxy>()
{
  return appleproj_interfaces::msg::builder::Init_ObstacleProxy_obstacle_id();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__BUILDER_HPP_
