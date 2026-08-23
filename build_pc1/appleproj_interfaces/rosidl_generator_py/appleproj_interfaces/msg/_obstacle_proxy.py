# generated from rosidl_generator_py/resource/_idl.py.em
# with input from appleproj_interfaces:msg/ObstacleProxy.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ObstacleProxy(type):
    """Metaclass of message 'ObstacleProxy'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'SHAPE_SPHERE': 1,
        'SHAPE_BOX': 2,
        'SHAPE_CAPSULE': 3,
        'CLASS_TRUNK': 1,
        'CLASS_BRANCH': 2,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('appleproj_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'appleproj_interfaces.msg.ObstacleProxy')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__obstacle_proxy
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__obstacle_proxy
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__obstacle_proxy
            cls._TYPE_SUPPORT = module.type_support_msg__msg__obstacle_proxy
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__obstacle_proxy

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from geometry_msgs.msg import Vector3
            if Vector3.__class__._TYPE_SUPPORT is None:
                Vector3.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'SHAPE_SPHERE': cls.__constants['SHAPE_SPHERE'],
            'SHAPE_BOX': cls.__constants['SHAPE_BOX'],
            'SHAPE_CAPSULE': cls.__constants['SHAPE_CAPSULE'],
            'CLASS_TRUNK': cls.__constants['CLASS_TRUNK'],
            'CLASS_BRANCH': cls.__constants['CLASS_BRANCH'],
        }

    @property
    def SHAPE_SPHERE(self):
        """Message constant 'SHAPE_SPHERE'."""
        return Metaclass_ObstacleProxy.__constants['SHAPE_SPHERE']

    @property
    def SHAPE_BOX(self):
        """Message constant 'SHAPE_BOX'."""
        return Metaclass_ObstacleProxy.__constants['SHAPE_BOX']

    @property
    def SHAPE_CAPSULE(self):
        """Message constant 'SHAPE_CAPSULE'."""
        return Metaclass_ObstacleProxy.__constants['SHAPE_CAPSULE']

    @property
    def CLASS_TRUNK(self):
        """Message constant 'CLASS_TRUNK'."""
        return Metaclass_ObstacleProxy.__constants['CLASS_TRUNK']

    @property
    def CLASS_BRANCH(self):
        """Message constant 'CLASS_BRANCH'."""
        return Metaclass_ObstacleProxy.__constants['CLASS_BRANCH']


class ObstacleProxy(metaclass=Metaclass_ObstacleProxy):
    """
    Message class 'ObstacleProxy'.

    Constants:
      SHAPE_SPHERE
      SHAPE_BOX
      SHAPE_CAPSULE
      CLASS_TRUNK
      CLASS_BRANCH
    """

    __slots__ = [
        '_obstacle_id',
        '_shape',
        '_obstacle_class',
        '_pose',
        '_dimensions',
        '_safety_margin',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'obstacle_id': 'string',
        'shape': 'uint8',
        'obstacle_class': 'uint8',
        'pose': 'geometry_msgs/Pose',
        'dimensions': 'geometry_msgs/Vector3',
        'safety_margin': 'double',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Vector3'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.obstacle_id = kwargs.get('obstacle_id', str())
        self.shape = kwargs.get('shape', int())
        self.obstacle_class = kwargs.get('obstacle_class', int())
        from geometry_msgs.msg import Pose
        self.pose = kwargs.get('pose', Pose())
        from geometry_msgs.msg import Vector3
        self.dimensions = kwargs.get('dimensions', Vector3())
        self.safety_margin = kwargs.get('safety_margin', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.obstacle_id != other.obstacle_id:
            return False
        if self.shape != other.shape:
            return False
        if self.obstacle_class != other.obstacle_class:
            return False
        if self.pose != other.pose:
            return False
        if self.dimensions != other.dimensions:
            return False
        if self.safety_margin != other.safety_margin:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def obstacle_id(self):
        """Message field 'obstacle_id'."""
        return self._obstacle_id

    @obstacle_id.setter
    def obstacle_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'obstacle_id' field must be of type 'str'"
        self._obstacle_id = value

    @builtins.property
    def shape(self):
        """Message field 'shape'."""
        return self._shape

    @shape.setter
    def shape(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'shape' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'shape' field must be an unsigned integer in [0, 255]"
        self._shape = value

    @builtins.property
    def obstacle_class(self):
        """Message field 'obstacle_class'."""
        return self._obstacle_class

    @obstacle_class.setter
    def obstacle_class(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'obstacle_class' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'obstacle_class' field must be an unsigned integer in [0, 255]"
        self._obstacle_class = value

    @builtins.property
    def pose(self):
        """Message field 'pose'."""
        return self._pose

    @pose.setter
    def pose(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'pose' field must be a sub message of type 'Pose'"
        self._pose = value

    @builtins.property
    def dimensions(self):
        """Message field 'dimensions'."""
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Vector3
            assert \
                isinstance(value, Vector3), \
                "The 'dimensions' field must be a sub message of type 'Vector3'"
        self._dimensions = value

    @builtins.property
    def safety_margin(self):
        """Message field 'safety_margin'."""
        return self._safety_margin

    @safety_margin.setter
    def safety_margin(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'safety_margin' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'safety_margin' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._safety_margin = value
