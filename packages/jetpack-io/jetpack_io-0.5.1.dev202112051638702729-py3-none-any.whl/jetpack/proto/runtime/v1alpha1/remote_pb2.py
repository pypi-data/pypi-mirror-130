# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: jetpack/proto/runtime/v1alpha1/remote.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='jetpack/proto/runtime/v1alpha1/remote.proto',
  package='remote',
  syntax='proto3',
  serialized_options=b'\n\ncom.remoteB\013RemoteProtoP\001Z2go.jetpack.io/proto/jetpack/proto/runtime/v1alpha1\242\002\003RXX\252\002\006Remote\312\002\006Remote\342\002\022Remote\\GPBMetadata\352\002\006Remote',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+jetpack/proto/runtime/v1alpha1/remote.proto\x12\x06remote\x1a\x1fgoogle/protobuf/timestamp.proto\"[\n\x11RemoteCallRequest\x12)\n\x10qualified_symbol\x18\x01 \x01(\tR\x0fqualifiedSymbol\x12\x1b\n\tjson_args\x18\x02 \x01(\tR\x08jsonArgs\"7\n\x12RemoteCallResponse\x12!\n\x0cjson_results\x18\x01 \x01(\tR\x0bjsonResults\"V\n\x11\x43reateTaskRequest\x12 \n\x04task\x18\x01 \x01(\x0b\x32\x0c.remote.TaskR\x04task\x12\x1f\n\x0bsdk_version\x18\x02 \x01(\tR\nsdkVersion\"-\n\x12\x43reateTaskResponse\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\"T\n\x11PostResultRequest\x12\x17\n\x07\x65xec_id\x18\x01 \x01(\tR\x06\x65xecId\x12&\n\x06result\x18\x02 \x01(\x0b\x32\x0e.remote.ResultR\x06result\"\x14\n\x12PostResultResponse\"\xe4\x01\n\x04Task\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12\x1a\n\x08hostname\x18\x06 \x01(\tR\x08hostname\x12)\n\x10qualified_symbol\x18\x02 \x01(\tR\x0fqualifiedSymbol\x12!\n\x0c\x65ncoded_args\x18\x04 \x01(\x0cR\x0b\x65ncodedArgs\x12;\n\x0btarget_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ntargetTime\x12\x17\n\x07task_id\x18\x08 \x01(\tR\x06taskId\"R\n\x06Result\x12#\n\x05value\x18\x01 \x01(\x0b\x32\r.remote.ValueR\x05value\x12#\n\x05\x65rror\x18\x02 \x01(\x0b\x32\r.remote.ErrorR\x05\x65rror\"m\n\x05\x45rror\x12%\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x11.remote.ErrorCodeR\x04\x63ode\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12#\n\rencoded_error\x18\x03 \x01(\x0cR\x0c\x65ncodedError\",\n\x05Value\x12#\n\rencoded_value\x18\x01 \x01(\x0cR\x0c\x65ncodedValue\"\x97\x01\n\x12SetCronJobsRequest\x12\x1c\n\tnamespace\x18\x01 \x01(\tR\tnamespace\x12\x1a\n\x08hostname\x18\x02 \x01(\tR\x08hostname\x12\x19\n\x06\x61pp_id\x18\x03 \x01(\tB\x02\x18\x01R\x05\x61ppId\x12,\n\tcron_jobs\x18\x04 \x03(\x0b\x32\x0f.remote.CronJobR\x08\x63ronJobs\"\x15\n\x13SetCronJobsResponse\"/\n\x14WaitForResultRequest\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\"?\n\x15WaitForResultResponse\x12&\n\x06result\x18\x01 \x01(\x0b\x32\x0e.remote.ResultR\x06result\"\xd3\x01\n\x07\x43ronJob\x12)\n\x10qualified_symbol\x18\x03 \x01(\tR\x0fqualifiedSymbol\x12\x1f\n\x0btarget_time\x18\x04 \x01(\tR\ntargetTime\x12>\n\x12target_day_of_week\x18\x05 \x01(\x0e\x32\x11.remote.DayOfWeekR\x0ftargetDayOfWeek\x12 \n\x04unit\x18\x06 \x01(\x0e\x32\x0c.remote.UnitR\x04unit\x12\x1a\n\x08interval\x18\x07 \x01(\x03R\x08interval*7\n\tErrorCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07RUNTIME\x10\x64\x12\x10\n\x0b\x41PPLICATION\x10\xc8\x01*R\n\x04Unit\x12\x10\n\x0cUNKNOWN_UNIT\x10\x00\x12\x0b\n\x07SECONDS\x10\x01\x12\x0b\n\x07MINUTES\x10\x02\x12\t\n\x05HOURS\x10\x03\x12\x08\n\x04\x44\x41YS\x10\x04\x12\t\n\x05WEEKS\x10\x05*x\n\tDayOfWeek\x12\x0f\n\x0bUNKNOWN_DAY\x10\x00\x12\n\n\x06SUNDAY\x10\x01\x12\n\n\x06MONDAY\x10\x02\x12\x0b\n\x07TUESDAY\x10\x03\x12\r\n\tWEDNESDAY\x10\x04\x12\x0c\n\x08THURSDAY\x10\x05\x12\n\n\x06\x46RIDAY\x10\x06\x12\x0c\n\x08SATURDAY\x10\x07\x32\xff\x02\n\x0eRemoteExecutor\x12\x45\n\nCreateTask\x12\x19.remote.CreateTaskRequest\x1a\x1a.remote.CreateTaskResponse\"\x00\x12\x45\n\nPostResult\x12\x19.remote.PostResultRequest\x1a\x1a.remote.PostResultResponse\"\x00\x12N\n\rWaitForResult\x12\x1c.remote.WaitForResultRequest\x1a\x1d.remote.WaitForResultResponse\"\x00\x12H\n\x0bSetCronJobs\x12\x1a.remote.SetCronJobsRequest\x1a\x1b.remote.SetCronJobsResponse\"\x00\x12\x45\n\nRemoteCall\x12\x19.remote.RemoteCallRequest\x1a\x1a.remote.RemoteCallResponse\"\x00\x42\x85\x01\n\ncom.remoteB\x0bRemoteProtoP\x01Z2go.jetpack.io/proto/jetpack/proto/runtime/v1alpha1\xa2\x02\x03RXX\xaa\x02\x06Remote\xca\x02\x06Remote\xe2\x02\x12Remote\\GPBMetadata\xea\x02\x06Remoteb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])

