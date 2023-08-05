# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/identity/plugin/auth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/identity/plugin/auth.proto',
  package='spaceone.api.identity.plugin',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'spaceone/api/identity/plugin/auth.proto\x12\x1cspaceone.api.identity.plugin\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"7\n\x0bInitRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"w\n\rVerifyRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x03 \x01(\t\"\x97\x01\n\x0b\x46indRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x0f\n\x07keyword\x18\x04 \x01(\t\x12\x0e\n\x06schema\x18\x05 \x01(\t\"\xa9\x01\n\x0cLoginRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x31\n\x10user_credentials\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x04 \x01(\t\"\xd4\x01\n\x08UserInfo\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x0e\n\x06mobile\x18\x04 \x01(\t\x12\r\n\x05group\x18\x05 \x01(\t\x12;\n\x05state\x18\x06 \x01(\x0e\x32,.spaceone.api.identity.plugin.UserInfo.State\">\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\x12\x10\n\x0cUNIDENTIFIED\x10\x03\"g\n\tUsersInfo\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32&.spaceone.api.identity.plugin.UserInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x12\x0c\n\x04more\x18\x03 \x01(\x08\":\n\x0e\x41uthVerifyInfo\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"7\n\nPluginInfo\x12)\n\x08metadata\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct2\xf3\x02\n\x04\x41uth\x12]\n\x04init\x12).spaceone.api.identity.plugin.InitRequest\x1a(.spaceone.api.identity.plugin.PluginInfo\"\x00\x12O\n\x06verify\x12+.spaceone.api.identity.plugin.VerifyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\\\n\x04\x66ind\x12).spaceone.api.identity.plugin.FindRequest\x1a\'.spaceone.api.identity.plugin.UsersInfo\"\x00\x12]\n\x05login\x12*.spaceone.api.identity.plugin.LoginRequest\x1a&.spaceone.api.identity.plugin.UserInfo\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])



_USERINFO_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='spaceone.api.identity.plugin.UserInfo.State',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ENABLED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DISABLED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNIDENTIFIED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=787,
  serialized_end=849,
)
_sym_db.RegisterEnumDescriptor(_USERINFO_STATE)


_INITREQUEST = _descriptor.Descriptor(
  name='InitRequest',
  full_name='spaceone.api.identity.plugin.InitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.identity.plugin.InitRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=132,
  serialized_end=187,
)


_VERIFYREQUEST = _descriptor.Descriptor(
  name='VerifyRequest',
  full_name='spaceone.api.identity.plugin.VerifyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.identity.plugin.VerifyRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.identity.plugin.VerifyRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema', full_name='spaceone.api.identity.plugin.VerifyRequest.schema', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=189,
  serialized_end=308,
)


_FINDREQUEST = _descriptor.Descriptor(
  name='FindRequest',
  full_name='spaceone.api.identity.plugin.FindRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.identity.plugin.FindRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.identity.plugin.FindRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='spaceone.api.identity.plugin.FindRequest.user_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keyword', full_name='spaceone.api.identity.plugin.FindRequest.keyword', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema', full_name='spaceone.api.identity.plugin.FindRequest.schema', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=311,
  serialized_end=462,
)


_LOGINREQUEST = _descriptor.Descriptor(
  name='LoginRequest',
  full_name='spaceone.api.identity.plugin.LoginRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.identity.plugin.LoginRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.identity.plugin.LoginRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_credentials', full_name='spaceone.api.identity.plugin.LoginRequest.user_credentials', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema', full_name='spaceone.api.identity.plugin.LoginRequest.schema', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=465,
  serialized_end=634,
)


_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='spaceone.api.identity.plugin.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_id', full_name='spaceone.api.identity.plugin.UserInfo.user_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.identity.plugin.UserInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='spaceone.api.identity.plugin.UserInfo.email', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mobile', full_name='spaceone.api.identity.plugin.UserInfo.mobile', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group', full_name='spaceone.api.identity.plugin.UserInfo.group', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='spaceone.api.identity.plugin.UserInfo.state', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USERINFO_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=637,
  serialized_end=849,
)


_USERSINFO = _descriptor.Descriptor(
  name='UsersInfo',
  full_name='spaceone.api.identity.plugin.UsersInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='spaceone.api.identity.plugin.UsersInfo.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.identity.plugin.UsersInfo.total_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='more', full_name='spaceone.api.identity.plugin.UsersInfo.more', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=851,
  serialized_end=954,
)


