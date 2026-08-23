#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to appleproj_interfaces__srv__GetPlanningScene_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPlanningScene_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetPlanningScene_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetPlanningScene_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetPlanningScene_Request {
  type RmwMsg = super::srv::rmw::GetPlanningScene_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to appleproj_interfaces__srv__GetPlanningScene_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPlanningScene_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene: super::msg::PlanningScene,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GetPlanningScene_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetPlanningScene_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetPlanningScene_Response {
  type RmwMsg = super::srv::rmw::GetPlanningScene_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        scene: super::msg::PlanningScene::into_rmw_message(std::borrow::Cow::Owned(msg.scene)).into_owned(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        scene: super::msg::PlanningScene::into_rmw_message(std::borrow::Cow::Borrowed(&msg.scene)).into_owned(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      scene: super::msg::PlanningScene::from_rmw_message(msg.scene),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to appleproj_interfaces__srv__RetryInspection_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RetryInspection_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for RetryInspection_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::RetryInspection_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RetryInspection_Request {
  type RmwMsg = super::srv::rmw::RetryInspection_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        inspection_id: msg.inspection_id.as_str().into(),
        apple_id: msg.apple_id.as_str().into(),
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        inspection_id: msg.inspection_id.as_str().into(),
        apple_id: msg.apple_id.as_str().into(),
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      inspection_id: msg.inspection_id.to_string(),
      apple_id: msg.apple_id.to_string(),
      reason: msg.reason.to_string(),
    }
  }
}


// Corresponds to appleproj_interfaces__srv__RetryInspection_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RetryInspection_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub new_inspection_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for RetryInspection_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::RetryInspection_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RetryInspection_Response {
  type RmwMsg = super::srv::rmw::RetryInspection_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        new_inspection_id: msg.new_inspection_id.as_str().into(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        new_inspection_id: msg.new_inspection_id.as_str().into(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      new_inspection_id: msg.new_inspection_id.to_string(),
      message: msg.message.to_string(),
    }
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


