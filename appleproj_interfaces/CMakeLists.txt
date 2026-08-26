cmake_minimum_required(VERSION 3.8)
project(appleproj_interfaces)

find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CheckpointEvent.msg"
  "msg/HarvestPerceptionStatus.msg"
  "msg/HarvestTarget.msg"
  "msg/InspectionCompleted.msg"
  "msg/InspectionImage.msg"
  "msg/MotionStatus.msg"
  "msg/ObstacleProxy.msg"
  "msg/PlaceCoordinatorStatus.msg"
  "msg/PlanningScene.msg"
  "msg/QualityResult.msg"
  "msg/SimulationState.msg"
  "msg/SortStatus.msg"
  "srv/GetPlanningScene.srv"
  "srv/PlaceCommand.srv"
  "srv/RetryInspection.srv"
  "srv/SortCommand.srv"
  "action/RobotMotion.action"
  DEPENDENCIES
    builtin_interfaces
    geometry_msgs
    sensor_msgs
    std_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
