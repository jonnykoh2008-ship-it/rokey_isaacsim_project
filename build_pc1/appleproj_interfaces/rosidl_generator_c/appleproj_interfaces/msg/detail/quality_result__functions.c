// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:msg/QualityResult.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/msg/detail/quality_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `inspection_id`
// Member `apple_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `frame_indices`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `result_timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
appleproj_interfaces__msg__QualityResult__init(appleproj_interfaces__msg__QualityResult * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    appleproj_interfaces__msg__QualityResult__fini(msg);
    return false;
  }
  // inspection_id
  if (!rosidl_runtime_c__String__init(&msg->inspection_id)) {
    appleproj_interfaces__msg__QualityResult__fini(msg);
    return false;
  }
  // apple_id
  if (!rosidl_runtime_c__String__init(&msg->apple_id)) {
    appleproj_interfaces__msg__QualityResult__fini(msg);
    return false;
  }
  // grade
  // confidence
  // color_ratio
  // diameter_mm
  // damage_area_cm2
  // frames_used
  // frame_indices
  if (!rosidl_runtime_c__uint16__Sequence__init(&msg->frame_indices, 0)) {
    appleproj_interfaces__msg__QualityResult__fini(msg);
    return false;
  }
  // result_timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->result_timestamp)) {
    appleproj_interfaces__msg__QualityResult__fini(msg);
    return false;
  }
  // status
  return true;
}

void
appleproj_interfaces__msg__QualityResult__fini(appleproj_interfaces__msg__QualityResult * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // inspection_id
  rosidl_runtime_c__String__fini(&msg->inspection_id);
  // apple_id
  rosidl_runtime_c__String__fini(&msg->apple_id);
  // grade
  // confidence
  // color_ratio
  // diameter_mm
  // damage_area_cm2
  // frames_used
  // frame_indices
  rosidl_runtime_c__uint16__Sequence__fini(&msg->frame_indices);
  // result_timestamp
  builtin_interfaces__msg__Time__fini(&msg->result_timestamp);
  // status
}

bool
appleproj_interfaces__msg__QualityResult__are_equal(const appleproj_interfaces__msg__QualityResult * lhs, const appleproj_interfaces__msg__QualityResult * rhs)
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
  // inspection_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->inspection_id), &(rhs->inspection_id)))
  {
    return false;
  }
  // apple_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->apple_id), &(rhs->apple_id)))
  {
    return false;
  }
  // grade
  if (lhs->grade != rhs->grade) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // color_ratio
  if (lhs->color_ratio != rhs->color_ratio) {
    return false;
  }
  // diameter_mm
  if (lhs->diameter_mm != rhs->diameter_mm) {
    return false;
  }
  // damage_area_cm2
  if (lhs->damage_area_cm2 != rhs->damage_area_cm2) {
    return false;
  }
  // frames_used
  if (lhs->frames_used != rhs->frames_used) {
    return false;
  }
  // frame_indices
  if (!rosidl_runtime_c__uint16__Sequence__are_equal(
      &(lhs->frame_indices), &(rhs->frame_indices)))
  {
    return false;
  }
  // result_timestamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->result_timestamp), &(rhs->result_timestamp)))
  {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__msg__QualityResult__copy(
  const appleproj_interfaces__msg__QualityResult * input,
  appleproj_interfaces__msg__QualityResult * output)
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
  // inspection_id
  if (!rosidl_runtime_c__String__copy(
      &(input->inspection_id), &(output->inspection_id)))
  {
    return false;
  }
  // apple_id
  if (!rosidl_runtime_c__String__copy(
      &(input->apple_id), &(output->apple_id)))
  {
    return false;
  }
  // grade
  output->grade = input->grade;
  // confidence
  output->confidence = input->confidence;
  // color_ratio
  output->color_ratio = input->color_ratio;
  // diameter_mm
  output->diameter_mm = input->diameter_mm;
  // damage_area_cm2
  output->damage_area_cm2 = input->damage_area_cm2;
  // frames_used
  output->frames_used = input->frames_used;
  // frame_indices
  if (!rosidl_runtime_c__uint16__Sequence__copy(
      &(input->frame_indices), &(output->frame_indices)))
  {
    return false;
  }
  // result_timestamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->result_timestamp), &(output->result_timestamp)))
  {
    return false;
  }
  // status
  output->status = input->status;
  return true;
}

appleproj_interfaces__msg__QualityResult *
appleproj_interfaces__msg__QualityResult__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__QualityResult * msg = (appleproj_interfaces__msg__QualityResult *)allocator.allocate(sizeof(appleproj_interfaces__msg__QualityResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__msg__QualityResult));
  bool success = appleproj_interfaces__msg__QualityResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__msg__QualityResult__destroy(appleproj_interfaces__msg__QualityResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__msg__QualityResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__msg__QualityResult__Sequence__init(appleproj_interfaces__msg__QualityResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__QualityResult * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__msg__QualityResult)) {
      return false;
    }
    data = (appleproj_interfaces__msg__QualityResult *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__msg__QualityResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__msg__QualityResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__msg__QualityResult__fini(&data[i - 1]);
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
appleproj_interfaces__msg__QualityResult__Sequence__fini(appleproj_interfaces__msg__QualityResult__Sequence * array)
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
      appleproj_interfaces__msg__QualityResult__fini(&array->data[i]);
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

appleproj_interfaces__msg__QualityResult__Sequence *
appleproj_interfaces__msg__QualityResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__QualityResult__Sequence * array = (appleproj_interfaces__msg__QualityResult__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__msg__QualityResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__msg__QualityResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__msg__QualityResult__Sequence__destroy(appleproj_interfaces__msg__QualityResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__msg__QualityResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__msg__QualityResult__Sequence__are_equal(const appleproj_interfaces__msg__QualityResult__Sequence * lhs, const appleproj_interfaces__msg__QualityResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__msg__QualityResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__msg__QualityResult__Sequence__copy(
  const appleproj_interfaces__msg__QualityResult__Sequence * input,
  appleproj_interfaces__msg__QualityResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__msg__QualityResult)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__msg__QualityResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__msg__QualityResult * data =
      (appleproj_interfaces__msg__QualityResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__msg__QualityResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__msg__QualityResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__msg__QualityResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
