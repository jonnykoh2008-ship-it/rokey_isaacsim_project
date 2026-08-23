# generated from rosidl_generator_py/resource/_idl.py.em
# with input from appleproj_interfaces:msg/QualityResult.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

# Member 'frame_indices'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_QualityResult(type):
    """Metaclass of message 'QualityResult'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'HIGH': 1,
        'MEDIUM': 2,
        'LOW': 3,
        'VALID': 1,
        'RECHECK': 2,
        'UNCLASSIFIED': 3,
        'TIMEOUT': 4,
        'LATE_RESULT': 5,
        'ID_MISMATCH': 6,
        'INSUFFICIENT_VIEWS': 7,
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
                'appleproj_interfaces.msg.QualityResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__quality_result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__quality_result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__quality_result
            cls._TYPE_SUPPORT = module.type_support_msg__msg__quality_result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__quality_result

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'HIGH': cls.__constants['HIGH'],
            'MEDIUM': cls.__constants['MEDIUM'],
            'LOW': cls.__constants['LOW'],
            'VALID': cls.__constants['VALID'],
            'RECHECK': cls.__constants['RECHECK'],
            'UNCLASSIFIED': cls.__constants['UNCLASSIFIED'],
            'TIMEOUT': cls.__constants['TIMEOUT'],
            'LATE_RESULT': cls.__constants['LATE_RESULT'],
            'ID_MISMATCH': cls.__constants['ID_MISMATCH'],
            'INSUFFICIENT_VIEWS': cls.__constants['INSUFFICIENT_VIEWS'],
        }

    @property
    def HIGH(self):
        """Message constant 'HIGH'."""
        return Metaclass_QualityResult.__constants['HIGH']

    @property
    def MEDIUM(self):
        """Message constant 'MEDIUM'."""
        return Metaclass_QualityResult.__constants['MEDIUM']

    @property
    def LOW(self):
        """Message constant 'LOW'."""
        return Metaclass_QualityResult.__constants['LOW']

    @property
    def VALID(self):
        """Message constant 'VALID'."""
        return Metaclass_QualityResult.__constants['VALID']

    @property
    def RECHECK(self):
        """Message constant 'RECHECK'."""
        return Metaclass_QualityResult.__constants['RECHECK']

    @property
    def UNCLASSIFIED(self):
        """Message constant 'UNCLASSIFIED'."""
        return Metaclass_QualityResult.__constants['UNCLASSIFIED']

    @property
    def TIMEOUT(self):
        """Message constant 'TIMEOUT'."""
        return Metaclass_QualityResult.__constants['TIMEOUT']

    @property
    def LATE_RESULT(self):
        """Message constant 'LATE_RESULT'."""
        return Metaclass_QualityResult.__constants['LATE_RESULT']

    @property
    def ID_MISMATCH(self):
        """Message constant 'ID_MISMATCH'."""
        return Metaclass_QualityResult.__constants['ID_MISMATCH']

    @property
    def INSUFFICIENT_VIEWS(self):
        """Message constant 'INSUFFICIENT_VIEWS'."""
        return Metaclass_QualityResult.__constants['INSUFFICIENT_VIEWS']


class QualityResult(metaclass=Metaclass_QualityResult):
    """
    Message class 'QualityResult'.

    Constants:
      HIGH
      MEDIUM
      LOW
      VALID
      RECHECK
      UNCLASSIFIED
      TIMEOUT
      LATE_RESULT
      ID_MISMATCH
      INSUFFICIENT_VIEWS
    """

    __slots__ = [
        '_header',
        '_inspection_id',
        '_apple_id',
        '_grade',
        '_confidence',
        '_color_ratio',
        '_diameter_mm',
        '_damage_area_cm2',
        '_frames_used',
        '_frame_indices',
        '_result_timestamp',
        '_status',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'inspection_id': 'string',
        'apple_id': 'string',
        'grade': 'uint8',
        'confidence': 'float',
        'color_ratio': 'float',
        'diameter_mm': 'float',
        'damage_area_cm2': 'float',
        'frames_used': 'uint16',
        'frame_indices': 'sequence<uint16>',
        'result_timestamp': 'builtin_interfaces/Time',
        'status': 'uint8',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint16')),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
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
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.inspection_id = kwargs.get('inspection_id', str())
        self.apple_id = kwargs.get('apple_id', str())
        self.grade = kwargs.get('grade', int())
        self.confidence = kwargs.get('confidence', float())
        self.color_ratio = kwargs.get('color_ratio', float())
        self.diameter_mm = kwargs.get('diameter_mm', float())
        self.damage_area_cm2 = kwargs.get('damage_area_cm2', float())
        self.frames_used = kwargs.get('frames_used', int())
        self.frame_indices = array.array('H', kwargs.get('frame_indices', []))
        from builtin_interfaces.msg import Time
        self.result_timestamp = kwargs.get('result_timestamp', Time())
        self.status = kwargs.get('status', int())

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
        if self.header != other.header:
            return False
        if self.inspection_id != other.inspection_id:
            return False
        if self.apple_id != other.apple_id:
            return False
        if self.grade != other.grade:
            return False
        if self.confidence != other.confidence:
            return False
        if self.color_ratio != other.color_ratio:
            return False
        if self.diameter_mm != other.diameter_mm:
            return False
        if self.damage_area_cm2 != other.damage_area_cm2:
            return False
        if self.frames_used != other.frames_used:
            return False
        if self.frame_indices != other.frame_indices:
            return False
        if self.result_timestamp != other.result_timestamp:
            return False
        if self.status != other.status:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if self._check_fields:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def inspection_id(self):
        """Message field 'inspection_id'."""
        return self._inspection_id

    @inspection_id.setter
    def inspection_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'inspection_id' field must be of type 'str'"
        self._inspection_id = value

    @builtins.property
    def apple_id(self):
        """Message field 'apple_id'."""
        return self._apple_id

    @apple_id.setter
    def apple_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'apple_id' field must be of type 'str'"
        self._apple_id = value

    @builtins.property
    def grade(self):
        """Message field 'grade'."""
        return self._grade

    @grade.setter
    def grade(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'grade' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'grade' field must be an unsigned integer in [0, 255]"
        self._grade = value

    @builtins.property
    def confidence(self):
        """Message field 'confidence'."""
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._confidence = value

    @builtins.property
    def color_ratio(self):
        """Message field 'color_ratio'."""
        return self._color_ratio

    @color_ratio.setter
    def color_ratio(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'color_ratio' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'color_ratio' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._color_ratio = value

    @builtins.property
    def diameter_mm(self):
        """Message field 'diameter_mm'."""
        return self._diameter_mm

    @diameter_mm.setter
    def diameter_mm(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'diameter_mm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'diameter_mm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._diameter_mm = value

    @builtins.property
    def damage_area_cm2(self):
        """Message field 'damage_area_cm2'."""
        return self._damage_area_cm2

    @damage_area_cm2.setter
    def damage_area_cm2(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'damage_area_cm2' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'damage_area_cm2' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._damage_area_cm2 = value

    @builtins.property
    def frames_used(self):
        """Message field 'frames_used'."""
        return self._frames_used

    @frames_used.setter
    def frames_used(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'frames_used' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'frames_used' field must be an unsigned integer in [0, 65535]"
        self._frames_used = value

    @builtins.property
    def frame_indices(self):
        """Message field 'frame_indices'."""
        return self._frame_indices

    @frame_indices.setter
    def frame_indices(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'H', \
                    "The 'frame_indices' array.array() must have the type code of 'H'"
                self._frame_indices = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 65536 for val in value)), \
                "The 'frame_indices' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 65535]"
        self._frame_indices = array.array('H', value)

    @builtins.property
    def result_timestamp(self):
        """Message field 'result_timestamp'."""
        return self._result_timestamp

    @result_timestamp.setter
    def result_timestamp(self, value):
        if self._check_fields:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'result_timestamp' field must be a sub message of type 'Time'"
        self._result_timestamp = value

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'status' field must be an unsigned integer in [0, 255]"
        self._status = value
