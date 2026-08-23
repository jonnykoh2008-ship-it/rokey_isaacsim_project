// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:srv/RetryInspection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/retry_inspection.hpp"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/srv/detail/retry_inspection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace srv
{

namespace builder
{

class Init_RetryInspection_Request_reason
{
public:
  explicit Init_RetryInspection_Request_reason(::appleproj_interfaces::srv::RetryInspection_Request & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::srv::RetryInspection_Request reason(::appleproj_interfaces::srv::RetryInspection_Request::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Request msg_;
};

class Init_RetryInspection_Request_apple_id
{
public:
  explicit Init_RetryInspection_Request_apple_id(::appleproj_interfaces::srv::RetryInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RetryInspection_Request_reason apple_id(::appleproj_interfaces::srv::RetryInspection_Request::_apple_id_type arg)
  {
    msg_.apple_id = std::move(arg);
    return Init_RetryInspection_Request_reason(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Request msg_;
};

class Init_RetryInspection_Request_inspection_id
{
public:
  Init_RetryInspection_Request_inspection_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RetryInspection_Request_apple_id inspection_id(::appleproj_interfaces::srv::RetryInspection_Request::_inspection_id_type arg)
  {
    msg_.inspection_id = std::move(arg);
    return Init_RetryInspection_Request_apple_id(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::srv::RetryInspection_Request>()
{
  return appleproj_interfaces::srv::builder::Init_RetryInspection_Request_inspection_id();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace srv
{

namespace builder
{

class Init_RetryInspection_Response_message
{
public:
  explicit Init_RetryInspection_Response_message(::appleproj_interfaces::srv::RetryInspection_Response & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::srv::RetryInspection_Response message(::appleproj_interfaces::srv::RetryInspection_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Response msg_;
};

class Init_RetryInspection_Response_new_inspection_id
{
public:
  explicit Init_RetryInspection_Response_new_inspection_id(::appleproj_interfaces::srv::RetryInspection_Response & msg)
  : msg_(msg)
  {}
  Init_RetryInspection_Response_message new_inspection_id(::appleproj_interfaces::srv::RetryInspection_Response::_new_inspection_id_type arg)
  {
    msg_.new_inspection_id = std::move(arg);
    return Init_RetryInspection_Response_message(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Response msg_;
};

class Init_RetryInspection_Response_accepted
{
public:
  Init_RetryInspection_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RetryInspection_Response_new_inspection_id accepted(::appleproj_interfaces::srv::RetryInspection_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_RetryInspection_Response_new_inspection_id(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::srv::RetryInspection_Response>()
{
  return appleproj_interfaces::srv::builder::Init_RetryInspection_Response_accepted();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace srv
{

namespace builder
{

class Init_RetryInspection_Event_response
{
public:
  explicit Init_RetryInspection_Event_response(::appleproj_interfaces::srv::RetryInspection_Event & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::srv::RetryInspection_Event response(::appleproj_interfaces::srv::RetryInspection_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Event msg_;
};

class Init_RetryInspection_Event_request
{
public:
  explicit Init_RetryInspection_Event_request(::appleproj_interfaces::srv::RetryInspection_Event & msg)
  : msg_(msg)
  {}
  Init_RetryInspection_Event_response request(::appleproj_interfaces::srv::RetryInspection_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_RetryInspection_Event_response(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Event msg_;
};

class Init_RetryInspection_Event_info
{
public:
  Init_RetryInspection_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RetryInspection_Event_request info(::appleproj_interfaces::srv::RetryInspection_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_RetryInspection_Event_request(msg_);
  }

private:
  ::appleproj_interfaces::srv::RetryInspection_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::srv::RetryInspection_Event>()
{
  return appleproj_interfaces::srv::builder::Init_RetryInspection_Event_info();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__BUILDER_HPP_
