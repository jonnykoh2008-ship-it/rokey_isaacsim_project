// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/quality_result.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__STRUCT_HPP_

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
// Member 'result_timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__msg__QualityResult __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__QualityResult __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct QualityResult_
{
  using Type = QualityResult_<ContainerAllocator>;

  explicit QualityResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    result_timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->apple_id = "";
      this->grade = 0;
      this->confidence = 0.0f;
      this->color_ratio = 0.0f;
      this->diameter_mm = 0.0f;
      this->damage_area_cm2 = 0.0f;
      this->frames_used = 0;
      this->status = 0;
    }
  }

  explicit QualityResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    inspection_id(_alloc),
    apple_id(_alloc),
    result_timestamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->apple_id = "";
      this->grade = 0;
      this->confidence = 0.0f;
      this->color_ratio = 0.0f;
      this->diameter_mm = 0.0f;
      this->damage_area_cm2 = 0.0f;
      this->frames_used = 0;
      this->status = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _inspection_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _inspection_id_type inspection_id;
  using _apple_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _apple_id_type apple_id;
  using _grade_type =
    uint8_t;
  _grade_type grade;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _color_ratio_type =
    float;
  _color_ratio_type color_ratio;
  using _diameter_mm_type =
    float;
  _diameter_mm_type diameter_mm;
  using _damage_area_cm2_type =
    float;
  _damage_area_cm2_type damage_area_cm2;
  using _frames_used_type =
    uint16_t;
  _frames_used_type frames_used;
  using _frame_indices_type =
    std::vector<uint16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint16_t>>;
  _frame_indices_type frame_indices;
  using _result_timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _result_timestamp_type result_timestamp;
  using _status_type =
    uint8_t;
  _status_type status;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__inspection_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->inspection_id = _arg;
    return *this;
  }
  Type & set__apple_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->apple_id = _arg;
    return *this;
  }
  Type & set__grade(
    const uint8_t & _arg)
  {
    this->grade = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__color_ratio(
    const float & _arg)
  {
    this->color_ratio = _arg;
    return *this;
  }
  Type & set__diameter_mm(
    const float & _arg)
  {
    this->diameter_mm = _arg;
    return *this;
  }
  Type & set__damage_area_cm2(
    const float & _arg)
  {
    this->damage_area_cm2 = _arg;
    return *this;
  }
  Type & set__frames_used(
    const uint16_t & _arg)
  {
    this->frames_used = _arg;
    return *this;
  }
  Type & set__frame_indices(
    const std::vector<uint16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint16_t>> & _arg)
  {
    this->frame_indices = _arg;
    return *this;
  }
  Type & set__result_timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->result_timestamp = _arg;
    return *this;
  }
  Type & set__status(
    const uint8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t HIGH =
    1u;
  static constexpr uint8_t MEDIUM =
    2u;
  static constexpr uint8_t LOW =
    3u;
  static constexpr uint8_t VALID =
    1u;
  static constexpr uint8_t RECHECK =
    2u;
  static constexpr uint8_t UNCLASSIFIED =
    3u;
  static constexpr uint8_t TIMEOUT =
    4u;
  static constexpr uint8_t LATE_RESULT =
    5u;
  static constexpr uint8_t ID_MISMATCH =
    6u;
  static constexpr uint8_t INSUFFICIENT_VIEWS =
    7u;

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::QualityResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::QualityResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::QualityResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::QualityResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__QualityResult
    std::shared_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__QualityResult
    std::shared_ptr<appleproj_interfaces::msg::QualityResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QualityResult_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->inspection_id != other.inspection_id) {
      return false;
    }
    if (this->apple_id != other.apple_id) {
      return false;
    }
    if (this->grade != other.grade) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->color_ratio != other.color_ratio) {
      return false;
    }
    if (this->diameter_mm != other.diameter_mm) {
      return false;
    }
    if (this->damage_area_cm2 != other.damage_area_cm2) {
      return false;
    }
    if (this->frames_used != other.frames_used) {
      return false;
    }
    if (this->frame_indices != other.frame_indices) {
      return false;
    }
    if (this->result_timestamp != other.result_timestamp) {
      return false;
    }
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const QualityResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QualityResult_

// alias to use template instance with default allocator
using QualityResult =
  appleproj_interfaces::msg::QualityResult_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::HIGH;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::MEDIUM;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::LOW;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::VALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::RECHECK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::UNCLASSIFIED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::TIMEOUT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::LATE_RESULT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::ID_MISMATCH;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t QualityResult_<ContainerAllocator>::INSUFFICIENT_VIEWS;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__QUALITY_RESULT__STRUCT_HPP_
