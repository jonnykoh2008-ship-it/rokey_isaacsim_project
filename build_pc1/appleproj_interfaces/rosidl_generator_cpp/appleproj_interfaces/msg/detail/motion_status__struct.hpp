// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/MotionStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/motion_status.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__STRUCT_HPP_

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
# define DEPRECATED__appleproj_interfaces__msg__MotionStatus __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__MotionStatus __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotionStatus_
{
  using Type = MotionStatus_<ContainerAllocator>;

  explicit MotionStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_state = "";
      this->success = false;
      this->progress = 0.0f;
      this->error_code = "";
      this->message = "";
    }
  }

  explicit MotionStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    current_state(_alloc),
    error_code(_alloc),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_state = "";
      this->success = false;
      this->progress = 0.0f;
      this->error_code = "";
      this->message = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _current_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_state_type current_state;
  using _success_type =
    bool;
  _success_type success;
  using _progress_type =
    float;
  _progress_type progress;
  using _error_code_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_code_type error_code;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__current_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_state = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__progress(
    const float & _arg)
  {
    this->progress = _arg;
    return *this;
  }
  Type & set__error_code(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error_code = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::MotionStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::MotionStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::MotionStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::MotionStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__MotionStatus
    std::shared_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__MotionStatus
    std::shared_ptr<appleproj_interfaces::msg::MotionStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotionStatus_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->current_state != other.current_state) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    if (this->progress != other.progress) {
      return false;
    }
    if (this->error_code != other.error_code) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotionStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotionStatus_

// alias to use template instance with default allocator
using MotionStatus =
  appleproj_interfaces::msg::MotionStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__MOTION_STATUS__STRUCT_HPP_
