// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/CheckpointEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/checkpoint_event.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__STRUCT_HPP_

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

#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__msg__CheckpointEvent __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__CheckpointEvent __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CheckpointEvent_
{
  using Type = CheckpointEvent_<ContainerAllocator>;

  explicit CheckpointEvent_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->apple_id = "";
      this->checkpoint_id = "";
      this->event = 0;
    }
  }

  explicit CheckpointEvent_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    apple_id(_alloc),
    checkpoint_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->apple_id = "";
      this->checkpoint_id = "";
      this->event = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _apple_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _apple_id_type apple_id;
  using _checkpoint_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _checkpoint_id_type checkpoint_id;
  using _event_type =
    uint8_t;
  _event_type event;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__apple_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->apple_id = _arg;
    return *this;
  }
  Type & set__checkpoint_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->checkpoint_id = _arg;
    return *this;
  }
  Type & set__event(
    const uint8_t & _arg)
  {
    this->event = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t ENTER =
    1u;
  static constexpr uint8_t EXIT =
    2u;

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__CheckpointEvent
    std::shared_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__CheckpointEvent
    std::shared_ptr<appleproj_interfaces::msg::CheckpointEvent_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CheckpointEvent_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->apple_id != other.apple_id) {
      return false;
    }
    if (this->checkpoint_id != other.checkpoint_id) {
      return false;
    }
    if (this->event != other.event) {
      return false;
    }
    return true;
  }
  bool operator!=(const CheckpointEvent_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CheckpointEvent_

// alias to use template instance with default allocator
using CheckpointEvent =
  appleproj_interfaces::msg::CheckpointEvent_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CheckpointEvent_<ContainerAllocator>::ENTER;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CheckpointEvent_<ContainerAllocator>::EXIT;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__CHECKPOINT_EVENT__STRUCT_HPP_
