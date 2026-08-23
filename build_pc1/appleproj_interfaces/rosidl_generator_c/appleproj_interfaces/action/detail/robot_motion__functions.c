// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:action/RobotMotion.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/action/detail/robot_motion__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `target_pose`
// Member `waypoints`
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"

bool
appleproj_interfaces__action__RobotMotion_Goal__init(appleproj_interfaces__action__RobotMotion_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // motion_type
  // target_pose
  if (!geometry_msgs__msg__PoseStamped__init(&msg->target_pose)) {
    appleproj_interfaces__action__RobotMotion_Goal__fini(msg);
    return false;
  }
  // reset_id
  // scene_version
  // waypoints
  if (!geometry_msgs__msg__PoseStamped__Sequence__init(&msg->waypoints, 0)) {
    appleproj_interfaces__action__RobotMotion_Goal__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_Goal__fini(appleproj_interfaces__action__RobotMotion_Goal * msg)
{
  if (!msg) {
    return;
  }
  // motion_type
  // target_pose
  geometry_msgs__msg__PoseStamped__fini(&msg->target_pose);
  // reset_id
  // scene_version
  // waypoints
  geometry_msgs__msg__PoseStamped__Sequence__fini(&msg->waypoints);
}

bool
appleproj_interfaces__action__RobotMotion_Goal__are_equal(const appleproj_interfaces__action__RobotMotion_Goal * lhs, const appleproj_interfaces__action__RobotMotion_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // motion_type
  if (lhs->motion_type != rhs->motion_type) {
    return false;
  }
  // target_pose
  if (!geometry_msgs__msg__PoseStamped__are_equal(
      &(lhs->target_pose), &(rhs->target_pose)))
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
  // waypoints
  if (!geometry_msgs__msg__PoseStamped__Sequence__are_equal(
      &(lhs->waypoints), &(rhs->waypoints)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_Goal__copy(
  const appleproj_interfaces__action__RobotMotion_Goal * input,
  appleproj_interfaces__action__RobotMotion_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // motion_type
  output->motion_type = input->motion_type;
  // target_pose
  if (!geometry_msgs__msg__PoseStamped__copy(
      &(input->target_pose), &(output->target_pose)))
  {
    return false;
  }
  // reset_id
  output->reset_id = input->reset_id;
  // scene_version
  output->scene_version = input->scene_version;
  // waypoints
  if (!geometry_msgs__msg__PoseStamped__Sequence__copy(
      &(input->waypoints), &(output->waypoints)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_Goal *
appleproj_interfaces__action__RobotMotion_Goal__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Goal * msg = (appleproj_interfaces__action__RobotMotion_Goal *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_Goal));
  bool success = appleproj_interfaces__action__RobotMotion_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_Goal__destroy(appleproj_interfaces__action__RobotMotion_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_Goal__Sequence__init(appleproj_interfaces__action__RobotMotion_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Goal * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_Goal)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_Goal *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_Goal__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_Goal__Sequence__fini(appleproj_interfaces__action__RobotMotion_Goal__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_Goal__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_Goal__Sequence *
appleproj_interfaces__action__RobotMotion_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Goal__Sequence * array = (appleproj_interfaces__action__RobotMotion_Goal__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_Goal__Sequence__destroy(appleproj_interfaces__action__RobotMotion_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_Goal__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_Goal__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_Goal__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_Goal__Sequence * input,
  appleproj_interfaces__action__RobotMotion_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_Goal)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_Goal * data =
      (appleproj_interfaces__action__RobotMotion_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `error_code`
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
appleproj_interfaces__action__RobotMotion_Result__init(appleproj_interfaces__action__RobotMotion_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // error_code
  if (!rosidl_runtime_c__String__init(&msg->error_code)) {
    appleproj_interfaces__action__RobotMotion_Result__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    appleproj_interfaces__action__RobotMotion_Result__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_Result__fini(appleproj_interfaces__action__RobotMotion_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // error_code
  rosidl_runtime_c__String__fini(&msg->error_code);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
appleproj_interfaces__action__RobotMotion_Result__are_equal(const appleproj_interfaces__action__RobotMotion_Result * lhs, const appleproj_interfaces__action__RobotMotion_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // error_code
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error_code), &(rhs->error_code)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_Result__copy(
  const appleproj_interfaces__action__RobotMotion_Result * input,
  appleproj_interfaces__action__RobotMotion_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // error_code
  if (!rosidl_runtime_c__String__copy(
      &(input->error_code), &(output->error_code)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_Result *
appleproj_interfaces__action__RobotMotion_Result__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Result * msg = (appleproj_interfaces__action__RobotMotion_Result *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_Result));
  bool success = appleproj_interfaces__action__RobotMotion_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_Result__destroy(appleproj_interfaces__action__RobotMotion_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_Result__Sequence__init(appleproj_interfaces__action__RobotMotion_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Result * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_Result)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_Result *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_Result__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_Result__Sequence__fini(appleproj_interfaces__action__RobotMotion_Result__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_Result__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_Result__Sequence *
appleproj_interfaces__action__RobotMotion_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Result__Sequence * array = (appleproj_interfaces__action__RobotMotion_Result__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_Result__Sequence__destroy(appleproj_interfaces__action__RobotMotion_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_Result__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_Result__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_Result__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_Result__Sequence * input,
  appleproj_interfaces__action__RobotMotion_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_Result)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_Result * data =
      (appleproj_interfaces__action__RobotMotion_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `current_state`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
appleproj_interfaces__action__RobotMotion_Feedback__init(appleproj_interfaces__action__RobotMotion_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // current_state
  if (!rosidl_runtime_c__String__init(&msg->current_state)) {
    appleproj_interfaces__action__RobotMotion_Feedback__fini(msg);
    return false;
  }
  // progress
  return true;
}

void
appleproj_interfaces__action__RobotMotion_Feedback__fini(appleproj_interfaces__action__RobotMotion_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // current_state
  rosidl_runtime_c__String__fini(&msg->current_state);
  // progress
}

bool
appleproj_interfaces__action__RobotMotion_Feedback__are_equal(const appleproj_interfaces__action__RobotMotion_Feedback * lhs, const appleproj_interfaces__action__RobotMotion_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // current_state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_state), &(rhs->current_state)))
  {
    return false;
  }
  // progress
  if (lhs->progress != rhs->progress) {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_Feedback__copy(
  const appleproj_interfaces__action__RobotMotion_Feedback * input,
  appleproj_interfaces__action__RobotMotion_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // current_state
  if (!rosidl_runtime_c__String__copy(
      &(input->current_state), &(output->current_state)))
  {
    return false;
  }
  // progress
  output->progress = input->progress;
  return true;
}

appleproj_interfaces__action__RobotMotion_Feedback *
appleproj_interfaces__action__RobotMotion_Feedback__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Feedback * msg = (appleproj_interfaces__action__RobotMotion_Feedback *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_Feedback));
  bool success = appleproj_interfaces__action__RobotMotion_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_Feedback__destroy(appleproj_interfaces__action__RobotMotion_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_Feedback__Sequence__init(appleproj_interfaces__action__RobotMotion_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Feedback * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_Feedback)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_Feedback *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_Feedback__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_Feedback__Sequence__fini(appleproj_interfaces__action__RobotMotion_Feedback__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_Feedback__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_Feedback__Sequence *
appleproj_interfaces__action__RobotMotion_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_Feedback__Sequence * array = (appleproj_interfaces__action__RobotMotion_Feedback__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_Feedback__Sequence__destroy(appleproj_interfaces__action__RobotMotion_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_Feedback__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_Feedback__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_Feedback__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_Feedback__Sequence * input,
  appleproj_interfaces__action__RobotMotion_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_Feedback)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_Feedback * data =
      (appleproj_interfaces__action__RobotMotion_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Request__init(appleproj_interfaces__action__RobotMotion_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!appleproj_interfaces__action__RobotMotion_Goal__init(&msg->goal)) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(appleproj_interfaces__action__RobotMotion_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  appleproj_interfaces__action__RobotMotion_Goal__fini(&msg->goal);
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Request__are_equal(const appleproj_interfaces__action__RobotMotion_SendGoal_Request * lhs, const appleproj_interfaces__action__RobotMotion_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!appleproj_interfaces__action__RobotMotion_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Request__copy(
  const appleproj_interfaces__action__RobotMotion_SendGoal_Request * input,
  appleproj_interfaces__action__RobotMotion_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!appleproj_interfaces__action__RobotMotion_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_SendGoal_Request *
appleproj_interfaces__action__RobotMotion_SendGoal_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Request * msg = (appleproj_interfaces__action__RobotMotion_SendGoal_Request *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request));
  bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Request__destroy(appleproj_interfaces__action__RobotMotion_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__init(appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_SendGoal_Request *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__fini(appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence *
appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * array = (appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__destroy(appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * input,
  appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_SendGoal_Request * data =
      (appleproj_interfaces__action__RobotMotion_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Response__init(appleproj_interfaces__action__RobotMotion_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Response__fini(appleproj_interfaces__action__RobotMotion_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Response__are_equal(const appleproj_interfaces__action__RobotMotion_SendGoal_Response * lhs, const appleproj_interfaces__action__RobotMotion_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Response__copy(
  const appleproj_interfaces__action__RobotMotion_SendGoal_Response * input,
  appleproj_interfaces__action__RobotMotion_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_SendGoal_Response *
appleproj_interfaces__action__RobotMotion_SendGoal_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Response * msg = (appleproj_interfaces__action__RobotMotion_SendGoal_Response *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response));
  bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Response__destroy(appleproj_interfaces__action__RobotMotion_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__init(appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_SendGoal_Response *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_SendGoal_Response__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__fini(appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_SendGoal_Response__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence *
appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * array = (appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__destroy(appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * input,
  appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_SendGoal_Response * data =
      (appleproj_interfaces__action__RobotMotion_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Event__init(appleproj_interfaces__action__RobotMotion_SendGoal_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(msg);
    return false;
  }
  // request
  if (!appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__init(&msg->request, 0)) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(msg);
    return false;
  }
  // response
  if (!appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__init(&msg->response, 0)) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(appleproj_interfaces__action__RobotMotion_SendGoal_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__fini(&msg->request);
  // response
  appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__fini(&msg->response);
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Event__are_equal(const appleproj_interfaces__action__RobotMotion_SendGoal_Event * lhs, const appleproj_interfaces__action__RobotMotion_SendGoal_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Event__copy(
  const appleproj_interfaces__action__RobotMotion_SendGoal_Event * input,
  appleproj_interfaces__action__RobotMotion_SendGoal_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!appleproj_interfaces__action__RobotMotion_SendGoal_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__action__RobotMotion_SendGoal_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_SendGoal_Event *
appleproj_interfaces__action__RobotMotion_SendGoal_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Event * msg = (appleproj_interfaces__action__RobotMotion_SendGoal_Event *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event));
  bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Event__destroy(appleproj_interfaces__action__RobotMotion_SendGoal_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__init(appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_SendGoal_Event *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__fini(appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence *
appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * array = (appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__destroy(appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_SendGoal_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * input,
  appleproj_interfaces__action__RobotMotion_SendGoal_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_SendGoal_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_SendGoal_Event * data =
      (appleproj_interfaces__action__RobotMotion_SendGoal_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_SendGoal_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_SendGoal_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_SendGoal_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
appleproj_interfaces__action__RobotMotion_GetResult_Request__init(appleproj_interfaces__action__RobotMotion_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    appleproj_interfaces__action__RobotMotion_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Request__fini(appleproj_interfaces__action__RobotMotion_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Request__are_equal(const appleproj_interfaces__action__RobotMotion_GetResult_Request * lhs, const appleproj_interfaces__action__RobotMotion_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Request__copy(
  const appleproj_interfaces__action__RobotMotion_GetResult_Request * input,
  appleproj_interfaces__action__RobotMotion_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_GetResult_Request *
appleproj_interfaces__action__RobotMotion_GetResult_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Request * msg = (appleproj_interfaces__action__RobotMotion_GetResult_Request *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request));
  bool success = appleproj_interfaces__action__RobotMotion_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Request__destroy(appleproj_interfaces__action__RobotMotion_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__init(appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_GetResult_Request *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_GetResult_Request__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__fini(appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_GetResult_Request__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence *
appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * array = (appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__destroy(appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * input,
  appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_GetResult_Request * data =
      (appleproj_interfaces__action__RobotMotion_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"

bool
appleproj_interfaces__action__RobotMotion_GetResult_Response__init(appleproj_interfaces__action__RobotMotion_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!appleproj_interfaces__action__RobotMotion_Result__init(&msg->result)) {
    appleproj_interfaces__action__RobotMotion_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Response__fini(appleproj_interfaces__action__RobotMotion_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  appleproj_interfaces__action__RobotMotion_Result__fini(&msg->result);
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Response__are_equal(const appleproj_interfaces__action__RobotMotion_GetResult_Response * lhs, const appleproj_interfaces__action__RobotMotion_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!appleproj_interfaces__action__RobotMotion_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Response__copy(
  const appleproj_interfaces__action__RobotMotion_GetResult_Response * input,
  appleproj_interfaces__action__RobotMotion_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!appleproj_interfaces__action__RobotMotion_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_GetResult_Response *
appleproj_interfaces__action__RobotMotion_GetResult_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Response * msg = (appleproj_interfaces__action__RobotMotion_GetResult_Response *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response));
  bool success = appleproj_interfaces__action__RobotMotion_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Response__destroy(appleproj_interfaces__action__RobotMotion_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__init(appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_GetResult_Response *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_GetResult_Response__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__fini(appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_GetResult_Response__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence *
appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * array = (appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__destroy(appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * input,
  appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_GetResult_Response * data =
      (appleproj_interfaces__action__RobotMotion_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
// already included above
// #include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"

bool
appleproj_interfaces__action__RobotMotion_GetResult_Event__init(appleproj_interfaces__action__RobotMotion_GetResult_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(msg);
    return false;
  }
  // request
  if (!appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__init(&msg->request, 0)) {
    appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(msg);
    return false;
  }
  // response
  if (!appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__init(&msg->response, 0)) {
    appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(appleproj_interfaces__action__RobotMotion_GetResult_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__fini(&msg->request);
  // response
  appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__fini(&msg->response);
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Event__are_equal(const appleproj_interfaces__action__RobotMotion_GetResult_Event * lhs, const appleproj_interfaces__action__RobotMotion_GetResult_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Event__copy(
  const appleproj_interfaces__action__RobotMotion_GetResult_Event * input,
  appleproj_interfaces__action__RobotMotion_GetResult_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!appleproj_interfaces__action__RobotMotion_GetResult_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__action__RobotMotion_GetResult_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_GetResult_Event *
appleproj_interfaces__action__RobotMotion_GetResult_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Event * msg = (appleproj_interfaces__action__RobotMotion_GetResult_Event *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event));
  bool success = appleproj_interfaces__action__RobotMotion_GetResult_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Event__destroy(appleproj_interfaces__action__RobotMotion_GetResult_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__init(appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_GetResult_Event *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_GetResult_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__fini(appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence *
appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * array = (appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__destroy(appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_GetResult_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * input,
  appleproj_interfaces__action__RobotMotion_GetResult_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_GetResult_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_GetResult_Event * data =
      (appleproj_interfaces__action__RobotMotion_GetResult_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_GetResult_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_GetResult_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_GetResult_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "appleproj_interfaces/action/detail/robot_motion__functions.h"

bool
appleproj_interfaces__action__RobotMotion_FeedbackMessage__init(appleproj_interfaces__action__RobotMotion_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!appleproj_interfaces__action__RobotMotion_Feedback__init(&msg->feedback)) {
    appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(appleproj_interfaces__action__RobotMotion_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  appleproj_interfaces__action__RobotMotion_Feedback__fini(&msg->feedback);
}

bool
appleproj_interfaces__action__RobotMotion_FeedbackMessage__are_equal(const appleproj_interfaces__action__RobotMotion_FeedbackMessage * lhs, const appleproj_interfaces__action__RobotMotion_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!appleproj_interfaces__action__RobotMotion_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_FeedbackMessage__copy(
  const appleproj_interfaces__action__RobotMotion_FeedbackMessage * input,
  appleproj_interfaces__action__RobotMotion_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!appleproj_interfaces__action__RobotMotion_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__action__RobotMotion_FeedbackMessage *
appleproj_interfaces__action__RobotMotion_FeedbackMessage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_FeedbackMessage * msg = (appleproj_interfaces__action__RobotMotion_FeedbackMessage *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage));
  bool success = appleproj_interfaces__action__RobotMotion_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__action__RobotMotion_FeedbackMessage__destroy(appleproj_interfaces__action__RobotMotion_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__init(appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_FeedbackMessage * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage)) {
      return false;
    }
    data = (appleproj_interfaces__action__RobotMotion_FeedbackMessage *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__action__RobotMotion_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(&data[i - 1]);
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
appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__fini(appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * array)
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
      appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(&array->data[i]);
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

appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence *
appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * array = (appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__destroy(appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__are_equal(const appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * lhs, const appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence__copy(
  const appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * input,
  appleproj_interfaces__action__RobotMotion_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__action__RobotMotion_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__action__RobotMotion_FeedbackMessage * data =
      (appleproj_interfaces__action__RobotMotion_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__action__RobotMotion_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__action__RobotMotion_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__action__RobotMotion_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
