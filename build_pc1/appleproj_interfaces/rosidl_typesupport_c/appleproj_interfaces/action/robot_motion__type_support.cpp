// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from appleproj_interfaces:action/RobotMotion.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "appleproj_interfaces/action/detail/robot_motion__struct.h"
#include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
#include "appleproj_interfaces/action/detail/robot_motion__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_Goal_type_support_ids_t;

static const _RobotMotion_Goal_type_support_ids_t _RobotMotion_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_Goal_type_support_symbol_names_t _RobotMotion_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_Goal)),
  }
};

typedef struct _RobotMotion_Goal_type_support_data_t
{
  void * data[2];
} _RobotMotion_Goal_type_support_data_t;

static _RobotMotion_Goal_type_support_data_t _RobotMotion_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_Goal_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_Goal_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_Goal__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_Goal__get_type_description,
  &appleproj_interfaces__action__RobotMotion_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_Goal)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_Result_type_support_ids_t;

static const _RobotMotion_Result_type_support_ids_t _RobotMotion_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_Result_type_support_symbol_names_t _RobotMotion_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_Result)),
  }
};

typedef struct _RobotMotion_Result_type_support_data_t
{
  void * data[2];
} _RobotMotion_Result_type_support_data_t;

static _RobotMotion_Result_type_support_data_t _RobotMotion_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_Result_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_Result_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_Result_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_Result_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_Result__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_Result__get_type_description,
  &appleproj_interfaces__action__RobotMotion_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_Result)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_Feedback_type_support_ids_t;

static const _RobotMotion_Feedback_type_support_ids_t _RobotMotion_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_Feedback_type_support_symbol_names_t _RobotMotion_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_Feedback)),
  }
};

typedef struct _RobotMotion_Feedback_type_support_data_t
{
  void * data[2];
} _RobotMotion_Feedback_type_support_data_t;

static _RobotMotion_Feedback_type_support_data_t _RobotMotion_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_Feedback_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_Feedback_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_Feedback__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_Feedback__get_type_description,
  &appleproj_interfaces__action__RobotMotion_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_Feedback)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_SendGoal_Request_type_support_ids_t;

static const _RobotMotion_SendGoal_Request_type_support_ids_t _RobotMotion_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_SendGoal_Request_type_support_symbol_names_t _RobotMotion_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_SendGoal_Request)),
  }
};

typedef struct _RobotMotion_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _RobotMotion_SendGoal_Request_type_support_data_t;

static _RobotMotion_SendGoal_Request_type_support_data_t _RobotMotion_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_SendGoal_Request_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_SendGoal_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Request__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Request__get_type_description,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_SendGoal_Request)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_SendGoal_Response_type_support_ids_t;

static const _RobotMotion_SendGoal_Response_type_support_ids_t _RobotMotion_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_SendGoal_Response_type_support_symbol_names_t _RobotMotion_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_SendGoal_Response)),
  }
};

typedef struct _RobotMotion_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _RobotMotion_SendGoal_Response_type_support_data_t;

static _RobotMotion_SendGoal_Response_type_support_data_t _RobotMotion_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_SendGoal_Response_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_SendGoal_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Response__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Response__get_type_description,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_SendGoal_Response)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_SendGoal_Event_type_support_ids_t;

static const _RobotMotion_SendGoal_Event_type_support_ids_t _RobotMotion_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_SendGoal_Event_type_support_symbol_names_t _RobotMotion_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_SendGoal_Event)),
  }
};

typedef struct _RobotMotion_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _RobotMotion_SendGoal_Event_type_support_data_t;

static _RobotMotion_SendGoal_Event_type_support_data_t _RobotMotion_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_SendGoal_Event_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_SendGoal_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_SendGoal_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Event__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Event__get_type_description,
  &appleproj_interfaces__action__RobotMotion_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_SendGoal_Event)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _RobotMotion_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_SendGoal_type_support_ids_t;

static const _RobotMotion_SendGoal_type_support_ids_t _RobotMotion_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_SendGoal_type_support_symbol_names_t _RobotMotion_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_SendGoal)),
  }
};

typedef struct _RobotMotion_SendGoal_type_support_data_t
{
  void * data[2];
} _RobotMotion_SendGoal_type_support_data_t;

static _RobotMotion_SendGoal_type_support_data_t _RobotMotion_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_SendGoal_service_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t RobotMotion_SendGoal_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &RobotMotion_SendGoal_Request_message_type_support_handle,
  &RobotMotion_SendGoal_Response_message_type_support_handle,
  &RobotMotion_SendGoal_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    appleproj_interfaces,
    action,
    RobotMotion_SendGoal
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    appleproj_interfaces,
    action,
    RobotMotion_SendGoal
  ),
  &appleproj_interfaces__action__RobotMotion_SendGoal__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_SendGoal__get_type_description,
  &appleproj_interfaces__action__RobotMotion_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_SendGoal)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_GetResult_Request_type_support_ids_t;

static const _RobotMotion_GetResult_Request_type_support_ids_t _RobotMotion_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_GetResult_Request_type_support_symbol_names_t _RobotMotion_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_GetResult_Request)),
  }
};

typedef struct _RobotMotion_GetResult_Request_type_support_data_t
{
  void * data[2];
} _RobotMotion_GetResult_Request_type_support_data_t;

