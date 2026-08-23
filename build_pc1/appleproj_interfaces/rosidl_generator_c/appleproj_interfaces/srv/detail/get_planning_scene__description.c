// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from appleproj_interfaces:srv/GetPlanningScene.idl
// generated code does not contain a copyright notice

#include "appleproj_interfaces/srv/detail/get_planning_scene__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__GetPlanningScene__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xcf, 0x4e, 0x74, 0xf3, 0xbb, 0x54, 0x0a, 0x22,
      0x84, 0x24, 0xc5, 0x6c, 0xf8, 0xca, 0x12, 0xe1,
      0xc1, 0xd9, 0x5a, 0xc0, 0x21, 0xb1, 0x7c, 0x26,
      0x46, 0x6f, 0x82, 0x87, 0x89, 0x74, 0x38, 0x59,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__GetPlanningScene_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xe0, 0xb3, 0x6c, 0xb5, 0x33, 0xa7, 0x92, 0xee,
      0x0c, 0xf2, 0xd7, 0x53, 0x90, 0x16, 0xf3, 0x76,
      0xac, 0xee, 0x8f, 0xc0, 0xed, 0x5d, 0x4b, 0x18,
      0x3f, 0x57, 0xc7, 0xb4, 0x39, 0x61, 0xd0, 0xe6,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__GetPlanningScene_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x75, 0xf2, 0x7f, 0x51, 0x19, 0x9d, 0x38, 0x99,
      0x60, 0xf3, 0xc8, 0x31, 0x2b, 0x9b, 0xc3, 0x8b,
      0x10, 0xea, 0x44, 0x39, 0xfb, 0x0f, 0x9f, 0xea,
      0xbc, 0x65, 0x17, 0x70, 0xb1, 0x11, 0x80, 0xa2,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__GetPlanningScene_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb1, 0x2d, 0x3d, 0x1f, 0x2b, 0x7d, 0x6d, 0x41,
      0x94, 0xb9, 0xc2, 0x15, 0xc7, 0x0d, 0x17, 0xc7,
      0xc3, 0x6b, 0xe9, 0xc8, 0x38, 0xb9, 0x7a, 0xa7,
      0xf9, 0x6f, 0xaf, 0xed, 0x5d, 0xc1, 0x82, 0xbb,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "service_msgs/msg/detail/service_event_info__functions.h"
#include "geometry_msgs/msg/detail/pose__functions.h"
#include "appleproj_interfaces/msg/detail/obstacle_proxy__functions.h"
#include "geometry_msgs/msg/detail/vector3__functions.h"
#include "geometry_msgs/msg/detail/quaternion__functions.h"
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"
#include "std_msgs/msg/detail/header__functions.h"
#include "geometry_msgs/msg/detail/point__functions.h"
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t appleproj_interfaces__msg__ObstacleProxy__EXPECTED_HASH = {1, {
    0xae, 0x8b, 0x19, 0xd5, 0x89, 0x1e, 0x6e, 0xcd,
    0x40, 0x4d, 0xa3, 0x85, 0xcc, 0xd2, 0xb4, 0x26,
    0x45, 0x14, 0x7f, 0xe2, 0xb6, 0x4d, 0x6e, 0x63,
    0x0b, 0x98, 0x08, 0x5c, 0x67, 0xae, 0xd8, 0x6c,
  }};
