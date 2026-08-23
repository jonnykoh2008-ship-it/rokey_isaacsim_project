// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:msg/ObstacleProxy.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/msg/detail/obstacle_proxy__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `obstacle_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `dimensions`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
appleproj_interfaces__msg__ObstacleProxy__init(appleproj_interfaces__msg__ObstacleProxy * msg)
{
  if (!msg) {
    return false;
  }
  // obstacle_id
  if (!rosidl_runtime_c__String__init(&msg->obstacle_id)) {
    appleproj_interfaces__msg__ObstacleProxy__fini(msg);
    return false;
  }
  // shape
  // obstacle_class
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    appleproj_interfaces__msg__ObstacleProxy__fini(msg);
    return false;
  }
  // dimensions
  if (!geometry_msgs__msg__Vector3__init(&msg->dimensions)) {
    appleproj_interfaces__msg__ObstacleProxy__fini(msg);
    return false;
  }
  // safety_margin
  return true;
}

void
appleproj_interfaces__msg__ObstacleProxy__fini(appleproj_interfaces__msg__ObstacleProxy * msg)
{
  if (!msg) {
    return;
  }
  // obstacle_id
  rosidl_runtime_c__String__fini(&msg->obstacle_id);
  // shape
  // obstacle_class
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // dimensions
  geometry_msgs__msg__Vector3__fini(&msg->dimensions);
  // safety_margin
}

bool
appleproj_interfaces__msg__ObstacleProxy__are_equal(const appleproj_interfaces__msg__ObstacleProxy * lhs, const appleproj_interfaces__msg__ObstacleProxy * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // obstacle_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->obstacle_id), &(rhs->obstacle_id)))
  {
    return false;
  }
  // shape
  if (lhs->shape != rhs->shape) {
    return false;
  }
  // obstacle_class
  if (lhs->obstacle_class != rhs->obstacle_class) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // dimensions
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->dimensions), &(rhs->dimensions)))
  {
    return false;
  }
  // safety_margin
  if (lhs->safety_margin != rhs->safety_margin) {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__msg__ObstacleProxy__copy(
  const appleproj_interfaces__msg__ObstacleProxy * input,
  appleproj_interfaces__msg__ObstacleProxy * output)
{
  if (!input || !output) {
    return false;
  }
  // obstacle_id
  if (!rosidl_runtime_c__String__copy(
      &(input->obstacle_id), &(output->obstacle_id)))
  {
    return false;
  }
  // shape
  output->shape = input->shape;
  // obstacle_class
  output->obstacle_class = input->obstacle_class;
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // dimensions
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->dimensions), &(output->dimensions)))
  {
    return false;
  }
  // safety_margin
  output->safety_margin = input->safety_margin;
  return true;
}

appleproj_interfaces__msg__ObstacleProxy *
appleproj_interfaces__msg__ObstacleProxy__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__ObstacleProxy * msg = (appleproj_interfaces__msg__ObstacleProxy *)allocator.allocate(sizeof(appleproj_interfaces__msg__ObstacleProxy), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__msg__ObstacleProxy));
  bool success = appleproj_interfaces__msg__ObstacleProxy__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__msg__ObstacleProxy__destroy(appleproj_interfaces__msg__ObstacleProxy * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__msg__ObstacleProxy__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__msg__ObstacleProxy__Sequence__init(appleproj_interfaces__msg__ObstacleProxy__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__ObstacleProxy * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__msg__ObstacleProxy)) {
      return false;
    }
    data = (appleproj_interfaces__msg__ObstacleProxy *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__msg__ObstacleProxy), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__msg__ObstacleProxy__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__msg__ObstacleProxy__fini(&data[i - 1]);
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
appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(appleproj_interfaces__msg__ObstacleProxy__Sequence * array)
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
      appleproj_interfaces__msg__ObstacleProxy__fini(&array->data[i]);
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

appleproj_interfaces__msg__ObstacleProxy__Sequence *
appleproj_interfaces__msg__ObstacleProxy__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__ObstacleProxy__Sequence * array = (appleproj_interfaces__msg__ObstacleProxy__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__msg__ObstacleProxy__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__msg__ObstacleProxy__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__msg__ObstacleProxy__Sequence__destroy(appleproj_interfaces__msg__ObstacleProxy__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__msg__ObstacleProxy__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__msg__ObstacleProxy__Sequence__are_equal(const appleproj_interfaces__msg__ObstacleProxy__Sequence * lhs, const appleproj_interfaces__msg__ObstacleProxy__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__msg__ObstacleProxy__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__msg__ObstacleProxy__Sequence__copy(
  const appleproj_interfaces__msg__ObstacleProxy__Sequence * input,
  appleproj_interfaces__msg__ObstacleProxy__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__msg__ObstacleProxy)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__msg__ObstacleProxy);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__msg__ObstacleProxy * data =
      (appleproj_interfaces__msg__ObstacleProxy *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__msg__ObstacleProxy__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__msg__ObstacleProxy__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__msg__ObstacleProxy__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
