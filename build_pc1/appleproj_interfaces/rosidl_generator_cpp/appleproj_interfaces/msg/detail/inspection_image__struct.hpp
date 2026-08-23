// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:msg/InspectionImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/msg/inspection_image.hpp"


#ifndef APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__STRUCT_HPP_

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
// Member 'image'
#include "sensor_msgs/msg/detail/compressed_image__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__msg__InspectionImage __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__msg__InspectionImage __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct InspectionImage_
{
  using Type = InspectionImage_<ContainerAllocator>;

  explicit InspectionImage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    image(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->apple_id = "";
      this->frame_index = 0;
      this->total_frames = 0;
    }
  }

  explicit InspectionImage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    inspection_id(_alloc),
    apple_id(_alloc),
    image(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->apple_id = "";
      this->frame_index = 0;
      this->total_frames = 0;
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
  using _frame_index_type =
    uint16_t;
  _frame_index_type frame_index;
  using _total_frames_type =
    uint16_t;
  _total_frames_type total_frames;
  using _image_type =
    sensor_msgs::msg::CompressedImage_<ContainerAllocator>;
  _image_type image;

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
  Type & set__frame_index(
    const uint16_t & _arg)
  {
    this->frame_index = _arg;
    return *this;
  }
  Type & set__total_frames(
    const uint16_t & _arg)
  {
    this->total_frames = _arg;
    return *this;
  }
  Type & set__image(
    const sensor_msgs::msg::CompressedImage_<ContainerAllocator> & _arg)
  {
    this->image = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    appleproj_interfaces::msg::InspectionImage_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::msg::InspectionImage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::InspectionImage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::msg::InspectionImage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__msg__InspectionImage
    std::shared_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__msg__InspectionImage
    std::shared_ptr<appleproj_interfaces::msg::InspectionImage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const InspectionImage_ & other) const
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
    if (this->frame_index != other.frame_index) {
      return false;
    }
    if (this->total_frames != other.total_frames) {
      return false;
    }
    if (this->image != other.image) {
      return false;
    }
    return true;
  }
  bool operator!=(const InspectionImage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct InspectionImage_

// alias to use template instance with default allocator
using InspectionImage =
  appleproj_interfaces::msg::InspectionImage_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__MSG__DETAIL__INSPECTION_IMAGE__STRUCT_HPP_
