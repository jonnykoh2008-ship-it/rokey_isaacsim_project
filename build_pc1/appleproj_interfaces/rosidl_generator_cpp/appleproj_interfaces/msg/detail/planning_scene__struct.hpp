// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/planning_scene.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'robot_base_pose'
// Member 'robot_tcp_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"
// Member 'obstacles'
#include "appleproj_interfaces/msg/detail/obstacle_proxy__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__msg__PlanningScene __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__PlanningScene __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PlanningScene_
{
  using Type = PlanningScene_<ContainerAllocator>;

  explicit PlanningScene_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    robot_base_pose(_init),
    robot_tcp_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reset_id = 0ull;
      this->scene_version = 0ull;
    }
  }

  explicit PlanningScene_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    robot_base_pose(_alloc, _init),
    robot_tcp_pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reset_id = 0ull;
      this->scene_version = 0ull;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _reset_id_type =
    uint64_t;
  _reset_id_type reset_id;
  using _scene_version_type =
    uint64_t;
  _scene_version_type scene_version;
  using _robot_base_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _robot_base_pose_type robot_base_pose;
  using _robot_tcp_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _robot_tcp_pose_type robot_tcp_pose;
  using _obstacles_type =
    std::vector<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>>;
  _obstacles_type obstacles;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__reset_id(
    const uint64_t & _arg)
  {
    this->reset_id = _arg;
    return *this;
  }
  Type & set__scene_version(
    const uint64_t & _arg)
  {
    this->scene_version = _arg;
    return *this;
  }
  Type & set__robot_base_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->robot_base_pose = _arg;
    return *this;
  }
  Type & set__robot_tcp_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->robot_tcp_pose = _arg;
    return *this;
  }
  Type & set__obstacles(
    const std::vector<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>> & _arg)
  {
    this->obstacles = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::PlanningScene_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::PlanningScene_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::PlanningScene_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::PlanningScene_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__PlanningScene
    std::shared_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__PlanningScene
    std::shared_ptr<appleproj_interfaces::msg::PlanningScene_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlanningScene_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->reset_id != other.reset_id) {
      return false;
    }
    if (this->scene_version != other.scene_version) {
      return false;
    }
    if (this->robot_base_pose != other.robot_base_pose) {
      return false;
    }
    if (this->robot_tcp_pose != other.robot_tcp_pose) {
      return false;
    }
    if (this->obstacles != other.obstacles) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlanningScene_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlanningScene_

// alias to use template instance with default allocator
using PlanningScene =
  appleproj_interfaces::msg::PlanningScene_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__PLANNING_SCENE__STRUCT_HPP_