static const rosidl_type_hash_t appleproj_interfaces__msg__PlanningScene__EXPECTED_HASH = {1, {
    0x44, 0x14, 0xf5, 0xcf, 0x38, 0x57, 0xa3, 0x70,
    0x18, 0x46, 0x45, 0xd9, 0x69, 0x6d, 0x69, 0x0f,
    0x3d, 0x6b, 0x49, 0xcd, 0x3f, 0xc1, 0xb9, 0x38,
    0x11, 0x94, 0x7a, 0x60, 0xde, 0x28, 0x33, 0xb2,
  }};
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Point__EXPECTED_HASH = {1, {
    0x69, 0x63, 0x08, 0x48, 0x42, 0xa9, 0xb0, 0x44,
    0x94, 0xd6, 0xb2, 0x94, 0x1d, 0x11, 0x44, 0x47,
    0x08, 0xd8, 0x92, 0xda, 0x2f, 0x4b, 0x09, 0x84,
    0x3b, 0x9c, 0x43, 0xf4, 0x2a, 0x7f, 0x68, 0x81,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Pose__EXPECTED_HASH = {1, {
    0xd5, 0x01, 0x95, 0x4e, 0x94, 0x76, 0xce, 0xa2,
    0x99, 0x69, 0x84, 0xe8, 0x12, 0x05, 0x4b, 0x68,
    0x02, 0x6a, 0xe0, 0xbf, 0xae, 0x78, 0x9d, 0x9a,
    0x10, 0xb2, 0x3d, 0xaf, 0x35, 0xcc, 0x90, 0xfa,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__PoseStamped__EXPECTED_HASH = {1, {
    0x10, 0xf3, 0x78, 0x6d, 0x7d, 0x40, 0xfd, 0x2b,
    0x54, 0x36, 0x78, 0x35, 0x61, 0x4b, 0xff, 0x85,
    0xd4, 0xad, 0x3b, 0x5d, 0xab, 0x62, 0xbf, 0x8b,
    0xca, 0x0c, 0xc2, 0x32, 0xd7, 0x3b, 0x4c, 0xd8,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Quaternion__EXPECTED_HASH = {1, {
    0x8a, 0x76, 0x5f, 0x66, 0x77, 0x8c, 0x8f, 0xf7,
    0xc8, 0xab, 0x94, 0xaf, 0xcc, 0x59, 0x0a, 0x2e,
    0xd5, 0x32, 0x5a, 0x1d, 0x9a, 0x07, 0x6f, 0xff,
    0xf3, 0x8f, 0xbc, 0xe3, 0x6f, 0x45, 0x86, 0x84,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Vector3__EXPECTED_HASH = {1, {
    0xcc, 0x12, 0xfe, 0x83, 0xe4, 0xc0, 0x27, 0x19,
    0xf1, 0xce, 0x80, 0x70, 0xbf, 0xd1, 0x4a, 0xec,
    0xd4, 0x0f, 0x75, 0xa9, 0x66, 0x96, 0xa6, 0x7a,
    0x2a, 0x1f, 0x37, 0xf7, 0xdb, 0xb0, 0x76, 0x5d,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char appleproj_interfaces__srv__GetPlanningScene__TYPE_NAME[] = "appleproj_interfaces/srv/GetPlanningScene";
static char appleproj_interfaces__msg__ObstacleProxy__TYPE_NAME[] = "appleproj_interfaces/msg/ObstacleProxy";
static char appleproj_interfaces__msg__PlanningScene__TYPE_NAME[] = "appleproj_interfaces/msg/PlanningScene";
static char appleproj_interfaces__srv__GetPlanningScene_Event__TYPE_NAME[] = "appleproj_interfaces/srv/GetPlanningScene_Event";
static char appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME[] = "appleproj_interfaces/srv/GetPlanningScene_Request";
static char appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME[] = "appleproj_interfaces/srv/GetPlanningScene_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";
static char geometry_msgs__msg__Pose__TYPE_NAME[] = "geometry_msgs/msg/Pose";
static char geometry_msgs__msg__PoseStamped__TYPE_NAME[] = "geometry_msgs/msg/PoseStamped";
static char geometry_msgs__msg__Quaternion__TYPE_NAME[] = "geometry_msgs/msg/Quaternion";
static char geometry_msgs__msg__Vector3__TYPE_NAME[] = "geometry_msgs/msg/Vector3";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char appleproj_interfaces__srv__GetPlanningScene__FIELD_NAME__request_message[] = "request_message";
static char appleproj_interfaces__srv__GetPlanningScene__FIELD_NAME__response_message[] = "response_message";
static char appleproj_interfaces__srv__GetPlanningScene__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__GetPlanningScene__FIELDS[] = {
  {
    {appleproj_interfaces__srv__GetPlanningScene__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME, 50, 50},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__srv__GetPlanningScene_Event__TYPE_NAME, 47, 47},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription appleproj_interfaces__srv__GetPlanningScene__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {appleproj_interfaces__msg__ObstacleProxy__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__PlanningScene__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Event__TYPE_NAME, 47, 47},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME, 50, 50},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Pose__TYPE_NAME, 22, 22},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__PoseStamped__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Quaternion__TYPE_NAME, 28, 28},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Vector3__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__GetPlanningScene__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__GetPlanningScene__TYPE_NAME, 41, 41},
      {appleproj_interfaces__srv__GetPlanningScene__FIELDS, 3, 3},
    },
    {appleproj_interfaces__srv__GetPlanningScene__REFERENCED_TYPE_DESCRIPTIONS, 13, 13},
  };
  if (!constructed) {
    assert(0 == memcmp(&appleproj_interfaces__msg__ObstacleProxy__EXPECTED_HASH, appleproj_interfaces__msg__ObstacleProxy__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = appleproj_interfaces__msg__ObstacleProxy__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&appleproj_interfaces__msg__PlanningScene__EXPECTED_HASH, appleproj_interfaces__msg__PlanningScene__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = appleproj_interfaces__msg__PlanningScene__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = appleproj_interfaces__srv__GetPlanningScene_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = appleproj_interfaces__srv__GetPlanningScene_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[4].fields = appleproj_interfaces__srv__GetPlanningScene_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Pose__EXPECTED_HASH, geometry_msgs__msg__Pose__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[7].fields = geometry_msgs__msg__Pose__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__PoseStamped__EXPECTED_HASH, geometry_msgs__msg__PoseStamped__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[8].fields = geometry_msgs__msg__PoseStamped__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Quaternion__EXPECTED_HASH, geometry_msgs__msg__Quaternion__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[9].fields = geometry_msgs__msg__Quaternion__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Vector3__EXPECTED_HASH, geometry_msgs__msg__Vector3__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[10].fields = geometry_msgs__msg__Vector3__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[11].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[12].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char appleproj_interfaces__srv__GetPlanningScene_Request__FIELD_NAME__structure_needs_at_least_one_member[] = "structure_needs_at_least_one_member";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__GetPlanningScene_Request__FIELDS[] = {
  {
    {appleproj_interfaces__srv__GetPlanningScene_Request__FIELD_NAME__structure_needs_at_least_one_member, 35, 35},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__GetPlanningScene_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME, 49, 49},
      {appleproj_interfaces__srv__GetPlanningScene_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char appleproj_interfaces__srv__GetPlanningScene_Response__FIELD_NAME__success[] = "success";
static char appleproj_interfaces__srv__GetPlanningScene_Response__FIELD_NAME__scene[] = "scene";
static char appleproj_interfaces__srv__GetPlanningScene_Response__FIELD_NAME__message[] = "message";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__GetPlanningScene_Response__FIELDS[] = {
  {
    {appleproj_interfaces__srv__GetPlanningScene_Response__FIELD_NAME__success, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Response__FIELD_NAME__scene, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__msg__PlanningScene__TYPE_NAME, 38, 38},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Response__FIELD_NAME__message, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription appleproj_interfaces__srv__GetPlanningScene_Response__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {appleproj_interfaces__msg__ObstacleProxy__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__PlanningScene__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Pose__TYPE_NAME, 22, 22},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__PoseStamped__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Quaternion__TYPE_NAME, 28, 28},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Vector3__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__GetPlanningScene_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME, 50, 50},
      {appleproj_interfaces__srv__GetPlanningScene_Response__FIELDS, 3, 3},
    },
    {appleproj_interfaces__srv__GetPlanningScene_Response__REFERENCED_TYPE_DESCRIPTIONS, 9, 9},
  };
  if (!constructed) {
    assert(0 == memcmp(&appleproj_interfaces__msg__ObstacleProxy__EXPECTED_HASH, appleproj_interfaces__msg__ObstacleProxy__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = appleproj_interfaces__msg__ObstacleProxy__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&appleproj_interfaces__msg__PlanningScene__EXPECTED_HASH, appleproj_interfaces__msg__PlanningScene__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = appleproj_interfaces__msg__PlanningScene__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Pose__EXPECTED_HASH, geometry_msgs__msg__Pose__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = geometry_msgs__msg__Pose__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__PoseStamped__EXPECTED_HASH, geometry_msgs__msg__PoseStamped__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = geometry_msgs__msg__PoseStamped__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Quaternion__EXPECTED_HASH, geometry_msgs__msg__Quaternion__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = geometry_msgs__msg__Quaternion__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Vector3__EXPECTED_HASH, geometry_msgs__msg__Vector3__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[7].fields = geometry_msgs__msg__Vector3__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[8].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char appleproj_interfaces__srv__GetPlanningScene_Event__FIELD_NAME__info[] = "info";
static char appleproj_interfaces__srv__GetPlanningScene_Event__FIELD_NAME__request[] = "request";
static char appleproj_interfaces__srv__GetPlanningScene_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__GetPlanningScene_Event__FIELDS[] = {
  {
    {appleproj_interfaces__srv__GetPlanningScene_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME, 50, 50},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription appleproj_interfaces__srv__GetPlanningScene_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {appleproj_interfaces__msg__ObstacleProxy__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__PlanningScene__TYPE_NAME, 38, 38},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME, 50, 50},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Pose__TYPE_NAME, 22, 22},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__PoseStamped__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Quaternion__TYPE_NAME, 28, 28},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Vector3__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__GetPlanningScene_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__GetPlanningScene_Event__TYPE_NAME, 47, 47},
      {appleproj_interfaces__srv__GetPlanningScene_Event__FIELDS, 3, 3},
    },
    {appleproj_interfaces__srv__GetPlanningScene_Event__REFERENCED_TYPE_DESCRIPTIONS, 12, 12},
  };
  if (!constructed) {
    assert(0 == memcmp(&appleproj_interfaces__msg__ObstacleProxy__EXPECTED_HASH, appleproj_interfaces__msg__ObstacleProxy__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = appleproj_interfaces__msg__ObstacleProxy__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&appleproj_interfaces__msg__PlanningScene__EXPECTED_HASH, appleproj_interfaces__msg__PlanningScene__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = appleproj_interfaces__msg__PlanningScene__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = appleproj_interfaces__srv__GetPlanningScene_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = appleproj_interfaces__srv__GetPlanningScene_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Pose__EXPECTED_HASH, geometry_msgs__msg__Pose__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = geometry_msgs__msg__Pose__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__PoseStamped__EXPECTED_HASH, geometry_msgs__msg__PoseStamped__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[7].fields = geometry_msgs__msg__PoseStamped__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Quaternion__EXPECTED_HASH, geometry_msgs__msg__Quaternion__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[8].fields = geometry_msgs__msg__Quaternion__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Vector3__EXPECTED_HASH, geometry_msgs__msg__Vector3__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[9].fields = geometry_msgs__msg__Vector3__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[10].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[11].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "---\n"
  "bool success\n"
  "appleproj_interfaces/PlanningScene scene\n"
  "string message";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__GetPlanningScene__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__GetPlanningScene__TYPE_NAME, 41, 41},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 73, 73},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__GetPlanningScene_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__GetPlanningScene_Request__TYPE_NAME, 49, 49},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__GetPlanningScene_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__GetPlanningScene_Response__TYPE_NAME, 50, 50},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__GetPlanningScene_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__GetPlanningScene_Event__TYPE_NAME, 47, 47},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__GetPlanningScene__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[14];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 14, 14};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__GetPlanningScene__get_individual_type_description_source(NULL),
    sources[1] = *appleproj_interfaces__msg__ObstacleProxy__get_individual_type_description_source(NULL);
    sources[2] = *appleproj_interfaces__msg__PlanningScene__get_individual_type_description_source(NULL);
    sources[3] = *appleproj_interfaces__srv__GetPlanningScene_Event__get_individual_type_description_source(NULL);
    sources[4] = *appleproj_interfaces__srv__GetPlanningScene_Request__get_individual_type_description_source(NULL);
    sources[5] = *appleproj_interfaces__srv__GetPlanningScene_Response__get_individual_type_description_source(NULL);
    sources[6] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[7] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[8] = *geometry_msgs__msg__Pose__get_individual_type_description_source(NULL);
    sources[9] = *geometry_msgs__msg__PoseStamped__get_individual_type_description_source(NULL);
    sources[10] = *geometry_msgs__msg__Quaternion__get_individual_type_description_source(NULL);
    sources[11] = *geometry_msgs__msg__Vector3__get_individual_type_description_source(NULL);
    sources[12] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[13] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__GetPlanningScene_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__GetPlanningScene_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__GetPlanningScene_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[10];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 10, 10};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__GetPlanningScene_Response__get_individual_type_description_source(NULL),
    sources[1] = *appleproj_interfaces__msg__ObstacleProxy__get_individual_type_description_source(NULL);
    sources[2] = *appleproj_interfaces__msg__PlanningScene__get_individual_type_description_source(NULL);
    sources[3] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[4] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[5] = *geometry_msgs__msg__Pose__get_individual_type_description_source(NULL);
    sources[6] = *geometry_msgs__msg__PoseStamped__get_individual_type_description_source(NULL);
    sources[7] = *geometry_msgs__msg__Quaternion__get_individual_type_description_source(NULL);
    sources[8] = *geometry_msgs__msg__Vector3__get_individual_type_description_source(NULL);
    sources[9] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__GetPlanningScene_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[13];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 13, 13};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__GetPlanningScene_Event__get_individual_type_description_source(NULL),
    sources[1] = *appleproj_interfaces__msg__ObstacleProxy__get_individual_type_description_source(NULL);
    sources[2] = *appleproj_interfaces__msg__PlanningScene__get_individual_type_description_source(NULL);
    sources[3] = *appleproj_interfaces__srv__GetPlanningScene_Request__get_individual_type_description_source(NULL);
    sources[4] = *appleproj_interfaces__srv__GetPlanningScene_Response__get_individual_type_description_source(NULL);
    sources[5] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[6] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[7] = *geometry_msgs__msg__Pose__get_individual_type_description_source(NULL);
    sources[8] = *geometry_msgs__msg__PoseStamped__get_individual_type_description_source(NULL);
    sources[9] = *geometry_msgs__msg__Quaternion__get_individual_type_description_source(NULL);
    sources[10] = *geometry_msgs__msg__Vector3__get_individual_type_description_source(NULL);
    sources[11] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[12] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