_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='remote.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RUNTIME', index=1, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='APPLICATION', index=2, number=200,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1458,
  serialized_end=1513,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
_UNIT = _descriptor.EnumDescriptor(
  name='Unit',
  full_name='remote.Unit',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_UNIT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SECONDS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MINUTES', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HOURS', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DAYS', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WEEKS', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1515,
  serialized_end=1597,
)
_sym_db.RegisterEnumDescriptor(_UNIT)

Unit = enum_type_wrapper.EnumTypeWrapper(_UNIT)
_DAYOFWEEK = _descriptor.EnumDescriptor(
  name='DayOfWeek',
  full_name='remote.DayOfWeek',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_DAY', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUNDAY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MONDAY', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TUESDAY', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WEDNESDAY', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='THURSDAY', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FRIDAY', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SATURDAY', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1599,
  serialized_end=1719,
)
_sym_db.RegisterEnumDescriptor(_DAYOFWEEK)

DayOfWeek = enum_type_wrapper.EnumTypeWrapper(_DAYOFWEEK)
UNKNOWN = 0
RUNTIME = 100
APPLICATION = 200
UNKNOWN_UNIT = 0
SECONDS = 1
MINUTES = 2
HOURS = 3
DAYS = 4
WEEKS = 5
UNKNOWN_DAY = 0
SUNDAY = 1
MONDAY = 2
TUESDAY = 3
WEDNESDAY = 4
THURSDAY = 5
FRIDAY = 6
SATURDAY = 7



