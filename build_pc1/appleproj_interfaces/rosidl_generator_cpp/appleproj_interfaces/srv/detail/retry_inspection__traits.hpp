// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from appleproj_interfaces:srv/RetryInspection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "appleproj_interfaces/srv/retry_inspection.hpp"


#ifndef APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__TRAITS_HPP_
#define APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "appleproj_interfaces/srv/detail/retry_inspection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace appleproj_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const RetryInspection_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: inspection_id
  {
    out << "inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.inspection_id, out);
    out << ", ";
  }

  // member: apple_id
  {
    out << "apple_id: ";
    rosidl_generator_traits::value_to_yaml(msg.apple_id, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RetryInspection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: inspection_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.inspection_id, out);
    out << "\n";
  }

  // member: apple_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "apple_id: ";
    rosidl_generator_traits::value_to_yaml(msg.apple_id, out);
    out << "\n";
  }

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RetryInspection_Request & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::srv::RetryInspection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::srv::RetryInspection_Request & msg)
{
  return appleproj_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::srv::RetryInspection_Request>()
{
  return "appleproj_interfaces::srv::RetryInspection_Request";
}

template<>
inline const char * name<appleproj_interfaces::srv::RetryInspection_Request>()
{
  return "appleproj_interfaces/srv/RetryInspection_Request";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::RetryInspection_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::srv::RetryInspection_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::srv::RetryInspection_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace appleproj_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const RetryInspection_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: new_inspection_id
  {
    out << "new_inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.new_inspection_id, out);
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
  const RetryInspection_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: new_inspection_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "new_inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.new_inspection_id, out);
    out << "\n";
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

inline std::string to_yaml(const RetryInspection_Response & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::srv::RetryInspection_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::srv::RetryInspection_Response & msg)
{
  return appleproj_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::srv::RetryInspection_Response>()
{
  return "appleproj_interfaces::srv::RetryInspection_Response";
}

template<>
inline const char * name<appleproj_interfaces::srv::RetryInspection_Response>()
{
  return "appleproj_interfaces/srv/RetryInspection_Response";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::RetryInspection_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::srv::RetryInspection_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<appleproj_interfaces::srv::RetryInspection_Response>
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
  const RetryInspection_Event & msg,
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
  const RetryInspection_Event & msg,
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

inline std::string to_yaml(const RetryInspection_Event & msg, bool use_flow_style = false)
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
  const appleproj_interfaces::srv::RetryInspection_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  appleproj_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use appleproj_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const appleproj_interfaces::srv::RetryInspection_Event & msg)
{
  return appleproj_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<appleproj_interfaces::srv::RetryInspection_Event>()
{
  return "appleproj_interfaces::srv::RetryInspection_Event";
}

template<>
inline const char * name<appleproj_interfaces::srv::RetryInspection_Event>()
{
  return "appleproj_interfaces/srv/RetryInspection_Event";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::RetryInspection_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<appleproj_interfaces::srv::RetryInspection_Event>
  : std::integral_constant<bool, has_bounded_size<appleproj_interfaces::srv::RetryInspection_Request>::value && has_bounded_size<appleproj_interfaces::srv::RetryInspection_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<appleproj_interfaces::srv::RetryInspection_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<appleproj_interfaces::srv::RetryInspection>()
{
  return "appleproj_interfaces::srv::RetryInspection";
}

template<>
inline const char * name<appleproj_interfaces::srv::RetryInspection>()
{
  return "appleproj_interfaces/srv/RetryInspection";
}

template<>
struct has_fixed_size<appleproj_interfaces::srv::RetryInspection>
  : std::integral_constant<
    bool,
    has_fixed_size<appleproj_interfaces::srv::RetryInspection_Request>::value &&
    has_fixed_size<appleproj_interfaces::srv::RetryInspection_Response>::value
  >
{
};

template<>
struct has_bounded_size<appleproj_interfaces::srv::RetryInspection>
  : std::integral_constant<
    bool,
    has_bounded_size<appleproj_interfaces::srv::RetryInspection_Request>::value &&
    has_bounded_size<appleproj_interfaces::srv::RetryInspection_Response>::value
  >
{
};

template<>
struct is_service<appleproj_interfaces::srv::RetryInspection>
  : std::true_type
{
};

template<>
struct is_service_request<appleproj_interfaces::srv::RetryInspection_Request>
  : std::true_type
{
};

template<>
struct is_service_response<appleproj_interfaces::srv::RetryInspection_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // APPLEPROJ_INTERFACES__SRV__DETAIL__RETRY_INSPECTION__TRAITS_HPP_
