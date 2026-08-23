// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from appleproj_interfaces:srv/GetPlanningScene.idl
// generated code does not contain a copyright notice
#include "appleproj_interfaces/srv/detail/get_planning_scene__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
appleproj_interfaces__srv__GetPlanningScene_Request__init(appleproj_interfaces__srv__GetPlanningScene_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
appleproj_interfaces__srv__GetPlanningScene_Request__fini(appleproj_interfaces__srv__GetPlanningScene_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
appleproj_interfaces__srv__GetPlanningScene_Request__are_equal(const appleproj_interfaces__srv__GetPlanningScene_Request * lhs, const appleproj_interfaces__srv__GetPlanningScene_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__srv__GetPlanningScene_Request__copy(
  const appleproj_interfaces__srv__GetPlanningScene_Request * input,
  appleproj_interfaces__srv__GetPlanningScene_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

appleproj_interfaces__srv__GetPlanningScene_Request *
appleproj_interfaces__srv__GetPlanningScene_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Request * msg = (appleproj_interfaces__srv__GetPlanningScene_Request *)allocator.allocate(sizeof(appleproj_interfaces__srv__GetPlanningScene_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__srv__GetPlanningScene_Request));
  bool success = appleproj_interfaces__srv__GetPlanningScene_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__srv__GetPlanningScene_Request__destroy(appleproj_interfaces__srv__GetPlanningScene_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__srv__GetPlanningScene_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__init(appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__srv__GetPlanningScene_Request)) {
      return false;
    }
    data = (appleproj_interfaces__srv__GetPlanningScene_Request *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__srv__GetPlanningScene_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__srv__GetPlanningScene_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__srv__GetPlanningScene_Request__fini(&data[i - 1]);
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
appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__fini(appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * array)
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
      appleproj_interfaces__srv__GetPlanningScene_Request__fini(&array->data[i]);
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

appleproj_interfaces__srv__GetPlanningScene_Request__Sequence *
appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * array = (appleproj_interfaces__srv__GetPlanningScene_Request__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__srv__GetPlanningScene_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__destroy(appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__are_equal(const appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * lhs, const appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__srv__GetPlanningScene_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__copy(
  const appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * input,
  appleproj_interfaces__srv__GetPlanningScene_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__srv__GetPlanningScene_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__srv__GetPlanningScene_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__srv__GetPlanningScene_Request * data =
      (appleproj_interfaces__srv__GetPlanningScene_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__srv__GetPlanningScene_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__srv__GetPlanningScene_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__srv__GetPlanningScene_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `scene`
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
appleproj_interfaces__srv__GetPlanningScene_Response__init(appleproj_interfaces__srv__GetPlanningScene_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // scene
  if (!appleproj_interfaces__msg__PlanningScene__init(&msg->scene)) {
    appleproj_interfaces__srv__GetPlanningScene_Response__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    appleproj_interfaces__srv__GetPlanningScene_Response__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__srv__GetPlanningScene_Response__fini(appleproj_interfaces__srv__GetPlanningScene_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // scene
  appleproj_interfaces__msg__PlanningScene__fini(&msg->scene);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
appleproj_interfaces__srv__GetPlanningScene_Response__are_equal(const appleproj_interfaces__srv__GetPlanningScene_Response * lhs, const appleproj_interfaces__srv__GetPlanningScene_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // scene
  if (!appleproj_interfaces__msg__PlanningScene__are_equal(
      &(lhs->scene), &(rhs->scene)))
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
appleproj_interfaces__srv__GetPlanningScene_Response__copy(
  const appleproj_interfaces__srv__GetPlanningScene_Response * input,
  appleproj_interfaces__srv__GetPlanningScene_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // scene
  if (!appleproj_interfaces__msg__PlanningScene__copy(
      &(input->scene), &(output->scene)))
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

appleproj_interfaces__srv__GetPlanningScene_Response *
appleproj_interfaces__srv__GetPlanningScene_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Response * msg = (appleproj_interfaces__srv__GetPlanningScene_Response *)allocator.allocate(sizeof(appleproj_interfaces__srv__GetPlanningScene_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__srv__GetPlanningScene_Response));
  bool success = appleproj_interfaces__srv__GetPlanningScene_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__srv__GetPlanningScene_Response__destroy(appleproj_interfaces__srv__GetPlanningScene_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__srv__GetPlanningScene_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__init(appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__srv__GetPlanningScene_Response)) {
      return false;
    }
    data = (appleproj_interfaces__srv__GetPlanningScene_Response *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__srv__GetPlanningScene_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__srv__GetPlanningScene_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__srv__GetPlanningScene_Response__fini(&data[i - 1]);
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
appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__fini(appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * array)
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
      appleproj_interfaces__srv__GetPlanningScene_Response__fini(&array->data[i]);
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

appleproj_interfaces__srv__GetPlanningScene_Response__Sequence *
appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * array = (appleproj_interfaces__srv__GetPlanningScene_Response__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__srv__GetPlanningScene_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__destroy(appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__are_equal(const appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * lhs, const appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__srv__GetPlanningScene_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__copy(
  const appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * input,
  appleproj_interfaces__srv__GetPlanningScene_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__srv__GetPlanningScene_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__srv__GetPlanningScene_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__srv__GetPlanningScene_Response * data =
      (appleproj_interfaces__srv__GetPlanningScene_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__srv__GetPlanningScene_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__srv__GetPlanningScene_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__srv__GetPlanningScene_Response__copy(
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
// #include "appleproj_interfaces/srv/detail/get_planning_scene__functions.h"

bool
appleproj_interfaces__srv__GetPlanningScene_Event__init(appleproj_interfaces__srv__GetPlanningScene_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    appleproj_interfaces__srv__GetPlanningScene_Event__fini(msg);
    return false;
  }
  // request
  if (!appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__init(&msg->request, 0)) {
    appleproj_interfaces__srv__GetPlanningScene_Event__fini(msg);
    return false;
  }
  // response
  if (!appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__init(&msg->response, 0)) {
    appleproj_interfaces__srv__GetPlanningScene_Event__fini(msg);
    return false;
  }
  return true;
}

void
appleproj_interfaces__srv__GetPlanningScene_Event__fini(appleproj_interfaces__srv__GetPlanningScene_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__fini(&msg->request);
  // response
  appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__fini(&msg->response);
}

bool
appleproj_interfaces__srv__GetPlanningScene_Event__are_equal(const appleproj_interfaces__srv__GetPlanningScene_Event * lhs, const appleproj_interfaces__srv__GetPlanningScene_Event * rhs)
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
  if (!appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
appleproj_interfaces__srv__GetPlanningScene_Event__copy(
  const appleproj_interfaces__srv__GetPlanningScene_Event * input,
  appleproj_interfaces__srv__GetPlanningScene_Event * output)
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
  if (!appleproj_interfaces__srv__GetPlanningScene_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!appleproj_interfaces__srv__GetPlanningScene_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

appleproj_interfaces__srv__GetPlanningScene_Event *
appleproj_interfaces__srv__GetPlanningScene_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Event * msg = (appleproj_interfaces__srv__GetPlanningScene_Event *)allocator.allocate(sizeof(appleproj_interfaces__srv__GetPlanningScene_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(appleproj_interfaces__srv__GetPlanningScene_Event));
  bool success = appleproj_interfaces__srv__GetPlanningScene_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
appleproj_interfaces__srv__GetPlanningScene_Event__destroy(appleproj_interfaces__srv__GetPlanningScene_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    appleproj_interfaces__srv__GetPlanningScene_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__init(appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(appleproj_interfaces__srv__GetPlanningScene_Event)) {
      return false;
    }
    data = (appleproj_interfaces__srv__GetPlanningScene_Event *)allocator.zero_allocate(size, sizeof(appleproj_interfaces__srv__GetPlanningScene_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = appleproj_interfaces__srv__GetPlanningScene_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        appleproj_interfaces__srv__GetPlanningScene_Event__fini(&data[i - 1]);
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
appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__fini(appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * array)
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
      appleproj_interfaces__srv__GetPlanningScene_Event__fini(&array->data[i]);
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

appleproj_interfaces__srv__GetPlanningScene_Event__Sequence *
appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * array = (appleproj_interfaces__srv__GetPlanningScene_Event__Sequence *)allocator.allocate(sizeof(appleproj_interfaces__srv__GetPlanningScene_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__destroy(appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__are_equal(const appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * lhs, const appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!appleproj_interfaces__srv__GetPlanningScene_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
appleproj_interfaces__srv__GetPlanningScene_Event__Sequence__copy(
  const appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * input,
  appleproj_interfaces__srv__GetPlanningScene_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(appleproj_interfaces__srv__GetPlanningScene_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(appleproj_interfaces__srv__GetPlanningScene_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    appleproj_interfaces__srv__GetPlanningScene_Event * data =
      (appleproj_interfaces__srv__GetPlanningScene_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!appleproj_interfaces__srv__GetPlanningScene_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          appleproj_interfaces__srv__GetPlanningScene_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!appleproj_interfaces__srv__GetPlanningScene_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
