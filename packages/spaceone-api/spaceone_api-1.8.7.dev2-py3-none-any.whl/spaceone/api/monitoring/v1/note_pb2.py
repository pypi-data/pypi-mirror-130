# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/v1/note.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/monitoring/v1/note.proto',
  package='spaceone.api.monitoring.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%spaceone/api/monitoring/v1/note.proto\x12\x1aspaceone.api.monitoring.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"F\n\x11\x43reateNoteRequest\x12\x10\n\x08\x61lert_id\x18\x01 \x01(\t\x12\x0c\n\x04note\x18\x02 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"E\n\x11UpdateNoteRequest\x12\x0f\n\x07note_id\x18\x01 \x01(\t\x12\x0c\n\x04note\x18\x02 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"1\n\x0bNoteRequest\x12\x0f\n\x07note_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"B\n\x0eGetNoteRequest\x12\x0f\n\x07note_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\x95\x01\n\tNoteQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x0f\n\x07note_id\x18\x02 \x01(\t\x12\x10\n\x08\x61lert_id\x18\x03 \x01(\t\x12\x12\n\ncreated_by\x18\x04 \x01(\t\x12\x12\n\nproject_id\x18\x05 \x01(\t\x12\x11\n\tdomain_id\x18\x06 \x01(\t\"\x8a\x01\n\x08NoteInfo\x12\x0f\n\x07note_id\x18\x01 \x01(\t\x12\x10\n\x08\x61lert_id\x18\x02 \x01(\t\x12\x0c\n\x04note\x18\x03 \x01(\t\x12\x12\n\ncreated_by\x18\x0b \x01(\t\x12\x12\n\nproject_id\x18\x0c \x01(\t\x12\x11\n\tdomain_id\x18\r \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\"W\n\tNotesInfo\x12\x35\n\x07results\x18\x01 \x03(\x0b\x32$.spaceone.api.monitoring.v1.NoteInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"X\n\rNoteStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xff\x05\n\x04Note\x12{\n\x06\x63reate\x12-.spaceone.api.monitoring.v1.CreateNoteRequest\x1a$.spaceone.api.monitoring.v1.NoteInfo\"\x1c\x82\xd3\xe4\x93\x02\x16\"\x14/monitoring/v1/notes\x12\x84\x01\n\x06update\x12-.spaceone.api.monitoring.v1.UpdateNoteRequest\x1a$.spaceone.api.monitoring.v1.NoteInfo\"%\x82\xd3\xe4\x93\x02\x1f\x1a\x1d/monitoring/v1/note/{note_id}\x12p\n\x06\x64\x65lete\x12\'.spaceone.api.monitoring.v1.NoteRequest\x1a\x16.google.protobuf.Empty\"%\x82\xd3\xe4\x93\x02\x1f*\x1d/monitoring/v1/note/{note_id}\x12~\n\x03get\x12*.spaceone.api.monitoring.v1.GetNoteRequest\x1a$.spaceone.api.monitoring.v1.NoteInfo\"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/monitoring/v1/note/{note_id}\x12\x91\x01\n\x04list\x12%.spaceone.api.monitoring.v1.NoteQuery\x1a%.spaceone.api.monitoring.v1.NotesInfo\";\x82\xd3\xe4\x93\x02\x35\x12\x14/monitoring/v1/notesZ\x1d\"\x1b/monitoring/v1/notes/search\x12m\n\x04stat\x12).spaceone.api.monitoring.v1.NoteStatQuery\x1a\x17.google.protobuf.Struct\"!\x82\xd3\xe4\x93\x02\x1b\"\x19/monitoring/v1/notes/statb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_query__pb2.DESCRIPTOR,])




_CREATENOTEREQUEST = _descriptor.Descriptor(
  name='CreateNoteRequest',
  full_name='spaceone.api.monitoring.v1.CreateNoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='alert_id', full_name='spaceone.api.monitoring.v1.CreateNoteRequest.alert_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note', full_name='spaceone.api.monitoring.v1.CreateNoteRequest.note', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.CreateNoteRequest.domain_id', index=2,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=192,
  serialized_end=262,
)


