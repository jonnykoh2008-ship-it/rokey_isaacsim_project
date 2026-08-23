
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to appleproj_interfaces__action__RobotMotion_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_type: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reset_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene_version: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoints: Vec<geometry_msgs::msg::PoseStamped>,

}

impl RobotMotion_Goal {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const APPROACH: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const GRASP: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TWIST: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PULL: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TRANSPORT: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PLACE: u8 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RETRACT: u8 = 7;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RELEASE: u8 = 8;

}


impl Default for RobotMotion_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_Goal {
  type RmwMsg = super::action::rmw::RobotMotion_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        motion_type: msg.motion_type,
        target_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.target_pose)).into_owned(),
        reset_id: msg.reset_id,
        scene_version: msg.scene_version,
        waypoints: msg.waypoints
          .into_iter()
          .map(|elem| geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      motion_type: msg.motion_type,
        target_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.target_pose)).into_owned(),
      reset_id: msg.reset_id,
      scene_version: msg.scene_version,
        waypoints: msg.waypoints
          .iter()
          .map(|elem| geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      motion_type: msg.motion_type,
      target_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.target_pose),
      reset_id: msg.reset_id,
      scene_version: msg.scene_version,
      waypoints: msg.waypoints
          .into_iter()
          .map(geometry_msgs::msg::PoseStamped::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to appleproj_interfaces__action__RobotMotion_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for RobotMotion_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_Result::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_Result {
  type RmwMsg = super::action::rmw::RobotMotion_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        error_code: msg.error_code.as_str().into(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        error_code: msg.error_code.as_str().into(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      error_code: msg.error_code.to_string(),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to appleproj_interfaces__action__RobotMotion_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub progress: f32,

}



impl Default for RobotMotion_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_Feedback {
  type RmwMsg = super::action::rmw::RobotMotion_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        current_state: msg.current_state.as_str().into(),
        progress: msg.progress,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        current_state: msg.current_state.as_str().into(),
      progress: msg.progress,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      current_state: msg.current_state.to_string(),
      progress: msg.progress,
    }
  }
}


// Corresponds to appleproj_interfaces__action__RobotMotion_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::RobotMotion_Feedback,

}



impl Default for RobotMotion_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_FeedbackMessage {
  type RmwMsg = super::action::rmw::RobotMotion_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::RobotMotion_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::RobotMotion_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::RobotMotion_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to appleproj_interfaces__action__RobotMotion_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::RobotMotion_Goal,

}



impl Default for RobotMotion_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_SendGoal_Request {
  type RmwMsg = super::action::rmw::RobotMotion_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::RobotMotion_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::RobotMotion_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::RobotMotion_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to appleproj_interfaces__action__RobotMotion_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for RobotMotion_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_SendGoal_Response {
  type RmwMsg = super::action::rmw::RobotMotion_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to appleproj_interfaces__action__RobotMotion_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for RobotMotion_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_GetResult_Request {
  type RmwMsg = super::action::rmw::RobotMotion_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to appleproj_interfaces__action__RobotMotion_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::RobotMotion_Result,

}



impl Default for RobotMotion_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RobotMotion_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_GetResult_Response {
  type RmwMsg = super::action::rmw::RobotMotion_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::RobotMotion_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::RobotMotion_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::RobotMotion_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__action__RobotMotion_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct RobotMotion_SendGoal;

impl rosidl_runtime_rs::Service for RobotMotion_SendGoal {
    type Request = RobotMotion_SendGoal_Request;
    type Response = RobotMotion_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__action__RobotMotion_SendGoal() }
    }
}




#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__action__RobotMotion_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct RobotMotion_GetResult;

impl rosidl_runtime_rs::Service for RobotMotion_GetResult {
    type Request = RobotMotion_GetResult_Request;
    type Response = RobotMotion_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__action__RobotMotion_GetResult() }
    }
}






#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__appleproj_interfaces__action__RobotMotion() -> *const std::ffi::c_void;
}

// Corresponds to appleproj_interfaces__action__RobotMotion
#[allow(missing_docs, non_camel_case_types)]
pub struct RobotMotion;

impl rosidl_runtime_rs::Action for RobotMotion {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = RobotMotion_Goal;

  /// The result message defined in the action definition.
  type Result = RobotMotion_Result;

  /// The feedback message defined in the action definition.
  type Feedback = RobotMotion_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::RobotMotion_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::RobotMotion_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::RobotMotion_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__appleproj_interfaces__action__RobotMotion() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::RobotMotion_Goal,
  ) -> super::action::rmw::RobotMotion_SendGoal_Request {
   super::action::rmw::RobotMotion_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::RobotMotion_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::RobotMotion_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::RobotMotion_SendGoal_Response {
   super::action::rmw::RobotMotion_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::RobotMotion_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::RobotMotion_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::RobotMotion_Feedback,
  ) -> super::action::rmw::RobotMotion_FeedbackMessage {
    let mut message = super::action::rmw::RobotMotion_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::RobotMotion_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::RobotMotion_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::RobotMotion_GetResult_Request {
   super::action::rmw::RobotMotion_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::RobotMotion_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::RobotMotion_Result,
  ) -> super::action::rmw::RobotMotion_GetResult_Response {
   super::action::rmw::RobotMotion_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::RobotMotion_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::RobotMotion_Result,
  ) {
    (response.status, response.result)
  }
}


