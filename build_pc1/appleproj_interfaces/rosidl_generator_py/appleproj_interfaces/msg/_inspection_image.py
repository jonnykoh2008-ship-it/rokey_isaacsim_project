# generated from rosidl_generator_py/resource/_idl.py.em
# with input from appleproj_interfaces:msg/InspectionImage.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_InspectionImage(type):
    """Metaclass of message 'InspectionImage'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
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
                'appleproj_interfaces.msg.InspectionImage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__inspection_image
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__inspection_image
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__inspection_image
            cls._TYPE_SUPPORT = module.type_support_msg__msg__inspection_image
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__inspection_image

            from sensor_msgs.msg import CompressedImage
            if CompressedImage.__class__._TYPE_SUPPORT is None:
                CompressedImage.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class InspectionImage(metaclass=Metaclass_InspectionImage):
    """Message class 'InspectionImage'."""

    __slots__ = [
        '_header',
        '_inspection_id',
        '_apple_id',
        '_frame_index',
        '_total_frames',
        '_image',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'inspection_id': 'string',
        'apple_id': 'string',
        'frame_index': 'uint16',
        'total_frames': 'uint16',
        'image': 'sensor_msgs/CompressedImage',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'CompressedImage'),  # noqa: E501
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
        self.frame_index = kwargs.get('frame_index', int())
        self.total_frames = kwargs.get('total_frames', int())
        from sensor_msgs.msg import CompressedImage
        self.image = kwargs.get('image', CompressedImage())

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
        if self.frame_index != other.frame_index:
            return False
        if self.total_frames != other.total_frames:
            return False
        if self.image != other.image:
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
    def frame_index(self):
        """Message field 'frame_index'."""
        return self._frame_index

    @frame_index.setter
    def frame_index(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'frame_index' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'frame_index' field must be an unsigned integer in [0, 65535]"
        self._frame_index = value

    @builtins.property
    def total_frames(self):
        """Message field 'total_frames'."""
        return self._total_frames

    @total_frames.setter
    def total_frames(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'total_frames' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'total_frames' field must be an unsigned integer in [0, 65535]"
        self._total_frames = value

    @builtins.property
    def image(self):
        """Message field 'image'."""
        return self._image

    @image.setter
    def image(self, value):
        if self._check_fields:
            from sensor_msgs.msg import CompressedImage
            assert \
                isinstance(value, CompressedImage), \
                "The 'image' field must be a sub message of type 'CompressedImage'"
        self._image = value