_UPDATENOTEREQUEST = _descriptor.Descriptor(
  name='UpdateNoteRequest',
  full_name='spaceone.api.monitoring.v1.UpdateNoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='note_id', full_name='spaceone.api.monitoring.v1.UpdateNoteRequest.note_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note', full_name='spaceone.api.monitoring.v1.UpdateNoteRequest.note', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.UpdateNoteRequest.domain_id', index=2,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=264,
  serialized_end=333,
)


_NOTEREQUEST = _descriptor.Descriptor(
  name='NoteRequest',
  full_name='spaceone.api.monitoring.v1.NoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='note_id', full_name='spaceone.api.monitoring.v1.NoteRequest.note_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.NoteRequest.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=335,
  serialized_end=384,
)


_GETNOTEREQUEST = _descriptor.Descriptor(
  name='GetNoteRequest',
  full_name='spaceone.api.monitoring.v1.GetNoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='note_id', full_name='spaceone.api.monitoring.v1.GetNoteRequest.note_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.GetNoteRequest.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='only', full_name='spaceone.api.monitoring.v1.GetNoteRequest.only', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=386,
  serialized_end=452,
)


_NOTEQUERY = _descriptor.Descriptor(
  name='NoteQuery',
  full_name='spaceone.api.monitoring.v1.NoteQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.monitoring.v1.NoteQuery.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note_id', full_name='spaceone.api.monitoring.v1.NoteQuery.note_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='alert_id', full_name='spaceone.api.monitoring.v1.NoteQuery.alert_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_by', full_name='spaceone.api.monitoring.v1.NoteQuery.created_by', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_id', full_name='spaceone.api.monitoring.v1.NoteQuery.project_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.NoteQuery.domain_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
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
  serialized_start=455,
  serialized_end=604,
)


_NOTEINFO = _descriptor.Descriptor(
  name='NoteInfo',
  full_name='spaceone.api.monitoring.v1.NoteInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='note_id', full_name='spaceone.api.monitoring.v1.NoteInfo.note_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='alert_id', full_name='spaceone.api.monitoring.v1.NoteInfo.alert_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note', full_name='spaceone.api.monitoring.v1.NoteInfo.note', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_by', full_name='spaceone.api.monitoring.v1.NoteInfo.created_by', index=3,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_id', full_name='spaceone.api.monitoring.v1.NoteInfo.project_id', index=4,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.NoteInfo.domain_id', index=5,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='spaceone.api.monitoring.v1.NoteInfo.created_at', index=6,
      number=21, type=9, cpp_type=9, label=1,
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
  serialized_start=607,
  serialized_end=745,
)


_NOTESINFO = _descriptor.Descriptor(
  name='NotesInfo',
  full_name='spaceone.api.monitoring.v1.NotesInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='spaceone.api.monitoring.v1.NotesInfo.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.monitoring.v1.NotesInfo.total_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=747,
  serialized_end=834,
)


_NOTESTATQUERY = _descriptor.Descriptor(
  name='NoteStatQuery',
  full_name='spaceone.api.monitoring.v1.NoteStatQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.monitoring.v1.NoteStatQuery.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.monitoring.v1.NoteStatQuery.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=836,
  serialized_end=924,
)

_NOTEQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._QUERY
_NOTESINFO.fields_by_name['results'].message_type = _NOTEINFO
_NOTESTATQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
DESCRIPTOR.message_types_by_name['CreateNoteRequest'] = _CREATENOTEREQUEST
DESCRIPTOR.message_types_by_name['UpdateNoteRequest'] = _UPDATENOTEREQUEST
DESCRIPTOR.message_types_by_name['NoteRequest'] = _NOTEREQUEST
DESCRIPTOR.message_types_by_name['GetNoteRequest'] = _GETNOTEREQUEST
DESCRIPTOR.message_types_by_name['NoteQuery'] = _NOTEQUERY
DESCRIPTOR.message_types_by_name['NoteInfo'] = _NOTEINFO
DESCRIPTOR.message_types_by_name['NotesInfo'] = _NOTESINFO
DESCRIPTOR.message_types_by_name['NoteStatQuery'] = _NOTESTATQUERY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateNoteRequest = _reflection.GeneratedProtocolMessageType('CreateNoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATENOTEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.CreateNoteRequest)
  })
