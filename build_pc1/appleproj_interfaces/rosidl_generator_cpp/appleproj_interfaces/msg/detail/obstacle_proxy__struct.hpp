// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/ObstacleProxy.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/obstacle_proxy.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"
// Member 'dimensions'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__msg__ObstacleProxy __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__ObstacleProxy __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObstacleProxy_
{
  using Type = ObstacleProxy_<ContainerAllocator>;

  explicit ObstacleProxy_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_init),
    dimensions(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->obstacle_id = "";
      this->shape = 0;
      this->obstacle_class = 0;
      this->safety_margin = 0.0;
    }
  }

  explicit ObstacleProxy_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : obstacle_id(_alloc),
    pose(_alloc, _init),
    dimensions(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->obstacle_id = "";
      this->shape = 0;
      this->obstacle_class = 0;
      this->safety_margin = 0.0;
    }
  }

  // field types and members
  using _obstacle_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _obstacle_id_type obstacle_id;
  using _shape_type =
    uint8_t;
  _shape_type shape;
  using _obstacle_class_type =
    uint8_t;
  _obstacle_class_type obstacle_class;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _dimensions_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _dimensions_type dimensions;
  using _safety_margin_type =
    double;
  _safety_margin_type safety_margin;

  // setters for named parameter idiom
  Type & set__obstacle_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->obstacle_id = _arg;
    return *this;
  }
  Type & set__shape(
    const uint8_t & _arg)
  {
    this->shape = _arg;
    return *this;
  }
  Type & set__obstacle_class(
    const uint8_t & _arg)
  {
    this->obstacle_class = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__dimensions(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->dimensions = _arg;
    return *this;
  }
  Type & set__safety_margin(
    const double & _arg)
  {
    this->safety_margin = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t SHAPE_SPHERE =
    1u;
  static constexpr uint8_t SHAPE_BOX =
    2u;
  static constexpr uint8_t SHAPE_CAPSULE =
    3u;
  static constexpr uint8_t CLASS_TRUNK =
    1u;
  static constexpr uint8_t CLASS_BRANCH =
    2u;

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__ObstacleProxy
    std::shared_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__ObstacleProxy
    std::shared_ptr<appleproj_interfaces::msg::ObstacleProxy_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObstacleProxy_ & other) const
  {
    if (this->obstacle_id != other.obstacle_id) {
      return false;
    }
    if (this->shape != other.shape) {
      return false;
    }
    if (this->obstacle_class != other.obstacle_class) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->dimensions != other.dimensions) {
      return false;
    }
    if (this->safety_margin != other.safety_margin) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObstacleProxy_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObstacleProxy_

// alias to use template instance with default allocator
using ObstacleProxy =
  appleproj_interfaces::msg::ObstacleProxy_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObstacleProxy_<ContainerAllocator>::SHAPE_SPHERE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObstacleProxy_<ContainerAllocator>::SHAPE_BOX;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObstacleProxy_<ContainerAllocator>::SHAPE_CAPSULE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObstacleProxy_<ContainerAllocator>::CLASS_TRUNK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ObstacleProxy_<ContainerAllocator>::CLASS_BRANCH;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__OBSTACLE_PROXY__STRUCT_HPP_