_AUTHVERIFYINFO = _descriptor.Descriptor(
  name='AuthVerifyInfo',
  full_name='spaceone.api.identity.plugin.AuthVerifyInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.identity.plugin.AuthVerifyInfo.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=956,
  serialized_end=1014,
)


_PLUGININFO = _descriptor.Descriptor(
  name='PluginInfo',
  full_name='spaceone.api.identity.plugin.PluginInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='spaceone.api.identity.plugin.PluginInfo.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1016,
  serialized_end=1071,
)

_INITREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_VERIFYREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_VERIFYREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_FINDREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_FINDREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_LOGINREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_LOGINREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_LOGINREQUEST.fields_by_name['user_credentials'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_USERINFO.fields_by_name['state'].enum_type = _USERINFO_STATE
_USERINFO_STATE.containing_type = _USERINFO
_USERSINFO.fields_by_name['results'].message_type = _USERINFO
_AUTHVERIFYINFO.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_PLUGININFO.fields_by_name['metadata'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name['InitRequest'] = _INITREQUEST
DESCRIPTOR.message_types_by_name['VerifyRequest'] = _VERIFYREQUEST
DESCRIPTOR.message_types_by_name['FindRequest'] = _FINDREQUEST
DESCRIPTOR.message_types_by_name['LoginRequest'] = _LOGINREQUEST
DESCRIPTOR.message_types_by_name['UserInfo'] = _USERINFO
DESCRIPTOR.message_types_by_name['UsersInfo'] = _USERSINFO
DESCRIPTOR.message_types_by_name['AuthVerifyInfo'] = _AUTHVERIFYINFO
DESCRIPTOR.message_types_by_name['PluginInfo'] = _PLUGININFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InitRequest = _reflection.GeneratedProtocolMessageType('InitRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITREQUEST,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.InitRequest)
  })
_sym_db.RegisterMessage(InitRequest)

VerifyRequest = _reflection.GeneratedProtocolMessageType('VerifyRequest', (_message.Message,), {
  'DESCRIPTOR' : _VERIFYREQUEST,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.VerifyRequest)
  })
_sym_db.RegisterMessage(VerifyRequest)

FindRequest = _reflection.GeneratedProtocolMessageType('FindRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINDREQUEST,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.FindRequest)
  })
_sym_db.RegisterMessage(FindRequest)

LoginRequest = _reflection.GeneratedProtocolMessageType('LoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINREQUEST,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.LoginRequest)
  })
_sym_db.RegisterMessage(LoginRequest)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERINFO,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.UserInfo)
  })
_sym_db.RegisterMessage(UserInfo)

UsersInfo = _reflection.GeneratedProtocolMessageType('UsersInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERSINFO,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.UsersInfo)
  })
_sym_db.RegisterMessage(UsersInfo)

AuthVerifyInfo = _reflection.GeneratedProtocolMessageType('AuthVerifyInfo', (_message.Message,), {
  'DESCRIPTOR' : _AUTHVERIFYINFO,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.AuthVerifyInfo)
  })
_sym_db.RegisterMessage(AuthVerifyInfo)

PluginInfo = _reflection.GeneratedProtocolMessageType('PluginInfo', (_message.Message,), {
  'DESCRIPTOR' : _PLUGININFO,
  '__module__' : 'spaceone.api.identity.plugin.auth_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.plugin.PluginInfo)
  })
_sym_db.RegisterMessage(PluginInfo)



_AUTH = _descriptor.ServiceDescriptor(
  name='Auth',
  full_name='spaceone.api.identity.plugin.Auth',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1074,
  serialized_end=1445,
  methods=[
  _descriptor.MethodDescriptor(
    name='init',
    full_name='spaceone.api.identity.plugin.Auth.init',
    index=0,
    containing_service=None,
    input_type=_INITREQUEST,
    output_type=_PLUGININFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='verify',
    full_name='spaceone.api.identity.plugin.Auth.verify',
    index=1,
    containing_service=None,
    input_type=_VERIFYREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='find',
    full_name='spaceone.api.identity.plugin.Auth.find',
    index=2,
    containing_service=None,
    input_type=_FINDREQUEST,
    output_type=_USERSINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='login',
    full_name='spaceone.api.identity.plugin.Auth.login',
    index=3,
    containing_service=None,
    input_type=_LOGINREQUEST,
    output_type=_USERINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUTH)

DESCRIPTOR.services_by_name['Auth'] = _AUTH

# @@protoc_insertion_point(module_scope)
