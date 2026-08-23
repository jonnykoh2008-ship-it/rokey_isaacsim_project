// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `robot_base_pose`
// Member `robot_tcp_pose`
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"
// Member `obstacles`
#include "appleproj_interfaces/msg/detail/obstacle_proxy__functions.h"

bool
appleproj_interfaces__msg__PlanningScene__init(appleproj_interfaces__msg__PlanningScene * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    appleproj_interfaces__msg__PlanningScene__fini(msg);
    return false;
  }
  // reset_id
  // scene_version
  // robot_base_pose
  if (!geometry_msgs__msg__PoseStamped__init(&msg->robot_base_pose)) {
    appleproj_interfaces__msg__PlanningScene__fini(msg);
    return false;
  }
  // robot_tcp_pose
  if (!geometry_msgs__msg__PoseStamped__init(&msg->robot_tcp_pose)) {
    appleproj_interfaces__msg__PlanningScene__fini(msg);
    return false;
  }
  // obstacles
  if (!appleproj_interfaces__msg__ObstacleProxy__Sequence__init(&msg->obstacles, 0)) {
    appleproj_interfaces__msg__PlanningScene__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__msg__PlanningScene__fini(appleproj_interfaces__msg__PlanningScene * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // reset_id
  // scene_version
  // robot_base_pose
  geometry_msgs__msg__PoseStamped__fini(&msg->robot_base_pose);
  // robot_tcp_pose
  geometry_msgs__msg__PoseStamped__fini(&msg->robot_tcp_pose);
  // obstacles
  appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(&msg->obstacles);
}

bool
appleproj_interfaces__msg__PlanningScene__are_equal(const appleproj_interfaces__msg__PlanningScene * lhs, const appleproj_interfaces__msg__PlanningScene * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // reset_id
  if (lhs->reset_id != rhs->reset_id) {
    return false;
  }
  // scene_version
  if (lhs->scene_version != rhs->scene_version) {
    return false;
  }
  // robot_base_pose
  if (!geometry_msgs__msg__PoseStamped__are_equal(
      &(lhs->robot_base_pose), &(rhs->robot_base_pose)))
  {
    return false;
  }
  // robot_tcp_pose
  if (!geometry_msgs__msg__PoseStamped__are_equal(
      &(lhs->robot_tcp_pose), &(rhs->robot_tcp_pose)))
  {
    return false;
  }
  // obstacles
  if (!appleproj_interfaces__msg__ObstacleProxy__Sequence__are_equal(
      &(lhs->obstacles), &(rhs->obstacles)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__msg__PlanningScene__copy(
  const appleproj_interfaces__msg__PlanningScene * input,
  appleproj_interfaces__msg__PlanningScene * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // reset_id
  output->reset_id = input->reset_id;
  // scene_version
  output->scene_version = input->scene_version;
  // robot_base_pose
  if (!geometry_msgs__msg__PoseStamped__copy(
      &(input->robot_base_pose), &(output->robot_base_pose)))
  {
    return false;
  }
  // robot_tcp_pose
  if (!geometry_msgs__msg__PoseStamped__copy(
      &(input->robot_tcp_pose), &(output->robot_tcp_pose)))
  {
    return false;
  }
  // obstacles
  if (!appleproj_interfaces__msg__ObstacleProxy__Sequence__copy(
      &(input->obstacles), &(output->obstacles)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__msg__PlanningScene *
appleproj_interfaces__msg__PlanningScene__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__PlanningScene * msg = (appleproj_interfaces__msg__PlanningScene *)allocator.allocate(sizeof(appleproj_interfaces__msg__PlanningScene), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__msg__PlanningScene));
  bool success = appleproj_interfaces__msg__PlanningScene__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__msg__PlanningScene__destroy(appleproj_interfaces__msg__PlanningScene * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__msg__PlanningScene__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__msg__PlanningScene__Sequence__init(appleproj_interfaces__msg__PlanningScene__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__PlanningScene * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__msg__PlanningScene)) {
      return false;
    }
    data = (appleproj_interfaces__msg__PlanningScene *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__msg__PlanningScene), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__msg__PlanningScene__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__msg__PlanningScene__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
appleproj_interfaces__msg__PlanningScene__Sequence__fini(appleproj_interfaces__msg__PlanningScene__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      appleproj_interfaces__msg__PlanningScene__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

appleproj_interfaces__msg__PlanningScene__Sequence *
appleproj_interfaces__msg__PlanningScene__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__PlanningScene__Sequence * array = (appleproj_interfaces__msg__PlanningScene__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__msg__PlanningScene__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__msg__PlanningScene__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__msg__PlanningScene__Sequence__destroy(appleproj_interfaces__msg__PlanningScene__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__msg__PlanningScene__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__msg__PlanningScene__Sequence__are_equal(const appleproj_interfaces__msg__PlanningScene__Sequence * lhs, const appleproj_interfaces__msg__PlanningScene__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__msg__PlanningScene__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__msg__PlanningScene__Sequence__copy(
  const appleproj_interfaces__msg__PlanningScene__Sequence * input,
  appleproj_interfaces__msg__PlanningScene__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__msg__PlanningScene)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__msg__PlanningScene);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__msg__PlanningScene * data =
      (appleproj_interfaces__msg__PlanningScene *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__msg__PlanningScene__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__msg__PlanningScene__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__msg__PlanningScene__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
