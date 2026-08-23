# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target appleproj_interfaces::appleproj_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${appleproj_interfaces_TARGETS}.
if(appleproj_interfaces_TARGETS AND NOT TARGET appleproj_interfaces::appleproj_interfaces)
  add_library(appleproj_interfaces::appleproj_interfaces INTERFACE IMPORTED)
  set_target_properties(appleproj_interfaces::appleproj_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${appleproj_interfaces_TARGETS}")
endif()