_sym_db.RegisterMessage(CreateNoteRequest)

UpdateNoteRequest = _reflection.GeneratedProtocolMessageType('UpdateNoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATENOTEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.UpdateNoteRequest)
  })
_sym_db.RegisterMessage(UpdateNoteRequest)

NoteRequest = _reflection.GeneratedProtocolMessageType('NoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _NOTEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.NoteRequest)
  })
_sym_db.RegisterMessage(NoteRequest)

GetNoteRequest = _reflection.GeneratedProtocolMessageType('GetNoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETNOTEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.GetNoteRequest)
  })
_sym_db.RegisterMessage(GetNoteRequest)

NoteQuery = _reflection.GeneratedProtocolMessageType('NoteQuery', (_message.Message,), {
  'DESCRIPTOR' : _NOTEQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.NoteQuery)
  })
_sym_db.RegisterMessage(NoteQuery)

NoteInfo = _reflection.GeneratedProtocolMessageType('NoteInfo', (_message.Message,), {
  'DESCRIPTOR' : _NOTEINFO,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.NoteInfo)
  })
_sym_db.RegisterMessage(NoteInfo)

NotesInfo = _reflection.GeneratedProtocolMessageType('NotesInfo', (_message.Message,), {
  'DESCRIPTOR' : _NOTESINFO,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.NotesInfo)
  })
_sym_db.RegisterMessage(NotesInfo)

NoteStatQuery = _reflection.GeneratedProtocolMessageType('NoteStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _NOTESTATQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.note_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.NoteStatQuery)
  })
_sym_db.RegisterMessage(NoteStatQuery)



_NOTE = _descriptor.ServiceDescriptor(
  name='Note',
  full_name='spaceone.api.monitoring.v1.Note',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=927,
  serialized_end=1694,
  methods=[
  _descriptor.MethodDescriptor(
    name='create',
    full_name='spaceone.api.monitoring.v1.Note.create',
    index=0,
    containing_service=None,
    input_type=_CREATENOTEREQUEST,
    output_type=_NOTEINFO,
    serialized_options=b'\202\323\344\223\002\026\"\024/monitoring/v1/notes',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='update',
    full_name='spaceone.api.monitoring.v1.Note.update',
    index=1,
    containing_service=None,
    input_type=_UPDATENOTEREQUEST,
    output_type=_NOTEINFO,
    serialized_options=b'\202\323\344\223\002\037\032\035/monitoring/v1/note/{note_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete',
    full_name='spaceone.api.monitoring.v1.Note.delete',
    index=2,
    containing_service=None,
    input_type=_NOTEREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\037*\035/monitoring/v1/note/{note_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get',
    full_name='spaceone.api.monitoring.v1.Note.get',
    index=3,
    containing_service=None,
    input_type=_GETNOTEREQUEST,
    output_type=_NOTEINFO,
    serialized_options=b'\202\323\344\223\002\037\022\035/monitoring/v1/note/{note_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='list',
    full_name='spaceone.api.monitoring.v1.Note.list',
    index=4,
    containing_service=None,
    input_type=_NOTEQUERY,
    output_type=_NOTESINFO,
    serialized_options=b'\202\323\344\223\0025\022\024/monitoring/v1/notesZ\035\"\033/monitoring/v1/notes/search',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='stat',
    full_name='spaceone.api.monitoring.v1.Note.stat',
    index=5,
    containing_service=None,
    input_type=_NOTESTATQUERY,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\033\"\031/monitoring/v1/notes/stat',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_NOTE)

DESCRIPTOR.services_by_name['Note'] = _NOTE

# @@protoc_insertion_point(module_scope)
