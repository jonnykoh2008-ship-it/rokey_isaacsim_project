#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to appleproj_interfaces__msg__CheckpointEvent

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckpointEvent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub checkpoint_id: std::string::String,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CheckpointEvent::default())
  }
}

impl rosidl_runtime_rs::Message for CheckpointEvent {
  type RmwMsg = super::msg::rmw::CheckpointEvent;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        apple_id: msg.apple_id.as_str().into(),
        checkpoint_id: msg.checkpoint_id.as_str().into(),
        event: msg.event,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        apple_id: msg.apple_id.as_str().into(),
        checkpoint_id: msg.checkpoint_id.as_str().into(),
      event: msg.event,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      apple_id: msg.apple_id.to_string(),
      checkpoint_id: msg.checkpoint_id.to_string(),
      event: msg.event,
    }
  }
}


// Corresponds to appleproj_interfaces__msg__InspectionImage

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct InspectionImage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frame_index: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub total_frames: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image: sensor_msgs::msg::CompressedImage,

}



impl Default for InspectionImage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::InspectionImage::default())
  }
}

impl rosidl_runtime_rs::Message for InspectionImage {
  type RmwMsg = super::msg::rmw::InspectionImage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        inspection_id: msg.inspection_id.as_str().into(),
        apple_id: msg.apple_id.as_str().into(),
        frame_index: msg.frame_index,
        total_frames: msg.total_frames,
        image: sensor_msgs::msg::CompressedImage::into_rmw_message(std::borrow::Cow::Owned(msg.image)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        inspection_id: msg.inspection_id.as_str().into(),
        apple_id: msg.apple_id.as_str().into(),
      frame_index: msg.frame_index,
      total_frames: msg.total_frames,
        image: sensor_msgs::msg::CompressedImage::into_rmw_message(std::borrow::Cow::Borrowed(&msg.image)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      inspection_id: msg.inspection_id.to_string(),
      apple_id: msg.apple_id.to_string(),
      frame_index: msg.frame_index,
      total_frames: msg.total_frames,
      image: sensor_msgs::msg::CompressedImage::from_rmw_message(msg.image),
    }
  }
}


// Corresponds to appleproj_interfaces__msg__MotionStatus

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub progress: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MotionStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MotionStatus::default())
  }
}

impl rosidl_runtime_rs::Message for MotionStatus {
  type RmwMsg = super::msg::rmw::MotionStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        current_state: msg.current_state.as_str().into(),
        success: msg.success,
        progress: msg.progress,
        error_code: msg.error_code.as_str().into(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        current_state: msg.current_state.as_str().into(),
      success: msg.success,
      progress: msg.progress,
        error_code: msg.error_code.as_str().into(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      current_state: msg.current_state.to_string(),
      success: msg.success,
      progress: msg.progress,
      error_code: msg.error_code.to_string(),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to appleproj_interfaces__msg__ObstacleProxy

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleProxy {

    // This member is not documented.
    #[allow(missing_docs)]
    pub obstacle_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub shape: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obstacle_class: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub dimensions: geometry_msgs::msg::Vector3,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObstacleProxy::default())
  }
}

impl rosidl_runtime_rs::Message for ObstacleProxy {
  type RmwMsg = super::msg::rmw::ObstacleProxy;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        obstacle_id: msg.obstacle_id.as_str().into(),
        shape: msg.shape,
        obstacle_class: msg.obstacle_class,
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        dimensions: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(msg.dimensions)).into_owned(),
        safety_margin: msg.safety_margin,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        obstacle_id: msg.obstacle_id.as_str().into(),
      shape: msg.shape,
      obstacle_class: msg.obstacle_class,
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        dimensions: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(&msg.dimensions)).into_owned(),
      safety_margin: msg.safety_margin,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      obstacle_id: msg.obstacle_id.to_string(),
      shape: msg.shape,
      obstacle_class: msg.obstacle_class,
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      dimensions: geometry_msgs::msg::Vector3::from_rmw_message(msg.dimensions),
      safety_margin: msg.safety_margin,
    }
  }
}


