// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from appleproj_interfaces:msg/PlanningScene.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "appleproj_interfaces/msg/detail/planning_scene__struct.h"
#include "appleproj_interfaces/msg/detail/planning_scene__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "appleproj_interfaces/msg/detail/obstacle_proxy__functions.h"
// end nested array functions include
ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__pose_stamped__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__pose_stamped__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__pose_stamped__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__pose_stamped__convert_to_py(void * raw_ros_message);
bool appleproj_interfaces__msg__obstacle_proxy__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * appleproj_interfaces__msg__obstacle_proxy__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool appleproj_interfaces__msg__planning_scene__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[55];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("appleproj_interfaces.msg._planning_scene.PlanningScene", full_classname_dest, 54) == 0);
  }
  appleproj_interfaces__msg__PlanningScene * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // reset_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "reset_id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->reset_id = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // scene_version
    PyObject * field = PyObject_GetAttrString(_pymsg, "scene_version");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->scene_version = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // robot_base_pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "robot_base_pose");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__pose_stamped__convert_from_py(field, &ros_message->robot_base_pose)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // robot_tcp_pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "robot_tcp_pose");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__pose_stamped__convert_from_py(field, &ros_message->robot_tcp_pose)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // obstacles
    PyObject * field = PyObject_GetAttrString(_pymsg, "obstacles");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'obstacles'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!appleproj_interfaces__msg__ObstacleProxy__Sequence__init(&(ros_message->obstacles), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create appleproj_interfaces__msg__ObstacleProxy__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    appleproj_interfaces__msg__ObstacleProxy * dest = ros_message->obstacles.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!appleproj_interfaces__msg__obstacle_proxy__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * appleproj_interfaces__msg__planning_scene__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of PlanningScene */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("appleproj_interfaces.msg._planning_scene");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "PlanningScene");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  appleproj_interfaces__msg__PlanningScene * ros_message = (appleproj_interfaces__msg__PlanningScene *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // reset_id
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->reset_id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "reset_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scene_version
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->scene_version);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scene_version", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // robot_base_pose
    PyObject * field = NULL;
    field = geometry_msgs__msg__pose_stamped__convert_to_py(&ros_message->robot_base_pose);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "robot_base_pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // robot_tcp_pose
    PyObject * field = NULL;
    field = geometry_msgs__msg__pose_stamped__convert_to_py(&ros_message->robot_tcp_pose);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "robot_tcp_pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // obstacles
    PyObject * field = NULL;
    size_t size = ros_message->obstacles.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    appleproj_interfaces__msg__ObstacleProxy * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->obstacles.data[i]);
      PyObject * pyitem = appleproj_interfaces__msg__obstacle_proxy__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "obstacles", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
