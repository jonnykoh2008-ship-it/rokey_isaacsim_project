// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:srv/GetPlanningScene.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/get_planning_scene.hpp"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/srv/detail/get_planning_scene__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace appleproj_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetPlanningScene_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetPlanningScene_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetPlanningScene_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace appleproj_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use appleproj_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const appleproj_interfaces::srv::GetPlanningScene_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::srv::GetPlanningScene_Request & msg)
{
  return appleproj_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::srv::GetPlanningScene_Request>()
{
  return "appleproj_interfaces::srv::GetPlanningScene_Request";
}

template<>
inline const char * name<appleproj_interfaces::srv::GetPlanningScene_Request>()
{
  return "appleproj_interfaces/srv/GetPlanningScene_Request";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::GetPlanningScene_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<appleproj_interfaces::srv::GetPlanningScene_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'scene'
#include "appleproj_interfaces/msg/detail/planning_scene__traits.hpp"

namespace appleproj_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetPlanningScene_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: scene
  {
    out << "scene: ";
    to_flow_style_yaml(msg.scene, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetPlanningScene_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: scene
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scene:\n";
    to_block_style_yaml(msg.scene, out, indentation + 2);
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetPlanningScene_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace appleproj_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use appleproj_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const appleproj_interfaces::srv::GetPlanningScene_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::srv::GetPlanningScene_Response & msg)
{
  return appleproj_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::srv::GetPlanningScene_Response>()
{
  return "appleproj_interfaces::srv::GetPlanningScene_Response";
}

template<>
inline const char * name<appleproj_interfaces::srv::GetPlanningScene_Response>()
{
  return "appleproj_interfaces/srv/GetPlanningScene_Response";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::GetPlanningScene_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::srv::GetPlanningScene_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace appleproj_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetPlanningScene_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetPlanningScene_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetPlanningScene_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace appleproj_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use appleproj_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const appleproj_interfaces::srv::GetPlanningScene_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::srv::GetPlanningScene_Event & msg)
{
  return appleproj_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::srv::GetPlanningScene_Event>()
{
  return "appleproj_interfaces::srv::GetPlanningScene_Event";
}

template<>
inline const char * name<appleproj_interfaces::srv::GetPlanningScene_Event>()
{
  return "appleproj_interfaces/srv/GetPlanningScene_Event";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::GetPlanningScene_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Event>
  : std::integral_constant<bool, has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Request>::value && has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<appleproj_interfaces::srv::GetPlanningScene_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<appleproj_interfaces::srv::GetPlanningScene>()
{
  return "appleproj_interfaces::srv::GetPlanningScene";
}

template<>
inline const char * name<appleproj_interfaces::srv::GetPlanningScene>()
{
  return "appleproj_interfaces/srv/GetPlanningScene";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::GetPlanningScene>
  : std::integral_constant<
    bool,
    has_fixed_size<appleproj_interfaces::srv::GetPlanningScene_Request>::value &&
    has_fixed_size<appleproj_interfaces::srv::GetPlanningScene_Response>::value
  >
{
};

template<>
struct has_bounded_size<appleproj_interfaces::srv::GetPlanningScene>
  : std::integral_constant<
    bool,
    has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Request>::value &&
    has_bounded_size<appleproj_interfaces::srv::GetPlanningScene_Response>::value
  >
{
};

template<>
struct is_service<appleproj_interfaces::srv::GetPlanningScene>
  : std::true_type
{
};

template<>
struct is_service_request<appleproj_interfaces::srv::GetPlanningScene_Request>
  : std::true_type
{
};

template<>
struct is_service_response<appleproj_interfaces::srv::GetPlanningScene_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__GET_PLANNING_SCENE__TRAITS_HPP_
