// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:srv/RetryInspection.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/srv/detail/retry_inspection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `inspection_id`
// Member `apple_id`
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"

bool
appleproj_interfaces__srv__RetryInspection_Request__init(appleproj_interfaces__srv__RetryInspection_Request * msg)
{
  if (!msg) {
    return false;
  }
  // inspection_id
  if (!rosidl_runtime_c__String__init(&msg->inspection_id)) {
    appleproj_interfaces__srv__RetryInspection_Request__fini(msg);
    return false;
  }
  // apple_id
  if (!rosidl_runtime_c__String__init(&msg->apple_id)) {
    appleproj_interfaces__srv__RetryInspection_Request__fini(msg);
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    appleproj_interfaces__srv__RetryInspection_Request__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__srv__RetryInspection_Request__fini(appleproj_interfaces__srv__RetryInspection_Request * msg)
{
  if (!msg) {
    return;
  }
  // inspection_id
  rosidl_runtime_c__String__fini(&msg->inspection_id);
  // apple_id
  rosidl_runtime_c__String__fini(&msg->apple_id);
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
}

bool
appleproj_interfaces__srv__RetryInspection_Request__are_equal(const appleproj_interfaces__srv__RetryInspection_Request * lhs, const appleproj_interfaces__srv__RetryInspection_Request * rhs)
{
  if (!lhs || !rhs) {
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
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__srv__RetryInspection_Request__copy(
  const appleproj_interfaces__srv__RetryInspection_Request * input,
  appleproj_interfaces__srv__RetryInspection_Request * output)
{
  if (!input || !output) {
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
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__srv__RetryInspection_Request *
appleproj_interfaces__srv__RetryInspection_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Request * msg = (appleproj_interfaces__srv__RetryInspection_Request *)allocator.allocate(sizeof(appleproj_interfaces__srv__RetryInspection_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__srv__RetryInspection_Request));
  bool success = appleproj_interfaces__srv__RetryInspection_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__srv__RetryInspection_Request__destroy(appleproj_interfaces__srv__RetryInspection_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__srv__RetryInspection_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__srv__RetryInspection_Request__Sequence__init(appleproj_interfaces__srv__RetryInspection_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__srv__RetryInspection_Request)) {
      return false;
    }
    data = (appleproj_interfaces__srv__RetryInspection_Request *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__srv__RetryInspection_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__srv__RetryInspection_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__srv__RetryInspection_Request__fini(&data[i - 1]);
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
appleproj_interfaces__srv__RetryInspection_Request__Sequence__fini(appleproj_interfaces__srv__RetryInspection_Request__Sequence * array)
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
      appleproj_interfaces__srv__RetryInspection_Request__fini(&array->data[i]);
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

appleproj_interfaces__srv__RetryInspection_Request__Sequence *
appleproj_interfaces__srv__RetryInspection_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Request__Sequence * array = (appleproj_interfaces__srv__RetryInspection_Request__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__srv__RetryInspection_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__srv__RetryInspection_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__srv__RetryInspection_Request__Sequence__destroy(appleproj_interfaces__srv__RetryInspection_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__srv__RetryInspection_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__srv__RetryInspection_Request__Sequence__are_equal(const appleproj_interfaces__srv__RetryInspection_Request__Sequence * lhs, const appleproj_interfaces__srv__RetryInspection_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__srv__RetryInspection_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__srv__RetryInspection_Request__Sequence__copy(
  const appleproj_interfaces__srv__RetryInspection_Request__Sequence * input,
  appleproj_interfaces__srv__RetryInspection_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__srv__RetryInspection_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__srv__RetryInspection_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__srv__RetryInspection_Request * data =
      (appleproj_interfaces__srv__RetryInspection_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__srv__RetryInspection_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__srv__RetryInspection_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__srv__RetryInspection_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `new_inspection_id`
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
appleproj_interfaces__srv__RetryInspection_Response__init(appleproj_interfaces__srv__RetryInspection_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // new_inspection_id
  if (!rosidl_runtime_c__String__init(&msg->new_inspection_id)) {
    appleproj_interfaces__srv__RetryInspection_Response__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    appleproj_interfaces__srv__RetryInspection_Response__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__srv__RetryInspection_Response__fini(appleproj_interfaces__srv__RetryInspection_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // new_inspection_id
  rosidl_runtime_c__String__fini(&msg->new_inspection_id);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
appleproj_interfaces__srv__RetryInspection_Response__are_equal(const appleproj_interfaces__srv__RetryInspection_Response * lhs, const appleproj_interfaces__srv__RetryInspection_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // new_inspection_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->new_inspection_id), &(rhs->new_inspection_id)))
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
appleproj_interfaces__srv__RetryInspection_Response__copy(
  const appleproj_interfaces__srv__RetryInspection_Response * input,
  appleproj_interfaces__srv__RetryInspection_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // new_inspection_id
  if (!rosidl_runtime_c__String__copy(
      &(input->new_inspection_id), &(output->new_inspection_id)))
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

appleproj_interfaces__srv__RetryInspection_Response *
appleproj_interfaces__srv__RetryInspection_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Response * msg = (appleproj_interfaces__srv__RetryInspection_Response *)allocator.allocate(sizeof(appleproj_interfaces__srv__RetryInspection_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__srv__RetryInspection_Response));
  bool success = appleproj_interfaces__srv__RetryInspection_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__srv__RetryInspection_Response__destroy(appleproj_interfaces__srv__RetryInspection_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__srv__RetryInspection_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__srv__RetryInspection_Response__Sequence__init(appleproj_interfaces__srv__RetryInspection_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__srv__RetryInspection_Response)) {
      return false;
    }
    data = (appleproj_interfaces__srv__RetryInspection_Response *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__srv__RetryInspection_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__srv__RetryInspection_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__srv__RetryInspection_Response__fini(&data[i - 1]);
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
appleproj_interfaces__srv__RetryInspection_Response__Sequence__fini(appleproj_interfaces__srv__RetryInspection_Response__Sequence * array)
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
      appleproj_interfaces__srv__RetryInspection_Response__fini(&array->data[i]);
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

appleproj_interfaces__srv__RetryInspection_Response__Sequence *
appleproj_interfaces__srv__RetryInspection_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Response__Sequence * array = (appleproj_interfaces__srv__RetryInspection_Response__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__srv__RetryInspection_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__srv__RetryInspection_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__srv__RetryInspection_Response__Sequence__destroy(appleproj_interfaces__srv__RetryInspection_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__srv__RetryInspection_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__srv__RetryInspection_Response__Sequence__are_equal(const appleproj_interfaces__srv__RetryInspection_Response__Sequence * lhs, const appleproj_interfaces__srv__RetryInspection_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__srv__RetryInspection_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__srv__RetryInspection_Response__Sequence__copy(
  const appleproj_interfaces__srv__RetryInspection_Response__Sequence * input,
  appleproj_interfaces__srv__RetryInspection_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__srv__RetryInspection_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__srv__RetryInspection_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__srv__RetryInspection_Response * data =
      (appleproj_interfaces__srv__RetryInspection_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__srv__RetryInspection_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__srv__RetryInspection_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__srv__RetryInspection_Response__copy(
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
// #include "appleproj_interfaces/srv/detail/retry_inspection__functions.h"

bool
appleproj_interfaces__srv__RetryInspection_Event__init(appleproj_interfaces__srv__RetryInspection_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    appleproj_interfaces__srv__RetryInspection_Event__fini(msg);
    return false;
  }
  // request
  if (!appleproj_interfaces__srv__RetryInspection_Request__Sequence__init(&msg->request, 0)) {
    appleproj_interfaces__srv__RetryInspection_Event__fini(msg);
    return false;
  }
  // response
  if (!appleproj_interfaces__srv__RetryInspection_Response__Sequence__init(&msg->response, 0)) {
    appleproj_interfaces__srv__RetryInspection_Event__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__srv__RetryInspection_Event__fini(appleproj_interfaces__srv__RetryInspection_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  appleproj_interfaces__srv__RetryInspection_Request__Sequence__fini(&msg->request);
  // response
  appleproj_interfaces__srv__RetryInspection_Response__Sequence__fini(&msg->response);
}

bool
appleproj_interfaces__srv__RetryInspection_Event__are_equal(const appleproj_interfaces__srv__RetryInspection_Event * lhs, const appleproj_interfaces__srv__RetryInspection_Event * rhs)
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
  if (!appleproj_interfaces__srv__RetryInspection_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__srv__RetryInspection_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__srv__RetryInspection_Event__copy(
  const appleproj_interfaces__srv__RetryInspection_Event * input,
  appleproj_interfaces__srv__RetryInspection_Event * output)
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
  if (!appleproj_interfaces__srv__RetryInspection_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__srv__RetryInspection_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__srv__RetryInspection_Event *
appleproj_interfaces__srv__RetryInspection_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Event * msg = (appleproj_interfaces__srv__RetryInspection_Event *)allocator.allocate(sizeof(appleproj_interfaces__srv__RetryInspection_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__srv__RetryInspection_Event));
  bool success = appleproj_interfaces__srv__RetryInspection_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__srv__RetryInspection_Event__destroy(appleproj_interfaces__srv__RetryInspection_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__srv__RetryInspection_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__srv__RetryInspection_Event__Sequence__init(appleproj_interfaces__srv__RetryInspection_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__srv__RetryInspection_Event)) {
      return false;
    }
    data = (appleproj_interfaces__srv__RetryInspection_Event *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__srv__RetryInspection_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__srv__RetryInspection_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__srv__RetryInspection_Event__fini(&data[i - 1]);
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
appleproj_interfaces__srv__RetryInspection_Event__Sequence__fini(appleproj_interfaces__srv__RetryInspection_Event__Sequence * array)
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
      appleproj_interfaces__srv__RetryInspection_Event__fini(&array->data[i]);
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

appleproj_interfaces__srv__RetryInspection_Event__Sequence *
appleproj_interfaces__srv__RetryInspection_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__RetryInspection_Event__Sequence * array = (appleproj_interfaces__srv__RetryInspection_Event__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__srv__RetryInspection_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__srv__RetryInspection_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__srv__RetryInspection_Event__Sequence__destroy(appleproj_interfaces__srv__RetryInspection_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__srv__RetryInspection_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__srv__RetryInspection_Event__Sequence__are_equal(const appleproj_interfaces__srv__RetryInspection_Event__Sequence * lhs, const appleproj_interfaces__srv__RetryInspection_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__srv__RetryInspection_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__srv__RetryInspection_Event__Sequence__copy(
  const appleproj_interfaces__srv__RetryInspection_Event__Sequence * input,
  appleproj_interfaces__srv__RetryInspection_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__srv__RetryInspection_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__srv__RetryInspection_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__srv__RetryInspection_Event * data =
      (appleproj_interfaces__srv__RetryInspection_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__srv__RetryInspection_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__srv__RetryInspection_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__srv__RetryInspection_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
