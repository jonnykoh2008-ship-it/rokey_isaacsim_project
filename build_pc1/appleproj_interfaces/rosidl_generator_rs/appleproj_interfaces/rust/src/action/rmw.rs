
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_Goal() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_Goal__init(msg: *mut RobotMotion_Goal) -> bool;
    fn appleproj_interfaces__action__RobotMotion_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Goal>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Goal>);
    fn appleproj_interfaces__action__RobotMotion_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Goal>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_type: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reset_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene_version: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub waypoints: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::PoseStamped>,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_Goal__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_Goal() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_Result() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_Result__init(msg: *mut RobotMotion_Result) -> bool;
    fn appleproj_interfaces__action__RobotMotion_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Result>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Result>);
    fn appleproj_interfaces__action__RobotMotion_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Result>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for RobotMotion_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_Result__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_Result where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_Result() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_Feedback__init(msg: *mut RobotMotion_Feedback) -> bool;
    fn appleproj_interfaces__action__RobotMotion_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Feedback>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Feedback>);
    fn appleproj_interfaces__action__RobotMotion_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_Feedback>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub progress: f32,

}



impl Default for RobotMotion_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_Feedback__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_Feedback() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_FeedbackMessage__init(msg: *mut RobotMotion_FeedbackMessage) -> bool;
    fn appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_FeedbackMessage>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_FeedbackMessage>);
    fn appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_FeedbackMessage>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::RobotMotion_Feedback,

}



impl Default for RobotMotion_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_FeedbackMessage() }
  }
}




#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Request__init(msg: *mut RobotMotion_SendGoal_Request) -> bool;
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Request>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Request>);
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Request>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::RobotMotion_Goal,

}



impl Default for RobotMotion_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_SendGoal_Request() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Response__init(msg: *mut RobotMotion_SendGoal_Response) -> bool;
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Response>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Response>);
    fn appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_SendGoal_Response>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for RobotMotion_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_SendGoal_Response() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_GetResult_Request__init(msg: *mut RobotMotion_GetResult_Request) -> bool;
    fn appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Request>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Request>);
    fn appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Request>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for RobotMotion_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_GetResult_Request() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__action__RobotMotion_GetResult_Response__init(msg: *mut RobotMotion_GetResult_Response) -> bool;
    fn appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Response>, size: usize) -> bool;
    fn appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Response>);
    fn appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMotion_GetResult_Response>) -> bool;
}

// Corresponds to appleproj_interfaces__action__RobotMotion_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMotion_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::RobotMotion_Result,

}



impl Default for RobotMotion_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__action__RobotMotion_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__action__RobotMotion_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMotion_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMotion_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMotion_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/action/RobotMotion_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__action__RobotMotion_GetResult_Response() }
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