_REMOTECALLREQUEST = _descriptor.Descriptor(
  name='RemoteCallRequest',
  full_name='remote.RemoteCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='qualified_symbol', full_name='remote.RemoteCallRequest.qualified_symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='qualifiedSymbol', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='json_args', full_name='remote.RemoteCallRequest.json_args', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='jsonArgs', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=88,
  serialized_end=179,
)


_REMOTECALLRESPONSE = _descriptor.Descriptor(
  name='RemoteCallResponse',
  full_name='remote.RemoteCallResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='json_results', full_name='remote.RemoteCallResponse.json_results', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='jsonResults', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=181,
  serialized_end=236,
)


_CREATETASKREQUEST = _descriptor.Descriptor(
  name='CreateTaskRequest',
  full_name='remote.CreateTaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='remote.CreateTaskRequest.task', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='task', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sdk_version', full_name='remote.CreateTaskRequest.sdk_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='sdkVersion', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=238,
  serialized_end=324,
)


_CREATETASKRESPONSE = _descriptor.Descriptor(
  name='CreateTaskResponse',
  full_name='remote.CreateTaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='remote.CreateTaskResponse.task_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='taskId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=326,
  serialized_end=371,
)


_POSTRESULTREQUEST = _descriptor.Descriptor(
  name='PostResultRequest',
  full_name='remote.PostResultRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exec_id', full_name='remote.PostResultRequest.exec_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='execId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='remote.PostResultRequest.result', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='result', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=373,
  serialized_end=457,
)


_POSTRESULTRESPONSE = _descriptor.Descriptor(
  name='PostResultResponse',
  full_name='remote.PostResultResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=459,
  serialized_end=479,
)


_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='remote.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='remote.Task.namespace', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='namespace', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hostname', full_name='remote.Task.hostname', index=1,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hostname', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='qualified_symbol', full_name='remote.Task.qualified_symbol', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='qualifiedSymbol', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoded_args', full_name='remote.Task.encoded_args', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='encodedArgs', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_time', full_name='remote.Task.target_time', index=4,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='targetTime', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_id', full_name='remote.Task.task_id', index=5,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='taskId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=482,
  serialized_end=710,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='remote.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='remote.Result.value', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='value', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='remote.Result.error', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='error', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=712,
  serialized_end=794,
)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='remote.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='remote.Error.code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='code', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='remote.Error.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='message', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoded_error', full_name='remote.Error.encoded_error', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='encodedError', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=796,
  serialized_end=905,
)


_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='remote.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='encoded_value', full_name='remote.Value.encoded_value', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='encodedValue', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=907,
  serialized_end=951,
)


_SETCRONJOBSREQUEST = _descriptor.Descriptor(
  name='SetCronJobsRequest',
  full_name='remote.SetCronJobsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='remote.SetCronJobsRequest.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='namespace', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hostname', full_name='remote.SetCronJobsRequest.hostname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='hostname', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='remote.SetCronJobsRequest.app_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', json_name='appId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cron_jobs', full_name='remote.SetCronJobsRequest.cron_jobs', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='cronJobs', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=954,
  serialized_end=1105,
)


_SETCRONJOBSRESPONSE = _descriptor.Descriptor(
  name='SetCronJobsResponse',
  full_name='remote.SetCronJobsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1107,
  serialized_end=1128,
)


_WAITFORRESULTREQUEST = _descriptor.Descriptor(
  name='WaitForResultRequest',
  full_name='remote.WaitForResultRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='remote.WaitForResultRequest.task_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='taskId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1130,
  serialized_end=1177,
)


_WAITFORRESULTRESPONSE = _descriptor.Descriptor(
  name='WaitForResultResponse',
  full_name='remote.WaitForResultResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='remote.WaitForResultResponse.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='result', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1179,
  serialized_end=1242,
)


