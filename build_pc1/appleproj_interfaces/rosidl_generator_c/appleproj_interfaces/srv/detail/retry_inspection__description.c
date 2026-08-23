// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from appleproj_interfaces:srv/RetryInspection.idl
// generated code does not contain a copyright notice

#include "appleproj_interfaces/srv/detail/retry_inspection__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__RetryInspection__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x3b, 0x34, 0x7d, 0xf4, 0x97, 0x60, 0xf8, 0xc4,
      0x0c, 0xd9, 0x20, 0xfd, 0x6f, 0x7c, 0x04, 0xdd,
      0x80, 0x4c, 0x56, 0x21, 0x52, 0x7c, 0xe3, 0x9e,
      0xc1, 0xa4, 0x4c, 0xab, 0x04, 0x05, 0xec, 0x37,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__RetryInspection_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xae, 0x2b, 0xd4, 0xe3, 0xea, 0xd1, 0x05, 0xe7,
      0xf2, 0xe1, 0xce, 0x91, 0xb2, 0x54, 0xf3, 0x61,
      0xda, 0x41, 0x95, 0x06, 0x9c, 0xf3, 0x83, 0x1a,
      0xe1, 0x1f, 0x44, 0x09, 0xb3, 0x52, 0xc6, 0x13,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__RetryInspection_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xdc, 0xf9, 0x0b, 0xf3, 0xb9, 0xa1, 0x09, 0x67,
      0xce, 0x88, 0x14, 0xe9, 0xce, 0x51, 0x32, 0x7b,
      0x06, 0xc7, 0x15, 0xf4, 0xfd, 0xd5, 0x1c, 0x2a,
      0xb0, 0xb9, 0x42, 0xdd, 0x52, 0x72, 0x30, 0xdd,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_appleproj_interfaces
const rosidl_type_hash_t *
appleproj_interfaces__srv__RetryInspection_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x1e, 0xfb, 0x7d, 0x09, 0x53, 0xa6, 0x1b, 0xbc,
      0xd4, 0x92, 0x63, 0xce, 0x1a, 0xa3, 0xb3, 0x5e,
      0x0d, 0xfc, 0xcc, 0xb6, 0xd6, 0x7b, 0x14, 0x55,
      0x97, 0xeb, 0xf5, 0x19, 0x5d, 0x34, 0x08, 0x3f,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "service_msgs/msg/detail/service_event_info__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char appleproj_interfaces__srv__RetryInspection__TYPE_NAME[] = "appleproj_interfaces/srv/RetryInspection";
static char appleproj_interfaces__srv__RetryInspection_Event__TYPE_NAME[] = "appleproj_interfaces/srv/RetryInspection_Event";
static char appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME[] = "appleproj_interfaces/srv/RetryInspection_Request";
static char appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME[] = "appleproj_interfaces/srv/RetryInspection_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char appleproj_interfaces__srv__RetryInspection__FIELD_NAME__request_message[] = "request_message";
static char appleproj_interfaces__srv__RetryInspection__FIELD_NAME__response_message[] = "response_message";
static char appleproj_interfaces__srv__RetryInspection__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__RetryInspection__FIELDS[] = {
  {
    {appleproj_interfaces__srv__RetryInspection__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {appleproj_interfaces__srv__RetryInspection_Event__TYPE_NAME, 46, 46},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription appleproj_interfaces__srv__RetryInspection__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {appleproj_interfaces__srv__RetryInspection_Event__TYPE_NAME, 46, 46},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__RetryInspection__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__RetryInspection__TYPE_NAME, 40, 40},
      {appleproj_interfaces__srv__RetryInspection__FIELDS, 3, 3},
    },
    {appleproj_interfaces__srv__RetryInspection__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = appleproj_interfaces__srv__RetryInspection_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = appleproj_interfaces__srv__RetryInspection_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = appleproj_interfaces__srv__RetryInspection_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char appleproj_interfaces__srv__RetryInspection_Request__FIELD_NAME__inspection_id[] = "inspection_id";
static char appleproj_interfaces__srv__RetryInspection_Request__FIELD_NAME__apple_id[] = "apple_id";
static char appleproj_interfaces__srv__RetryInspection_Request__FIELD_NAME__reason[] = "reason";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__RetryInspection_Request__FIELDS[] = {
  {
    {appleproj_interfaces__srv__RetryInspection_Request__FIELD_NAME__inspection_id, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Request__FIELD_NAME__apple_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Request__FIELD_NAME__reason, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__RetryInspection_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME, 48, 48},
      {appleproj_interfaces__srv__RetryInspection_Request__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char appleproj_interfaces__srv__RetryInspection_Response__FIELD_NAME__accepted[] = "accepted";
static char appleproj_interfaces__srv__RetryInspection_Response__FIELD_NAME__new_inspection_id[] = "new_inspection_id";
static char appleproj_interfaces__srv__RetryInspection_Response__FIELD_NAME__message[] = "message";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__RetryInspection_Response__FIELDS[] = {
  {
    {appleproj_interfaces__srv__RetryInspection_Response__FIELD_NAME__accepted, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Response__FIELD_NAME__new_inspection_id, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Response__FIELD_NAME__message, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__RetryInspection_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME, 49, 49},
      {appleproj_interfaces__srv__RetryInspection_Response__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char appleproj_interfaces__srv__RetryInspection_Event__FIELD_NAME__info[] = "info";
static char appleproj_interfaces__srv__RetryInspection_Event__FIELD_NAME__request[] = "request";
static char appleproj_interfaces__srv__RetryInspection_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field appleproj_interfaces__srv__RetryInspection_Event__FIELDS[] = {
  {
    {appleproj_interfaces__srv__RetryInspection_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription appleproj_interfaces__srv__RetryInspection_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
appleproj_interfaces__srv__RetryInspection_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {appleproj_interfaces__srv__RetryInspection_Event__TYPE_NAME, 46, 46},
      {appleproj_interfaces__srv__RetryInspection_Event__FIELDS, 3, 3},
    },
    {appleproj_interfaces__srv__RetryInspection_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = appleproj_interfaces__srv__RetryInspection_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = appleproj_interfaces__srv__RetryInspection_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string inspection_id\n"
  "string apple_id\n"
  "string reason\n"
  "---\n"
  "bool accepted\n"
  "string new_inspection_id\n"
  "string message";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__RetryInspection__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__RetryInspection__TYPE_NAME, 40, 40},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 109, 109},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__RetryInspection_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__RetryInspection_Request__TYPE_NAME, 48, 48},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__RetryInspection_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__RetryInspection_Response__TYPE_NAME, 49, 49},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
appleproj_interfaces__srv__RetryInspection_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {appleproj_interfaces__srv__RetryInspection_Event__TYPE_NAME, 46, 46},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__RetryInspection__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__RetryInspection__get_individual_type_description_source(NULL),
    sources[1] = *appleproj_interfaces__srv__RetryInspection_Event__get_individual_type_description_source(NULL);
    sources[2] = *appleproj_interfaces__srv__RetryInspection_Request__get_individual_type_description_source(NULL);
    sources[3] = *appleproj_interfaces__srv__RetryInspection_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__RetryInspection_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__RetryInspection_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__RetryInspection_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__RetryInspection_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
appleproj_interfaces__srv__RetryInspection_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *appleproj_interfaces__srv__RetryInspection_Event__get_individual_type_description_source(NULL),
    sources[1] = *appleproj_interfaces__srv__RetryInspection_Request__get_individual_type_description_source(NULL);
    sources[2] = *appleproj_interfaces__srv__RetryInspection_Response__get_individual_type_description_source(NULL);
    sources[3] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