static _RobotMotion_GetResult_Request_type_support_data_t _RobotMotion_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_GetResult_Request_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_GetResult_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_GetResult_Request__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_GetResult_Request__get_type_description,
  &appleproj_interfaces__action__RobotMotion_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_GetResult_Request)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_GetResult_Response_type_support_ids_t;

static const _RobotMotion_GetResult_Response_type_support_ids_t _RobotMotion_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_GetResult_Response_type_support_symbol_names_t _RobotMotion_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_GetResult_Response)),
  }
};

typedef struct _RobotMotion_GetResult_Response_type_support_data_t
{
  void * data[2];
} _RobotMotion_GetResult_Response_type_support_data_t;

static _RobotMotion_GetResult_Response_type_support_data_t _RobotMotion_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_GetResult_Response_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_GetResult_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_GetResult_Response__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_GetResult_Response__get_type_description,
  &appleproj_interfaces__action__RobotMotion_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_GetResult_Response)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_GetResult_Event_type_support_ids_t;

static const _RobotMotion_GetResult_Event_type_support_ids_t _RobotMotion_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_GetResult_Event_type_support_symbol_names_t _RobotMotion_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_GetResult_Event)),
  }
};

typedef struct _RobotMotion_GetResult_Event_type_support_data_t
{
  void * data[2];
} _RobotMotion_GetResult_Event_type_support_data_t;

static _RobotMotion_GetResult_Event_type_support_data_t _RobotMotion_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_GetResult_Event_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_GetResult_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_GetResult_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_GetResult_Event__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_GetResult_Event__get_type_description,
  &appleproj_interfaces__action__RobotMotion_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_GetResult_Event)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "service_msgs/msg/service_event_info.h"
// already included above
// #include "builtin_interfaces/msg/time.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _RobotMotion_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_GetResult_type_support_ids_t;

static const _RobotMotion_GetResult_type_support_ids_t _RobotMotion_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_GetResult_type_support_symbol_names_t _RobotMotion_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_GetResult)),
  }
};

typedef struct _RobotMotion_GetResult_type_support_data_t
{
  void * data[2];
} _RobotMotion_GetResult_type_support_data_t;

static _RobotMotion_GetResult_type_support_data_t _RobotMotion_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_GetResult_service_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t RobotMotion_GetResult_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &RobotMotion_GetResult_Request_message_type_support_handle,
  &RobotMotion_GetResult_Response_message_type_support_handle,
  &RobotMotion_GetResult_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    appleproj_interfaces,
    action,
    RobotMotion_GetResult
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    appleproj_interfaces,
    action,
    RobotMotion_GetResult
  ),
  &appleproj_interfaces__action__RobotMotion_GetResult__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_GetResult__get_type_description,
  &appleproj_interfaces__action__RobotMotion_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_GetResult)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__struct.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace appleproj_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _RobotMotion_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _RobotMotion_FeedbackMessage_type_support_ids_t;

static const _RobotMotion_FeedbackMessage_type_support_ids_t _RobotMotion_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _RobotMotion_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _RobotMotion_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _RobotMotion_FeedbackMessage_type_support_symbol_names_t _RobotMotion_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, appleproj_interfaces, action, RobotMotion_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, appleproj_interfaces, action, RobotMotion_FeedbackMessage)),
  }
};

typedef struct _RobotMotion_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _RobotMotion_FeedbackMessage_type_support_data_t;

static _RobotMotion_FeedbackMessage_type_support_data_t _RobotMotion_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _RobotMotion_FeedbackMessage_message_typesupport_map = {
  2,
  "appleproj_interfaces",
  &_RobotMotion_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_RobotMotion_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_RobotMotion_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t RobotMotion_FeedbackMessage_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_RobotMotion_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &appleproj_interfaces__action__RobotMotion_FeedbackMessage__get_type_hash,
  &appleproj_interfaces__action__RobotMotion_FeedbackMessage__get_type_description,
  &appleproj_interfaces__action__RobotMotion_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace appleproj_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_FeedbackMessage)() {
  return &::appleproj_interfaces::action::rosidl_typesupport_c::RobotMotion_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "appleproj_interfaces/action/robot_motion.h"
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__type_support.h"

static rosidl_action_type_support_t _appleproj_interfaces__action__RobotMotion__typesupport_c = {
  NULL, NULL, NULL, NULL, NULL,
  &appleproj_interfaces__action__RobotMotion__get_type_hash,
  &appleproj_interfaces__action__RobotMotion__get_type_description,
  &appleproj_interfaces__action__RobotMotion__get_type_description_sources,
};

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion)()
{
  // Thread-safe by always writing the same values to the static struct
  _appleproj_interfaces__action__RobotMotion__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_SendGoal)();
  _appleproj_interfaces__action__RobotMotion__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_GetResult)();
  _appleproj_interfaces__action__RobotMotion__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _appleproj_interfaces__action__RobotMotion__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, appleproj_interfaces, action, RobotMotion_FeedbackMessage)();
  _appleproj_interfaces__action__RobotMotion__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_appleproj_interfaces__action__RobotMotion__typesupport_c;
}

#ifdef __cplusplus
}
#endif
