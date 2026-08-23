// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice

#include "appleproj_interfaces/msg/detail/quality_result__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__msg__QualityResult__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xda, 0xc8, 0xc1, 0x10, 0x13, 0x40, 0x02, 0xf7,
      0x77, 0x05, 0xa2, 0xed, 0x1d, 0x0d, 0x73, 0x2d,
      0xdd, 0xf1, 0x0a, 0x6d, 0x33, 0xc0, 0x52, 0x15,
      0xc6, 0xd1, 0x01, 0x88, 0x77, 0x6e, 0xbd, 0xa2,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "std_msgs/msg/detail/header__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char appleproj_interfaces__msg__QualityResult__TYPE_NAME[] = "appleproj_interfaces/msg/QualityResult";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__header[] = "header";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__inspection_id[] = "inspection_id";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__apple_id[] = "apple_id";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__grade[] = "grade";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__confidence[] = "confidence";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__color_ratio[] = "color_ratio";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__diameter_mm[] = "diameter_mm";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__damage_area_cm2[] = "damage_area_cm2";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__frames_used[] = "frames_used";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__frame_indices[] = "frame_indices";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__result_timestamp[] = "result_timestamp";
static char appleproj_interfaces__msg__QualityResult__FIELD_NAME__status[] = "status";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__msg__QualityResult__FIELDS[] = {
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__inspection_id, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__apple_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__grade, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__color_ratio, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__diameter_mm, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__damage_area_cm2, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__frames_used, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__frame_indices, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__result_timestamp, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__msg__QualityResult__FIELD_NAME__status, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription appleproj_interfaces__msg__QualityResult__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__msg__QualityResult__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__msg__QualityResult__TYPE_NAME, 38, 38},
      {appleproj_interfaces__msg__QualityResult__FIELDS, 12, 12},
    },
    {appleproj_interfaces__msg__QualityResult__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint8 HIGH=1\n"
  "uint8 MEDIUM=2\n"
  "uint8 LOW=3\n"
  "\n"
  "uint8 VALID=1\n"
  "uint8 RECHECK=2\n"
  "uint8 UNCLASSIFIED=3\n"
  "uint8 TIMEOUT=4\n"
  "uint8 LATE_RESULT=5\n"
  "uint8 ID_MISMATCH=6\n"
  "uint8 INSUFFICIENT_VIEWS=7\n"
  "\n"
  "std_msgs/Header header\n"
  "string inspection_id\n"
  "string apple_id\n"
  "uint8 grade\n"
  "float32 confidence\n"
  "float32 color_ratio\n"
  "float32 diameter_mm\n"
  "float32 damage_area_cm2\n"
  "uint16 frames_used\n"
  "uint16[] frame_indices\n"
  "builtin_interfaces/Time result_timestamp\n"
  "uint8 status";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__msg__QualityResult__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__msg__QualityResult__TYPE_NAME, 38, 38},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 427, 427},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__msg__QualityResult__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__msg__QualityResult__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
