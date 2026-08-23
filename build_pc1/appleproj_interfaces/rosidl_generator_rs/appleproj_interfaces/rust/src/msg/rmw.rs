#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__CheckpointEvent() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__CheckpointEvent__init(msg: *mut CheckpointEvent) -> bool;
    fn appleproj_interfaces__msg__CheckpointEvent__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CheckpointEvent>, size: usize) -> bool;
    fn appleproj_interfaces__msg__CheckpointEvent__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CheckpointEvent>);
    fn appleproj_interfaces__msg__CheckpointEvent__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CheckpointEvent>, out_seq: *mut rosidl_runtime_rs::Sequence<CheckpointEvent>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__CheckpointEvent
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckpointEvent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub checkpoint_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub event: u8,

}

impl CheckpointEvent {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ENTER: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EXIT: u8 = 2;

}


impl Default for CheckpointEvent {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__CheckpointEvent__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__CheckpointEvent__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CheckpointEvent {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__CheckpointEvent__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__CheckpointEvent__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__CheckpointEvent__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CheckpointEvent {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CheckpointEvent where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/CheckpointEvent";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__CheckpointEvent() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__InspectionImage() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__InspectionImage__init(msg: *mut InspectionImage) -> bool;
    fn appleproj_interfaces__msg__InspectionImage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<InspectionImage>, size: usize) -> bool;
    fn appleproj_interfaces__msg__InspectionImage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<InspectionImage>);
    fn appleproj_interfaces__msg__InspectionImage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<InspectionImage>, out_seq: *mut rosidl_runtime_rs::Sequence<InspectionImage>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__InspectionImage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct InspectionImage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frame_index: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub total_frames: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image: sensor_msgs::msg::rmw::CompressedImage,

}



impl Default for InspectionImage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__InspectionImage__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__InspectionImage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for InspectionImage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__InspectionImage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__InspectionImage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__InspectionImage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for InspectionImage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for InspectionImage where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/InspectionImage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__InspectionImage() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__MotionStatus() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__MotionStatus__init(msg: *mut MotionStatus) -> bool;
    fn appleproj_interfaces__msg__MotionStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotionStatus>, size: usize) -> bool;
    fn appleproj_interfaces__msg__MotionStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotionStatus>);
    fn appleproj_interfaces__msg__MotionStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotionStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<MotionStatus>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__MotionStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub progress: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MotionStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__MotionStatus__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__MotionStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotionStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__MotionStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__MotionStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__MotionStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotionStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotionStatus where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/MotionStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__MotionStatus() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__ObstacleProxy() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__ObstacleProxy__init(msg: *mut ObstacleProxy) -> bool;
    fn appleproj_interfaces__msg__ObstacleProxy__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObstacleProxy>, size: usize) -> bool;
    fn appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObstacleProxy>);
    fn appleproj_interfaces__msg__ObstacleProxy__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObstacleProxy>, out_seq: *mut rosidl_runtime_rs::Sequence<ObstacleProxy>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__ObstacleProxy
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleProxy {

    // This member is not documented.
    #[allow(missing_docs)]
    pub obstacle_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub shape: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obstacle_class: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub dimensions: geometry_msgs::msg::rmw::Vector3,


    // This member is not documented.
    #[allow(missing_docs)]
    pub safety_margin: f64,

}

impl ObstacleProxy {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SHAPE_SPHERE: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SHAPE_BOX: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SHAPE_CAPSULE: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLASS_TRUNK: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLASS_BRANCH: u8 = 2;

}


impl Default for ObstacleProxy {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__ObstacleProxy__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__ObstacleProxy__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObstacleProxy {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__ObstacleProxy__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__ObstacleProxy__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObstacleProxy {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObstacleProxy where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/ObstacleProxy";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__ObstacleProxy() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__PlanningScene() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__PlanningScene__init(msg: *mut PlanningScene) -> bool;
    fn appleproj_interfaces__msg__PlanningScene__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanningScene>, size: usize) -> bool;
    fn appleproj_interfaces__msg__PlanningScene__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanningScene>);
    fn appleproj_interfaces__msg__PlanningScene__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanningScene>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanningScene>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__PlanningScene
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanningScene {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reset_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene_version: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_base_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_tcp_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obstacles: rosidl_runtime_rs::Sequence<super::super::msg::rmw::ObstacleProxy>,

}



impl Default for PlanningScene {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__PlanningScene__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__PlanningScene__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanningScene {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__PlanningScene__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__PlanningScene__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__PlanningScene__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanningScene {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanningScene where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/PlanningScene";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__PlanningScene() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__QualityResult() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__QualityResult__init(msg: *mut QualityResult) -> bool;
    fn appleproj_interfaces__msg__QualityResult__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QualityResult>, size: usize) -> bool;
    fn appleproj_interfaces__msg__QualityResult__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QualityResult>);
    fn appleproj_interfaces__msg__QualityResult__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QualityResult>, out_seq: *mut rosidl_runtime_rs::Sequence<QualityResult>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__QualityResult
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QualityResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grade: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_ratio: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub diameter_mm: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub damage_area_cm2: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frames_used: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frame_indices: rosidl_runtime_rs::Sequence<u16>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result_timestamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: u8,

}

impl QualityResult {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const HIGH: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MEDIUM: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const LOW: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const VALID: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RECHECK: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const UNCLASSIFIED: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TIMEOUT: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const LATE_RESULT: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ID_MISMATCH: u8 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INSUFFICIENT_VIEWS: u8 = 7;

}


impl Default for QualityResult {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__QualityResult__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__QualityResult__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QualityResult {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__QualityResult__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__QualityResult__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__QualityResult__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QualityResult {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QualityResult where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/QualityResult";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__QualityResult() }
  }
}


#[link(name = "appleproj_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__SimulationState() -> *const std::ffi::c_void;
}

#[link(name = "appleproj_interfaces__rosidl_generator_c")]
extern "C" {
    fn appleproj_interfaces__msg__SimulationState__init(msg: *mut SimulationState) -> bool;
    fn appleproj_interfaces__msg__SimulationState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SimulationState>, size: usize) -> bool;
    fn appleproj_interfaces__msg__SimulationState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SimulationState>);
    fn appleproj_interfaces__msg__SimulationState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SimulationState>, out_seq: *mut rosidl_runtime_rs::Sequence<SimulationState>) -> bool;
}

// Corresponds to appleproj_interfaces__msg__SimulationState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SimulationState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reset_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene_version: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}

impl SimulationState {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOPPED: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INITIALIZING: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READY: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PLAYING: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PAUSED: u8 = 4;

}


impl Default for SimulationState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !appleproj_interfaces__msg__SimulationState__init(&mut msg as *mut _) {
        panic!("Call to appleproj_interfaces__msg__SimulationState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SimulationState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__SimulationState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__SimulationState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { appleproj_interfaces__msg__SimulationState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SimulationState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SimulationState where Self: Sized {
  const TYPE_NAME: &'static str = "appleproj_interfaces/msg/SimulationState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__appleproj_interfaces__msg__SimulationState() }
  }
}


