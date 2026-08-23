// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from appleproj_interfaces:srv/RetryInspection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/retry_inspection.hpp"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__STRUCT_HPP_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__srv__RetryInspection_Request __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__srv__RetryInspection_Request __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct RetryInspection_Request_
{
  using Type = RetryInspection_Request_<ContainerAllocator>;

  explicit RetryInspection_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->apple_id = "";
      this->reason = "";
    }
  }

  explicit RetryInspection_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : inspection_id(_alloc),
    apple_id(_alloc),
    reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->apple_id = "";
      this->reason = "";
    }
  }

  // field types and members
  using _inspection_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _inspection_id_type inspection_id;
  using _apple_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _apple_id_type apple_id;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;

  // setters for named parameter idiom
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
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__srv__RetryInspection_Request
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__srv__RetryInspection_Request
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RetryInspection_Request_ & other) const
  {
    if (this->inspection_id != other.inspection_id) {
      return false;
    }
    if (this->apple_id != other.apple_id) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const RetryInspection_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RetryInspection_Request_

// alias to use template instance with default allocator
using RetryInspection_Request =
  appleproj_interfaces::srv::RetryInspection_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace appleproj_interfaces


#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__srv__RetryInspection_Response __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__srv__RetryInspection_Response __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct RetryInspection_Response_
{
  using Type = RetryInspection_Response_<ContainerAllocator>;

  explicit RetryInspection_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
      this->new_inspection_id = "";
      this->message = "";
    }
  }

  explicit RetryInspection_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : new_inspection_id(_alloc),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
      this->new_inspection_id = "";
      this->message = "";
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _new_inspection_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _new_inspection_id_type new_inspection_id;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__new_inspection_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->new_inspection_id = _arg;
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
    appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__srv__RetryInspection_Response
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__srv__RetryInspection_Response
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RetryInspection_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->new_inspection_id != other.new_inspection_id) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const RetryInspection_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RetryInspection_Response_

// alias to use template instance with default allocator
using RetryInspection_Response =
  appleproj_interfaces::srv::RetryInspection_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace appleproj_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__appleproj_interfaces__srv__RetryInspection_Event __attribute__((deprecated))
#else
# define DEPRECATED__appleproj_interfaces__srv__RetryInspection_Event __declspec(deprecated)
#endif

namespace appleproj_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct RetryInspection_Event_
{
  using Type = RetryInspection_Event_<ContainerAllocator>;

  explicit RetryInspection_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit RetryInspection_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<appleproj_interfaces::srv::RetryInspection_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<appleproj_interfaces::srv::RetryInspection_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__appleproj_interfaces__srv__RetryInspection_Event
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__appleproj_interfaces__srv__RetryInspection_Event
    std::shared_ptr<appleproj_interfaces::srv::RetryInspection_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RetryInspection_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const RetryInspection_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RetryInspection_Event_

// alias to use template instance with default allocator
using RetryInspection_Event =
  appleproj_interfaces::srv::RetryInspection_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace appleproj_interfaces

namespace appleproj_interfaces
{

namespace srv
{

struct RetryInspection
{
  using Request = appleproj_interfaces::srv::RetryInspection_Request;
  using Response = appleproj_interfaces::srv::RetryInspection_Response;
  using Event = appleproj_interfaces::srv::RetryInspection_Event;
};

}  // namespace srv

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__STRUCT_HPP_
