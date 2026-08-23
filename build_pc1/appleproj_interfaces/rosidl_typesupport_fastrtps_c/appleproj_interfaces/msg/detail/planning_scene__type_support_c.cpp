// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/msg/detail/planning_scene__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "appleproj_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "appleproj_interfaces/msg/detail/planning_scene__struct.h"
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "appleproj_interfaces/msg/detail/obstacle_proxy__functions.h"  // obstacles
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"  // robot_base_pose, robot_tcp_pose
#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions

bool cdr_serialize_appleproj_interfaces__msg__ObstacleProxy(
  const appleproj_interfaces__msg__ObstacleProxy * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_appleproj_interfaces__msg__ObstacleProxy(
  eprosima::fastcdr::Cdr & cdr,
  appleproj_interfaces__msg__ObstacleProxy * ros_message);

size_t get_serialized_size_appleproj_interfaces__msg__ObstacleProxy(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_appleproj_interfaces__msg__ObstacleProxy(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_appleproj_interfaces__msg__ObstacleProxy(
  const appleproj_interfaces__msg__ObstacleProxy * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_appleproj_interfaces__msg__ObstacleProxy(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_appleproj_interfaces__msg__ObstacleProxy(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, msg, ObstacleProxy)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
bool cdr_serialize_geometry_msgs__msg__PoseStamped(
  const geometry_msgs__msg__PoseStamped * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
bool cdr_deserialize_geometry_msgs__msg__PoseStamped(
  eprosima::fastcdr::Cdr & cdr,
  geometry_msgs__msg__PoseStamped * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t get_serialized_size_geometry_msgs__msg__PoseStamped(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t max_serialized_size_geometry_msgs__msg__PoseStamped(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
bool cdr_serialize_key_geometry_msgs__msg__PoseStamped(
  const geometry_msgs__msg__PoseStamped * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t get_serialized_size_key_geometry_msgs__msg__PoseStamped(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t max_serialized_size_key_geometry_msgs__msg__PoseStamped(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geometry_msgs, msg, PoseStamped)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
bool cdr_serialize_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
bool cdr_deserialize_std_msgs__msg__Header(
  eprosima::fastcdr::Cdr & cdr,
  std_msgs__msg__Header * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
bool cdr_serialize_key_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t get_serialized_size_key_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
size_t max_serialized_size_key_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_appleproj_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _PlanningScene__ros_msg_type = appleproj_interfaces__msg__PlanningScene;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
bool cdr_serialize_appleproj_interfaces__msg__PlanningScene(
  const appleproj_interfaces__msg__PlanningScene * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: header
  {
    cdr_serialize_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  // Field name: reset_id
  {
    cdr << ros_message->reset_id;
  }

  // Field name: scene_version
  {
    cdr << ros_message->scene_version;
  }

  // Field name: robot_base_pose
  {
    cdr_serialize_geometry_msgs__msg__PoseStamped(
      &ros_message->robot_base_pose, cdr);
  }

  // Field name: robot_tcp_pose
  {
    cdr_serialize_geometry_msgs__msg__PoseStamped(
      &ros_message->robot_tcp_pose, cdr);
  }

  // Field name: obstacles
  {
    size_t size = ros_message->obstacles.size;
    auto array_ptr = ros_message->obstacles.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_appleproj_interfaces__msg__ObstacleProxy(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
bool cdr_deserialize_appleproj_interfaces__msg__PlanningScene(
  eprosima::fastcdr::Cdr & cdr,
  appleproj_interfaces__msg__PlanningScene * ros_message)
{
  // Field name: header
  {
    cdr_deserialize_std_msgs__msg__Header(cdr, &ros_message->header);
  }

  // Field name: reset_id
  {
    cdr >> ros_message->reset_id;
  }

  // Field name: scene_version
  {
    cdr >> ros_message->scene_version;
  }

  // Field name: robot_base_pose
  {
    cdr_deserialize_geometry_msgs__msg__PoseStamped(cdr, &ros_message->robot_base_pose);
  }

  // Field name: robot_tcp_pose
  {
    cdr_deserialize_geometry_msgs__msg__PoseStamped(cdr, &ros_message->robot_tcp_pose);
  }

  // Field name: obstacles
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->obstacles.data) {
      appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(&ros_message->obstacles);
    }
    if (!appleproj_interfaces__msg__ObstacleProxy__Sequence__init(&ros_message->obstacles, size)) {
      fprintf(stderr, "failed to create array for field 'obstacles'");
      return false;
    }
    auto array_ptr = ros_message->obstacles.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_appleproj_interfaces__msg__ObstacleProxy(cdr, &array_ptr[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t get_serialized_size_appleproj_interfaces__msg__PlanningScene(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _PlanningScene__ros_msg_type * ros_message = static_cast<const _PlanningScene__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: header
  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  // Field name: reset_id
  {
    size_t item_size = sizeof(ros_message->reset_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: scene_version
  {
    size_t item_size = sizeof(ros_message->scene_version);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: robot_base_pose
  current_alignment += get_serialized_size_geometry_msgs__msg__PoseStamped(
    &(ros_message->robot_base_pose), current_alignment);

  // Field name: robot_tcp_pose
  current_alignment += get_serialized_size_geometry_msgs__msg__PoseStamped(
    &(ros_message->robot_tcp_pose), current_alignment);

  // Field name: obstacles
  {
    size_t array_size = ros_message->obstacles.size;
    auto array_ptr = ros_message->obstacles.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_appleproj_interfaces__msg__ObstacleProxy(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t max_serialized_size_appleproj_interfaces__msg__PlanningScene(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: reset_id
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: scene_version
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: robot_base_pose
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__PoseStamped(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: robot_tcp_pose
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__PoseStamped(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: obstacles
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_appleproj_interfaces__msg__ObstacleProxy(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = appleproj_interfaces__msg__PlanningScene;
    is_plain =
      (
      offsetof(DataType, obstacles) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
bool cdr_serialize_key_appleproj_interfaces__msg__PlanningScene(
  const appleproj_interfaces__msg__PlanningScene * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: header
  {
    cdr_serialize_key_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  // Field name: reset_id
  {
    cdr << ros_message->reset_id;
  }

  // Field name: scene_version
  {
    cdr << ros_message->scene_version;
  }

  // Field name: robot_base_pose
  {
    cdr_serialize_key_geometry_msgs__msg__PoseStamped(
      &ros_message->robot_base_pose, cdr);
  }

  // Field name: robot_tcp_pose
  {
    cdr_serialize_key_geometry_msgs__msg__PoseStamped(
      &ros_message->robot_tcp_pose, cdr);
  }

  // Field name: obstacles
  {
    size_t size = ros_message->obstacles.size;
    auto array_ptr = ros_message->obstacles.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_key_appleproj_interfaces__msg__ObstacleProxy(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t get_serialized_size_key_appleproj_interfaces__msg__PlanningScene(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _PlanningScene__ros_msg_type * ros_message = static_cast<const _PlanningScene__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: header
  current_alignment += get_serialized_size_key_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  // Field name: reset_id
  {
    size_t item_size = sizeof(ros_message->reset_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: scene_version
  {
    size_t item_size = sizeof(ros_message->scene_version);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: robot_base_pose
  current_alignment += get_serialized_size_key_geometry_msgs__msg__PoseStamped(
    &(ros_message->robot_base_pose), current_alignment);

  // Field name: robot_tcp_pose
  current_alignment += get_serialized_size_key_geometry_msgs__msg__PoseStamped(
    &(ros_message->robot_tcp_pose), current_alignment);

  // Field name: obstacles
  {
    size_t array_size = ros_message->obstacles.size;
    auto array_ptr = ros_message->obstacles.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_key_appleproj_interfaces__msg__ObstacleProxy(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_appleproj_interfaces
size_t max_serialized_size_key_appleproj_interfaces__msg__PlanningScene(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: reset_id
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: scene_version
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: robot_base_pose
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_geometry_msgs__msg__PoseStamped(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: robot_tcp_pose
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_geometry_msgs__msg__PoseStamped(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: obstacles
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_appleproj_interfaces__msg__ObstacleProxy(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = appleproj_interfaces__msg__PlanningScene;
    is_plain =
      (
      offsetof(DataType, obstacles) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _PlanningScene__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const appleproj_interfaces__msg__PlanningScene * ros_message = static_cast<const appleproj_interfaces__msg__PlanningScene *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_appleproj_interfaces__msg__PlanningScene(ros_message, cdr);
}

static bool _PlanningScene__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  appleproj_interfaces__msg__PlanningScene * ros_message = static_cast<appleproj_interfaces__msg__PlanningScene *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_appleproj_interfaces__msg__PlanningScene(cdr, ros_message);
}

static uint32_t _PlanningScene__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_appleproj_interfaces__msg__PlanningScene(
      untyped_ros_message, 0));
}

static size_t _PlanningScene__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_appleproj_interfaces__msg__PlanningScene(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_PlanningScene = {
  "appleproj_interfaces::msg",
  "PlanningScene",
  _PlanningScene__cdr_serialize,
  _PlanningScene__cdr_deserialize,
  _PlanningScene__get_serialized_size,
  _PlanningScene__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _PlanningScene__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_PlanningScene,
  get_message_typesupport_handle_function,
  &appleproj_interfaces__msg__PlanningScene__get_type_hash,
  &appleproj_interfaces__msg__PlanningScene__get_type_description,
  &appleproj_interfaces__msg__PlanningScene__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, msg, PlanningScene)() {
  return &_PlanningScene__type_support;
}

#if defined(__cplusplus)
}
#endif
