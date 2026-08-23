// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/planning_scene.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/msg/detail/planning_scene__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace msg
{

namespace builder
{

class Init_PlanningScene_obstacles
{
public:
  explicit Init_PlanningScene_obstacles(::appleproj_interfaces::msg::PlanningScene & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::msg::PlanningScene obstacles(::appleproj_interfaces::msg::PlanningScene::_obstacles_type arg)
  {
    msg_.obstacles = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::msg::PlanningScene msg_;
};

class Init_PlanningScene_robot_tcp_pose
{
public:
  explicit Init_PlanningScene_robot_tcp_pose(::appleproj_interfaces::msg::PlanningScene & msg)
  : msg_(msg)
  {}
  Init_PlanningScene_obstacles robot_tcp_pose(::appleproj_interfaces::msg::PlanningScene::_robot_tcp_pose_type arg)
  {
    msg_.robot_tcp_pose = std::move(arg);
    return Init_PlanningScene_obstacles(msg_);
  }

private:
  ::appleproj_interfaces::msg::PlanningScene msg_;
};

class Init_PlanningScene_robot_base_pose
{
public:
  explicit Init_PlanningScene_robot_base_pose(::appleproj_interfaces::msg::PlanningScene & msg)
  : msg_(msg)
  {}
  Init_PlanningScene_robot_tcp_pose robot_base_pose(::appleproj_interfaces::msg::PlanningScene::_robot_base_pose_type arg)
  {
    msg_.robot_base_pose = std::move(arg);
    return Init_PlanningScene_robot_tcp_pose(msg_);
  }

private:
  ::appleproj_interfaces::msg::PlanningScene msg_;
};

class Init_PlanningScene_scene_version
{
public:
  explicit Init_PlanningScene_scene_version(::appleproj_interfaces::msg::PlanningScene & msg)
  : msg_(msg)
  {}
  Init_PlanningScene_robot_base_pose scene_version(::appleproj_interfaces::msg::PlanningScene::_scene_version_type arg)
  {
    msg_.scene_version = std::move(arg);
    return Init_PlanningScene_robot_base_pose(msg_);
  }

private:
  ::appleproj_interfaces::msg::PlanningScene msg_;
};

class Init_PlanningScene_reset_id
{
public:
  explicit Init_PlanningScene_reset_id(::appleproj_interfaces::msg::PlanningScene & msg)
  : msg_(msg)
  {}
  Init_PlanningScene_scene_version reset_id(::appleproj_interfaces::msg::PlanningScene::_reset_id_type arg)
  {
    msg_.reset_id = std::move(arg);
    return Init_PlanningScene_scene_version(msg_);
  }

private:
  ::appleproj_interfaces::msg::PlanningScene msg_;
};

class Init_PlanningScene_header
{
public:
  Init_PlanningScene_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanningScene_reset_id header(::appleproj_interfaces::msg::PlanningScene::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_PlanningScene_reset_id(msg_);
  }

private:
  ::appleproj_interfaces::msg::PlanningScene msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::msg::PlanningScene>()
{
  return appleproj_interfaces::msg::builder::Init_PlanningScene_header();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__BUILDER_HPP_
