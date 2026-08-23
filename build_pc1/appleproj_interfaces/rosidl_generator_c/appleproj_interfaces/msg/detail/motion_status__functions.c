// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:msg/MotionStatus.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/msg/detail/motion_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `current_state`
// Member `error_code`
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
appleproj_interfaces__msg__MotionStatus__init(appleproj_interfaces__msg__MotionStatus * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    appleproj_interfaces__msg__MotionStatus__fini(msg);
    return false;
  }
  // current_state
  if (!rosidl_runtime_c__String__init(&msg->current_state)) {
    appleproj_interfaces__msg__MotionStatus__fini(msg);
    return false;
  }
  // success
  // progress
  // error_code
  if (!rosidl_runtime_c__String__init(&msg->error_code)) {
    appleproj_interfaces__msg__MotionStatus__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    appleproj_interfaces__msg__MotionStatus__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__msg__MotionStatus__fini(appleproj_interfaces__msg__MotionStatus * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // current_state
  rosidl_runtime_c__String__fini(&msg->current_state);
  // success
  // progress
  // error_code
  rosidl_runtime_c__String__fini(&msg->error_code);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
appleproj_interfaces__msg__MotionStatus__are_equal(const appleproj_interfaces__msg__MotionStatus * lhs, const appleproj_interfaces__msg__MotionStatus * rhs)
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
  // current_state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_state), &(rhs->current_state)))
  {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // progress
  if (lhs->progress != rhs->progress) {
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
appleproj_interfaces__msg__MotionStatus__copy(
  const appleproj_interfaces__msg__MotionStatus * input,
  appleproj_interfaces__msg__MotionStatus * output)
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
  // current_state
  if (!rosidl_runtime_c__String__copy(
      &(input->current_state), &(output->current_state)))
  {
    return false;
  }
  // success
  output->success = input->success;
  // progress
  output->progress = input->progress;
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

appleproj_interfaces__msg__MotionStatus *
appleproj_interfaces__msg__MotionStatus__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__MotionStatus * msg = (appleproj_interfaces__msg__MotionStatus *)allocator.allocate(sizeof(appleproj_interfaces__msg__MotionStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__msg__MotionStatus));
  bool success = appleproj_interfaces__msg__MotionStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__msg__MotionStatus__destroy(appleproj_interfaces__msg__MotionStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__msg__MotionStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__msg__MotionStatus__Sequence__init(appleproj_interfaces__msg__MotionStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__MotionStatus * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__msg__MotionStatus)) {
      return false;
    }
    data = (appleproj_interfaces__msg__MotionStatus *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__msg__MotionStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__msg__MotionStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__msg__MotionStatus__fini(&data[i - 1]);
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
appleproj_interfaces__msg__MotionStatus__Sequence__fini(appleproj_interfaces__msg__MotionStatus__Sequence * array)
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
      appleproj_interfaces__msg__MotionStatus__fini(&array->data[i]);
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

appleproj_interfaces__msg__MotionStatus__Sequence *
appleproj_interfaces__msg__MotionStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__MotionStatus__Sequence * array = (appleproj_interfaces__msg__MotionStatus__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__msg__MotionStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__msg__MotionStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__msg__MotionStatus__Sequence__destroy(appleproj_interfaces__msg__MotionStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__msg__MotionStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__msg__MotionStatus__Sequence__are_equal(const appleproj_interfaces__msg__MotionStatus__Sequence * lhs, const appleproj_interfaces__msg__MotionStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__msg__MotionStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__msg__MotionStatus__Sequence__copy(
  const appleproj_interfaces__msg__MotionStatus__Sequence * input,
  appleproj_interfaces__msg__MotionStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__msg__MotionStatus)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__msg__MotionStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__msg__MotionStatus * data =
      (appleproj_interfaces__msg__MotionStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__msg__MotionStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__msg__MotionStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__msg__MotionStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