_CRONJOB = _descriptor.Descriptor(
  name='CronJob',
  full_name='remote.CronJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='qualified_symbol', full_name='remote.CronJob.qualified_symbol', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='qualifiedSymbol', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_time', full_name='remote.CronJob.target_time', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='targetTime', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_day_of_week', full_name='remote.CronJob.target_day_of_week', index=2,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='targetDayOfWeek', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='unit', full_name='remote.CronJob.unit', index=3,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='unit', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='interval', full_name='remote.CronJob.interval', index=4,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='interval', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1245,
  serialized_end=1456,
)

_CREATETASKREQUEST.fields_by_name['task'].message_type = _TASK
_POSTRESULTREQUEST.fields_by_name['result'].message_type = _RESULT
_TASK.fields_by_name['target_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_RESULT.fields_by_name['value'].message_type = _VALUE
_RESULT.fields_by_name['error'].message_type = _ERROR
_ERROR.fields_by_name['code'].enum_type = _ERRORCODE
_SETCRONJOBSREQUEST.fields_by_name['cron_jobs'].message_type = _CRONJOB
_WAITFORRESULTRESPONSE.fields_by_name['result'].message_type = _RESULT
_CRONJOB.fields_by_name['target_day_of_week'].enum_type = _DAYOFWEEK
_CRONJOB.fields_by_name['unit'].enum_type = _UNIT
DESCRIPTOR.message_types_by_name['RemoteCallRequest'] = _REMOTECALLREQUEST
DESCRIPTOR.message_types_by_name['RemoteCallResponse'] = _REMOTECALLRESPONSE
DESCRIPTOR.message_types_by_name['CreateTaskRequest'] = _CREATETASKREQUEST
DESCRIPTOR.message_types_by_name['CreateTaskResponse'] = _CREATETASKRESPONSE
DESCRIPTOR.message_types_by_name['PostResultRequest'] = _POSTRESULTREQUEST
DESCRIPTOR.message_types_by_name['PostResultResponse'] = _POSTRESULTRESPONSE
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['Value'] = _VALUE
DESCRIPTOR.message_types_by_name['SetCronJobsRequest'] = _SETCRONJOBSREQUEST
DESCRIPTOR.message_types_by_name['SetCronJobsResponse'] = _SETCRONJOBSRESPONSE
DESCRIPTOR.message_types_by_name['WaitForResultRequest'] = _WAITFORRESULTREQUEST
DESCRIPTOR.message_types_by_name['WaitForResultResponse'] = _WAITFORRESULTRESPONSE
DESCRIPTOR.message_types_by_name['CronJob'] = _CRONJOB
DESCRIPTOR.enum_types_by_name['ErrorCode'] = _ERRORCODE
DESCRIPTOR.enum_types_by_name['Unit'] = _UNIT
DESCRIPTOR.enum_types_by_name['DayOfWeek'] = _DAYOFWEEK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RemoteCallRequest = _reflection.GeneratedProtocolMessageType('RemoteCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOTECALLREQUEST,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.RemoteCallRequest)
  })
_sym_db.RegisterMessage(RemoteCallRequest)

RemoteCallResponse = _reflection.GeneratedProtocolMessageType('RemoteCallResponse', (_message.Message,), {
  'DESCRIPTOR' : _REMOTECALLRESPONSE,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.RemoteCallResponse)
  })
_sym_db.RegisterMessage(RemoteCallResponse)

CreateTaskRequest = _reflection.GeneratedProtocolMessageType('CreateTaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATETASKREQUEST,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.CreateTaskRequest)
  })
_sym_db.RegisterMessage(CreateTaskRequest)

CreateTaskResponse = _reflection.GeneratedProtocolMessageType('CreateTaskResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATETASKRESPONSE,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.CreateTaskResponse)
  })
_sym_db.RegisterMessage(CreateTaskResponse)