// Corresponds to appleproj_interfaces__msg__PlanningScene

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanningScene {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reset_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scene_version: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_base_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_tcp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obstacles: Vec<super::msg::ObstacleProxy>,

}



impl Default for PlanningScene {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::PlanningScene::default())
  }
}

impl rosidl_runtime_rs::Message for PlanningScene {
  type RmwMsg = super::msg::rmw::PlanningScene;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        reset_id: msg.reset_id,
        scene_version: msg.scene_version,
        robot_base_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.robot_base_pose)).into_owned(),
        robot_tcp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.robot_tcp_pose)).into_owned(),
        obstacles: msg.obstacles
          .into_iter()
          .map(|elem| super::msg::ObstacleProxy::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      reset_id: msg.reset_id,
      scene_version: msg.scene_version,
        robot_base_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.robot_base_pose)).into_owned(),
        robot_tcp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.robot_tcp_pose)).into_owned(),
        obstacles: msg.obstacles
          .iter()
          .map(|elem| super::msg::ObstacleProxy::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      reset_id: msg.reset_id,
      scene_version: msg.scene_version,
      robot_base_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.robot_base_pose),
      robot_tcp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.robot_tcp_pose),
      obstacles: msg.obstacles
          .into_iter()
          .map(super::msg::ObstacleProxy::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to appleproj_interfaces__msg__QualityResult

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QualityResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apple_id: std::string::String,


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
    pub frame_indices: Vec<u16>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result_timestamp: builtin_interfaces::msg::Time,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::QualityResult::default())
  }
}

impl rosidl_runtime_rs::Message for QualityResult {
  type RmwMsg = super::msg::rmw::QualityResult;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        inspection_id: msg.inspection_id.as_str().into(),
        apple_id: msg.apple_id.as_str().into(),
        grade: msg.grade,
        confidence: msg.confidence,
        color_ratio: msg.color_ratio,
        diameter_mm: msg.diameter_mm,
        damage_area_cm2: msg.damage_area_cm2,
        frames_used: msg.frames_used,
        frame_indices: msg.frame_indices.into(),
        result_timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.result_timestamp)).into_owned(),
        status: msg.status,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        inspection_id: msg.inspection_id.as_str().into(),
        apple_id: msg.apple_id.as_str().into(),
      grade: msg.grade,
      confidence: msg.confidence,
      color_ratio: msg.color_ratio,
      diameter_mm: msg.diameter_mm,
      damage_area_cm2: msg.damage_area_cm2,
      frames_used: msg.frames_used,
        frame_indices: msg.frame_indices.as_slice().into(),
        result_timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result_timestamp)).into_owned(),
      status: msg.status,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      inspection_id: msg.inspection_id.to_string(),
      apple_id: msg.apple_id.to_string(),
      grade: msg.grade,
      confidence: msg.confidence,
      color_ratio: msg.color_ratio,
      diameter_mm: msg.diameter_mm,
      damage_area_cm2: msg.damage_area_cm2,
      frames_used: msg.frames_used,
      frame_indices: msg.frame_indices
          .into_iter()
          .collect(),
      result_timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.result_timestamp),
      status: msg.status,
    }
  }
}


// Corresponds to appleproj_interfaces__msg__SimulationState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SimulationState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    pub message: std::string::String,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SimulationState::default())
  }
}

impl rosidl_runtime_rs::Message for SimulationState {
  type RmwMsg = super::msg::rmw::SimulationState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        state: msg.state,
        reset_id: msg.reset_id,
        scene_version: msg.scene_version,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      state: msg.state,
      reset_id: msg.reset_id,
      scene_version: msg.scene_version,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      state: msg.state,
      reset_id: msg.reset_id,
      scene_version: msg.scene_version,
      message: msg.message.to_string(),
    }
  }
}


