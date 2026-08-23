// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from appleproj_interfaces:action/RobotMotion.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/action/robot_motion.hpp"


#ifndef APPLEPROJ_INTERFACES__ACTION__DETAIL__ROBOT_MOTION__BUILDER_HPP_
#define APPLEPROJ_INTERFACES__ACTION__DETAIL__ROBOT_MOTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "appleproj_interfaces/action/detail/robot_motion__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_Goal_waypoints
{
public:
  explicit Init_RobotMotion_Goal_waypoints(::appleproj_interfaces::action::RobotMotion_Goal & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_Goal waypoints(::appleproj_interfaces::action::RobotMotion_Goal::_waypoints_type arg)
  {
    msg_.waypoints = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Goal msg_;
};

class Init_RobotMotion_Goal_scene_version
{
public:
  explicit Init_RobotMotion_Goal_scene_version(::appleproj_interfaces::action::RobotMotion_Goal & msg)
  : msg_(msg)
  {}
  Init_RobotMotion_Goal_waypoints scene_version(::appleproj_interfaces::action::RobotMotion_Goal::_scene_version_type arg)
  {
    msg_.scene_version = std::move(arg);
    return Init_RobotMotion_Goal_waypoints(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Goal msg_;
};

class Init_RobotMotion_Goal_reset_id
{
public:
  explicit Init_RobotMotion_Goal_reset_id(::appleproj_interfaces::action::RobotMotion_Goal & msg)
  : msg_(msg)
  {}
  Init_RobotMotion_Goal_scene_version reset_id(::appleproj_interfaces::action::RobotMotion_Goal::_reset_id_type arg)
  {
    msg_.reset_id = std::move(arg);
    return Init_RobotMotion_Goal_scene_version(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Goal msg_;
};

class Init_RobotMotion_Goal_target_pose
{
public:
  explicit Init_RobotMotion_Goal_target_pose(::appleproj_interfaces::action::RobotMotion_Goal & msg)
  : msg_(msg)
  {}
  Init_RobotMotion_Goal_reset_id target_pose(::appleproj_interfaces::action::RobotMotion_Goal::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return Init_RobotMotion_Goal_reset_id(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Goal msg_;
};

class Init_RobotMotion_Goal_motion_type
{
public:
  Init_RobotMotion_Goal_motion_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_Goal_target_pose motion_type(::appleproj_interfaces::action::RobotMotion_Goal::_motion_type_type arg)
  {
    msg_.motion_type = std::move(arg);
    return Init_RobotMotion_Goal_target_pose(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_Goal>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_Goal_motion_type();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_Result_message
{
public:
  explicit Init_RobotMotion_Result_message(::appleproj_interfaces::action::RobotMotion_Result & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_Result message(::appleproj_interfaces::action::RobotMotion_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Result msg_;
};

class Init_RobotMotion_Result_error_code
{
public:
  explicit Init_RobotMotion_Result_error_code(::appleproj_interfaces::action::RobotMotion_Result & msg)
  : msg_(msg)
  {}
  Init_RobotMotion_Result_message error_code(::appleproj_interfaces::action::RobotMotion_Result::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_RobotMotion_Result_message(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Result msg_;
};

class Init_RobotMotion_Result_success
{
public:
  Init_RobotMotion_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_Result_error_code success(::appleproj_interfaces::action::RobotMotion_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_RobotMotion_Result_error_code(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_Result>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_Result_success();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_Feedback_progress
{
public:
  explicit Init_RobotMotion_Feedback_progress(::appleproj_interfaces::action::RobotMotion_Feedback & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_Feedback progress(::appleproj_interfaces::action::RobotMotion_Feedback::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Feedback msg_;
};

class Init_RobotMotion_Feedback_current_state
{
public:
  Init_RobotMotion_Feedback_current_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_Feedback_progress current_state(::appleproj_interfaces::action::RobotMotion_Feedback::_current_state_type arg)
  {
    msg_.current_state = std::move(arg);
    return Init_RobotMotion_Feedback_progress(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_Feedback>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_Feedback_current_state();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_SendGoal_Request_goal
{
public:
  explicit Init_RobotMotion_SendGoal_Request_goal(::appleproj_interfaces::action::RobotMotion_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Request goal(::appleproj_interfaces::action::RobotMotion_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Request msg_;
};

class Init_RobotMotion_SendGoal_Request_goal_id
{
public:
  Init_RobotMotion_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_SendGoal_Request_goal goal_id(::appleproj_interfaces::action::RobotMotion_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_RobotMotion_SendGoal_Request_goal(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_SendGoal_Request>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_SendGoal_Request_goal_id();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_SendGoal_Response_stamp
{
public:
  explicit Init_RobotMotion_SendGoal_Response_stamp(::appleproj_interfaces::action::RobotMotion_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Response stamp(::appleproj_interfaces::action::RobotMotion_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Response msg_;
};

class Init_RobotMotion_SendGoal_Response_accepted
{
public:
  Init_RobotMotion_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_SendGoal_Response_stamp accepted(::appleproj_interfaces::action::RobotMotion_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_RobotMotion_SendGoal_Response_stamp(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_SendGoal_Response>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_SendGoal_Response_accepted();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_SendGoal_Event_response
{
public:
  explicit Init_RobotMotion_SendGoal_Event_response(::appleproj_interfaces::action::RobotMotion_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Event response(::appleproj_interfaces::action::RobotMotion_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Event msg_;
};

class Init_RobotMotion_SendGoal_Event_request
{
public:
  explicit Init_RobotMotion_SendGoal_Event_request(::appleproj_interfaces::action::RobotMotion_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_RobotMotion_SendGoal_Event_response request(::appleproj_interfaces::action::RobotMotion_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_RobotMotion_SendGoal_Event_response(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Event msg_;
};

class Init_RobotMotion_SendGoal_Event_info
{
public:
  Init_RobotMotion_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_SendGoal_Event_request info(::appleproj_interfaces::action::RobotMotion_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_RobotMotion_SendGoal_Event_request(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_SendGoal_Event>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_SendGoal_Event_info();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_GetResult_Request_goal_id
{
public:
  Init_RobotMotion_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::appleproj_interfaces::action::RobotMotion_GetResult_Request goal_id(::appleproj_interfaces::action::RobotMotion_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_GetResult_Request>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_GetResult_Request_goal_id();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_GetResult_Response_result
{
public:
  explicit Init_RobotMotion_GetResult_Response_result(::appleproj_interfaces::action::RobotMotion_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_GetResult_Response result(::appleproj_interfaces::action::RobotMotion_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_GetResult_Response msg_;
};

class Init_RobotMotion_GetResult_Response_status
{
public:
  Init_RobotMotion_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_GetResult_Response_result status(::appleproj_interfaces::action::RobotMotion_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_RobotMotion_GetResult_Response_result(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_GetResult_Response>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_GetResult_Response_status();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_GetResult_Event_response
{
public:
  explicit Init_RobotMotion_GetResult_Event_response(::appleproj_interfaces::action::RobotMotion_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_GetResult_Event response(::appleproj_interfaces::action::RobotMotion_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_GetResult_Event msg_;
};

class Init_RobotMotion_GetResult_Event_request
{
public:
  explicit Init_RobotMotion_GetResult_Event_request(::appleproj_interfaces::action::RobotMotion_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_RobotMotion_GetResult_Event_response request(::appleproj_interfaces::action::RobotMotion_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_RobotMotion_GetResult_Event_response(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_GetResult_Event msg_;
};

class Init_RobotMotion_GetResult_Event_info
{
public:
  Init_RobotMotion_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_GetResult_Event_request info(::appleproj_interfaces::action::RobotMotion_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_RobotMotion_GetResult_Event_request(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_GetResult_Event>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_GetResult_Event_info();
}

}  // namespace appleproj_interfaces


namespace appleproj_interfaces
{

namespace action
{

namespace builder
{

class Init_RobotMotion_FeedbackMessage_feedback
{
public:
  explicit Init_RobotMotion_FeedbackMessage_feedback(::appleproj_interfaces::action::RobotMotion_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::appleproj_interfaces::action::RobotMotion_FeedbackMessage feedback(::appleproj_interfaces::action::RobotMotion_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_FeedbackMessage msg_;
};

class Init_RobotMotion_FeedbackMessage_goal_id
{
public:
  Init_RobotMotion_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotMotion_FeedbackMessage_feedback goal_id(::appleproj_interfaces::action::RobotMotion_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_RobotMotion_FeedbackMessage_feedback(msg_);
  }

private:
  ::appleproj_interfaces::action::RobotMotion_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::appleproj_interfaces::action::RobotMotion_FeedbackMessage>()
{
  return appleproj_interfaces::action::builder::Init_RobotMotion_FeedbackMessage_goal_id();
}

}  // namespace appleproj_interfaces

#endif  // APPLEPROJ_INTERFACES__ACTION__DETAIL__ROBOT_MOTION__BUILDER_HPP_
