// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:srv/GetPlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/get_planning_scene.hpp"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/srv/detail/get_planning_scene__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::srv::GetPlanningScene_Request>()
{
  return ::appleproj_interfaces::srv::GetPlanningScene_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetPlanningScene_Response_message
{
public:
  explicit Init_GetPlanningScene_Response_message(::appleproj_interfaces::srv::GetPlanningScene_Response & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::srv::GetPlanningScene_Response message(::appleproj_interfaces::srv::GetPlanningScene_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::srv::GetPlanningScene_Response msg_;
};

class Init_GetPlanningScene_Response_scene
{
public:
  explicit Init_GetPlanningScene_Response_scene(::appleproj_interfaces::srv::GetPlanningScene_Response & msg)
  : msg_(msg)
  {}
  Init_GetPlanningScene_Response_message scene(::appleproj_interfaces::srv::GetPlanningScene_Response::_scene_type arg)
  {
    msg_.scene = std::move(arg);
    return Init_GetPlanningScene_Response_message(msg_);
  }

private:
  ::appleproj_interfaces::srv::GetPlanningScene_Response msg_;
};

class Init_GetPlanningScene_Response_success
{
public:
  Init_GetPlanningScene_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetPlanningScene_Response_scene success(::appleproj_interfaces::srv::GetPlanningScene_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetPlanningScene_Response_scene(msg_);
  }

private:
  ::appleproj_interfaces::srv::GetPlanningScene_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::srv::GetPlanningScene_Response>()
{
  return appleproj_interfaces::srv::builder::Init_GetPlanningScene_Response_success();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetPlanningScene_Event_response
{
public:
  explicit Init_GetPlanningScene_Event_response(::appleproj_interfaces::srv::GetPlanningScene_Event & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::srv::GetPlanningScene_Event response(::appleproj_interfaces::srv::GetPlanningScene_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::srv::GetPlanningScene_Event msg_;
};

class Init_GetPlanningScene_Event_request
{
public:
  explicit Init_GetPlanningScene_Event_request(::appleproj_interfaces::srv::GetPlanningScene_Event & msg)
  : msg_(msg)
  {}
  Init_GetPlanningScene_Event_response request(::appleproj_interfaces::srv::GetPlanningScene_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GetPlanningScene_Event_response(msg_);
  }

private:
  ::appleproj_interfaces::srv::GetPlanningScene_Event msg_;
};

class Init_GetPlanningScene_Event_info
{
public:
  Init_GetPlanningScene_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetPlanningScene_Event_request info(::appleproj_interfaces::srv::GetPlanningScene_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GetPlanningScene_Event_request(msg_);
  }

private:
  ::appleproj_interfaces::srv::GetPlanningScene_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::srv::GetPlanningScene_Event>()
{
  return appleproj_interfaces::srv::builder::Init_GetPlanningScene_Event_info();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__BUILDER_HPP_
