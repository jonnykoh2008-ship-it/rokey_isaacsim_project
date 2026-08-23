// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/SimulationState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/simulation_state.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__STRUCT_HPP_

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
# define DEPRECATED__appleproj_interfaces__msg__SimulationState __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__SimulationState __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SimulationState_
{
  using Type = SimulationState_<ContainerAllocator>;

  explicit SimulationState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0;
      this->reset_id = 0ull;
      this->scene_version = 0ull;
      this->message = "";
    }
  }

  explicit SimulationState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0;
      this->reset_id = 0ull;
      this->scene_version = 0ull;
      this->message = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _state_type =
    uint8_t;
  _state_type state;
  using _reset_id_type =
    uint64_t;
  _reset_id_type reset_id;
  using _scene_version_type =
    uint64_t;
  _scene_version_type scene_version;
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
  Type & set__state(
    const uint8_t & _arg)
  {
    this->state = _arg;
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
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t STOPPED =
    0u;
  static constexpr uint8_t INITIALIZING =
    1u;
  static constexpr uint8_t READY =
    2u;
  static constexpr uint8_t PLAYING =
    3u;
  static constexpr uint8_t PAUSED =
    4u;

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::SimulationState_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::SimulationState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::SimulationState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::SimulationState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__SimulationState
    std::shared_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__SimulationState
    std::shared_ptr<appleproj_interfaces::msg::SimulationState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SimulationState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->state != other.state) {
      return false;
    }
    if (this->reset_id != other.reset_id) {
      return false;
    }
    if (this->scene_version != other.scene_version) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const SimulationState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SimulationState_

// alias to use template instance with default allocator
using SimulationState =
  appleproj_interfaces::msg::SimulationState_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t SimulationState_<ContainerAllocator>::STOPPED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t SimulationState_<ContainerAllocator>::INITIALIZING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t SimulationState_<ContainerAllocator>::READY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t SimulationState_<ContainerAllocator>::PLAYING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t SimulationState_<ContainerAllocator>::PAUSED;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__SIMULATION_STATE__STRUCT_HPP_
