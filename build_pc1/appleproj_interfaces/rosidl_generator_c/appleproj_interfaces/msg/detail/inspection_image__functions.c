// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:msg/InspectionImage.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/msg/detail/inspection_image__functions.h"

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
// Member `image`
#include "sensor_msgs/msg/detail/compressed_image__functions.h"

bool
appleproj_interfaces__msg__InspectionImage__init(appleproj_interfaces__msg__InspectionImage * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    appleproj_interfaces__msg__InspectionImage__fini(msg);
    return false;
  }
  // inspection_id
  if (!rosidl_runtime_c__String__init(&msg->inspection_id)) {
    appleproj_interfaces__msg__InspectionImage__fini(msg);
    return false;
  }
  // apple_id
  if (!rosidl_runtime_c__String__init(&msg->apple_id)) {
    appleproj_interfaces__msg__InspectionImage__fini(msg);
    return false;
  }
  // frame_index
  // total_frames
  // image
  if (!sensor_msgs__msg__CompressedImage__init(&msg->image)) {
    appleproj_interfaces__msg__InspectionImage__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__msg__InspectionImage__fini(appleproj_interfaces__msg__InspectionImage * msg)
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
  // frame_index
  // total_frames
  // image
  sensor_msgs__msg__CompressedImage__fini(&msg->image);
}

bool
appleproj_interfaces__msg__InspectionImage__are_equal(const appleproj_interfaces__msg__InspectionImage * lhs, const appleproj_interfaces__msg__InspectionImage * rhs)
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
  // frame_index
  if (lhs->frame_index != rhs->frame_index) {
    return false;
  }
  // total_frames
  if (lhs->total_frames != rhs->total_frames) {
    return false;
  }
  // image
  if (!sensor_msgs__msg__CompressedImage__are_equal(
      &(lhs->image), &(rhs->image)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__msg__InspectionImage__copy(
  const appleproj_interfaces__msg__InspectionImage * input,
  appleproj_interfaces__msg__InspectionImage * output)
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
  // frame_index
  output->frame_index = input->frame_index;
  // total_frames
  output->total_frames = input->total_frames;
  // image
  if (!sensor_msgs__msg__CompressedImage__copy(
      &(input->image), &(output->image)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__msg__InspectionImage *
appleproj_interfaces__msg__InspectionImage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__InspectionImage * msg = (appleproj_interfaces__msg__InspectionImage *)allocator.allocate(sizeof(appleproj_interfaces__msg__InspectionImage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__msg__InspectionImage));
  bool success = appleproj_interfaces__msg__InspectionImage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__msg__InspectionImage__destroy(appleproj_interfaces__msg__InspectionImage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__msg__InspectionImage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__msg__InspectionImage__Sequence__init(appleproj_interfaces__msg__InspectionImage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__InspectionImage * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__msg__InspectionImage)) {
      return false;
    }
    data = (appleproj_interfaces__msg__InspectionImage *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__msg__InspectionImage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__msg__InspectionImage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__msg__InspectionImage__fini(&data[i - 1]);
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
appleproj_interfaces__msg__InspectionImage__Sequence__fini(appleproj_interfaces__msg__InspectionImage__Sequence * array)
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
      appleproj_interfaces__msg__InspectionImage__fini(&array->data[i]);
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

appleproj_interfaces__msg__InspectionImage__Sequence *
appleproj_interfaces__msg__InspectionImage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__msg__InspectionImage__Sequence * array = (appleproj_interfaces__msg__InspectionImage__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__msg__InspectionImage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__msg__InspectionImage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__msg__InspectionImage__Sequence__destroy(appleproj_interfaces__msg__InspectionImage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__msg__InspectionImage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__msg__InspectionImage__Sequence__are_equal(const appleproj_interfaces__msg__InspectionImage__Sequence * lhs, const appleproj_interfaces__msg__InspectionImage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__msg__InspectionImage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__msg__InspectionImage__Sequence__copy(
  const appleproj_interfaces__msg__InspectionImage__Sequence * input,
  appleproj_interfaces__msg__InspectionImage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__msg__InspectionImage)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__msg__InspectionImage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__msg__InspectionImage * data =
      (appleproj_interfaces__msg__InspectionImage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__msg__InspectionImage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__msg__InspectionImage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__msg__InspectionImage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
