#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__GetPlanningScene_Request() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__srv__GetPlanningScene_Request__init(msg: *mut GetPlanningScene_Request) -> bool;
    fn appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetPlanningScene_Request>, size: usize) -> bool;
    fn appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetPlanningScene_Request>);
    fn appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetPlanningScene_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetPlanningScene_Request>) -> bool;
}

// Corresponds to appleproj_interfaces__srv__GetPlanningScene_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPlanningScene_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetPlanningScene_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__srv__GetPlanningScene_Request__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__srv__GetPlanningScene_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetPlanningScene_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetPlanningScene_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetPlanningScene_Request where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/srv/GetPlanningScene_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__GetPlanningScene_Request() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__GetPlanningScene_Response() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__srv__GetPlanningScene_Response__init(msg: *mut GetPlanningScene_Response) -> bool;
    fn appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetPlanningScene_Response>, size: usize) -> bool;
    fn appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetPlanningScene_Response>);
    fn appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetPlanningScene_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetPlanningScene_Response>) -> bool;
}

// Corresponds to appleproj_interfaces__srv__GetPlanningScene_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPlanningScene_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene: super::super::msg::rmw::PlanningScene,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for GetPlanningScene_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__srv__GetPlanningScene_Response__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__srv__GetPlanningScene_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetPlanningScene_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetPlanningScene_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetPlanningScene_Response where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/srv/GetPlanningScene_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__GetPlanningScene_Response() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__RetryInspection_Request() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__srv__RetryInspection_Request__init(msg: *mut RetryInspection_Request) -> bool;
    fn appleproj_interfaces__srv__RetryInspection_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RetryInspection_Request>, size: usize) -> bool;
    fn appleproj_interfaces__srv__RetryInspection_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RetryInspection_Request>);
    fn appleproj_interfaces__srv__RetryInspection_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RetryInspection_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RetryInspection_Request>) -> bool;
}

// Corresponds to appleproj_interfaces__srv__RetryInspection_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RetryInspection_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for RetryInspection_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__srv__RetryInspection_Request__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__srv__RetryInspection_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RetryInspection_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__RetryInspection_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__RetryInspection_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__RetryInspection_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RetryInspection_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RetryInspection_Request where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/srv/RetryInspection_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__RetryInspection_Request() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__RetryInspection_Response() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__srv__RetryInspection_Response__init(msg: *mut RetryInspection_Response) -> bool;
    fn appleproj_interfaces__srv__RetryInspection_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RetryInspection_Response>, size: usize) -> bool;
    fn appleproj_interfaces__srv__RetryInspection_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RetryInspection_Response>);
    fn appleproj_interfaces__srv__RetryInspection_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RetryInspection_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RetryInspection_Response>) -> bool;
}

// Corresponds to appleproj_interfaces__srv__RetryInspection_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RetryInspection_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub new_inspection_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for RetryInspection_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__srv__RetryInspection_Response__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__srv__RetryInspection_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RetryInspection_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__RetryInspection_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__RetryInspection_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__srv__RetryInspection_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RetryInspection_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RetryInspection_Response where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/srv/RetryInspection_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__srv__RetryInspection_Response() }
  }
}






#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__srv__GetPlanningScene() -> *const std::ffi::c_void;
}

// Corresponds to appleproj_interfaces__srv__GetPlanningScene
#[allow(missing_docs, non_camel_case_types)]
pub struct GetPlanningScene;

impl rosidl_runtime_rs::Service for GetPlanningScene {
    type Request = GetPlanningScene_Request;
    type Response = GetPlanningScene_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__srv__GetPlanningScene() }
    }
}




#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__srv__RetryInspection() -> *const std::ffi::c_void;
}

// Corresponds to appleproj_interfaces__srv__RetryInspection
#[allow(missing_docs, non_camel_case_types)]
pub struct RetryInspection;

impl rosidl_runtime_rs::Service for RetryInspection {
    type Request = RetryInspection_Request;
    type Response = RetryInspection_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__appleproj_interfaces__srv__RetryInspection() }
    }
}