PostResultRequest = _reflection.GeneratedProtocolMessageType('PostResultRequest', (_message.Message,), {
  'DESCRIPTOR' : _POSTRESULTREQUEST,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.PostResultRequest)
  })
_sym_db.RegisterMessage(PostResultRequest)

PostResultResponse = _reflection.GeneratedProtocolMessageType('PostResultResponse', (_message.Message,), {
  'DESCRIPTOR' : _POSTRESULTRESPONSE,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.PostResultResponse)
  })
_sym_db.RegisterMessage(PostResultResponse)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.Task)
  })
_sym_db.RegisterMessage(Task)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), {
  'DESCRIPTOR' : _RESULT,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.Result)
  })
_sym_db.RegisterMessage(Result)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
  'DESCRIPTOR' : _ERROR,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.Error)
  })
_sym_db.RegisterMessage(Error)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {
  'DESCRIPTOR' : _VALUE,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.Value)
  })
_sym_db.RegisterMessage(Value)

SetCronJobsRequest = _reflection.GeneratedProtocolMessageType('SetCronJobsRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETCRONJOBSREQUEST,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.SetCronJobsRequest)
  })
_sym_db.RegisterMessage(SetCronJobsRequest)

SetCronJobsResponse = _reflection.GeneratedProtocolMessageType('SetCronJobsResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETCRONJOBSRESPONSE,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.SetCronJobsResponse)
  })
_sym_db.RegisterMessage(SetCronJobsResponse)

WaitForResultRequest = _reflection.GeneratedProtocolMessageType('WaitForResultRequest', (_message.Message,), {
  'DESCRIPTOR' : _WAITFORRESULTREQUEST,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.WaitForResultRequest)
  })
_sym_db.RegisterMessage(WaitForResultRequest)

WaitForResultResponse = _reflection.GeneratedProtocolMessageType('WaitForResultResponse', (_message.Message,), {
  'DESCRIPTOR' : _WAITFORRESULTRESPONSE,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.WaitForResultResponse)
  })
_sym_db.RegisterMessage(WaitForResultResponse)

CronJob = _reflection.GeneratedProtocolMessageType('CronJob', (_message.Message,), {
  'DESCRIPTOR' : _CRONJOB,
  '__module__' : 'jetpack.proto.runtime.v1alpha1.remote_pb2'
  # @@protoc_insertion_point(class_scope:remote.CronJob)
  })
_sym_db.RegisterMessage(CronJob)


DESCRIPTOR._options = None
_SETCRONJOBSREQUEST.fields_by_name['app_id']._options = None

_REMOTEEXECUTOR = _descriptor.ServiceDescriptor(
  name='RemoteExecutor',
  full_name='remote.RemoteExecutor',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1722,
  serialized_end=2105,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateTask',
    full_name='remote.RemoteExecutor.CreateTask',
    index=0,
    containing_service=None,
    input_type=_CREATETASKREQUEST,
    output_type=_CREATETASKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PostResult',
    full_name='remote.RemoteExecutor.PostResult',
    index=1,
    containing_service=None,
    input_type=_POSTRESULTREQUEST,
    output_type=_POSTRESULTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='WaitForResult',
    full_name='remote.RemoteExecutor.WaitForResult',
    index=2,
    containing_service=None,
    input_type=_WAITFORRESULTREQUEST,
    output_type=_WAITFORRESULTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetCronJobs',
    full_name='remote.RemoteExecutor.SetCronJobs',
    index=3,
    containing_service=None,
    input_type=_SETCRONJOBSREQUEST,
    output_type=_SETCRONJOBSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RemoteCall',
    full_name='remote.RemoteExecutor.RemoteCall',
    index=4,
    containing_service=None,
    input_type=_REMOTECALLREQUEST,
    output_type=_REMOTECALLRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_REMOTEEXECUTOR)

DESCRIPTOR.services_by_name['RemoteExecutor'] = _REMOTEEXECUTOR

# @@protoc_insertion_point(module_scope)
