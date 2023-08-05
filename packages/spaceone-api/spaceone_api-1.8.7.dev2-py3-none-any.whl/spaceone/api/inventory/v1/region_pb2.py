# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/inventory/v1/region.proto
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
  name='spaceone/api/inventory/v1/region.proto',
  package='spaceone.api.inventory.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n&spaceone/api/inventory/v1/region.proto\x12\x19spaceone.api.inventory.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x84\x01\n\x13\x43reateRegionRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bregion_code\x18\x02 \x01(\t\x12\x10\n\x08provider\x18\x03 \x01(\t\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x05 \x01(\t\"p\n\x13UpdateRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"5\n\rRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"F\n\x10GetRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xa8\x01\n\x0bRegionQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x11\n\tregion_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nregion_key\x18\x04 \x01(\t\x12\x13\n\x0bregion_code\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x11\n\tdomain_id\x18\x07 \x01(\t\"\xca\x01\n\nRegionInfo\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\nregion_key\x18\x03 \x01(\t\x12\x13\n\x0bregion_code\x18\x04 \x01(\t\x12\x10\n\x08provider\x18\x05 \x01(\t\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\t\"Z\n\x0bRegionsInfo\x12\x36\n\x07results\x18\x01 \x03(\x0b\x32%.spaceone.api.inventory.v1.RegionInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"Z\n\x0fRegionStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\x99\x06\n\x06Region\x12~\n\x06\x63reate\x12..spaceone.api.inventory.v1.CreateRegionRequest\x1a%.spaceone.api.inventory.v1.RegionInfo\"\x1d\x82\xd3\xe4\x93\x02\x17\"\x15/inventory/v1/regions\x12\x89\x01\n\x06update\x12..spaceone.api.inventory.v1.UpdateRegionRequest\x1a%.spaceone.api.inventory.v1.RegionInfo\"(\x82\xd3\xe4\x93\x02\"\x1a /inventory/v1/region/{region_id}\x12t\n\x06\x64\x65lete\x12(.spaceone.api.inventory.v1.RegionRequest\x1a\x16.google.protobuf.Empty\"(\x82\xd3\xe4\x93\x02\"* /inventory/v1/region/{region_id}\x12\x83\x01\n\x03get\x12+.spaceone.api.inventory.v1.GetRegionRequest\x1a%.spaceone.api.inventory.v1.RegionInfo\"(\x82\xd3\xe4\x93\x02\"\x12 /inventory/v1/region/{region_id}\x12\x95\x01\n\x04list\x12&.spaceone.api.inventory.v1.RegionQuery\x1a&.spaceone.api.inventory.v1.RegionsInfo\"=\x82\xd3\xe4\x93\x02\x37\x12\x15/inventory/v1/regionsZ\x1e\"\x1c/inventory/v1/regions/search\x12o\n\x04stat\x12*.spaceone.api.inventory.v1.RegionStatQuery\x1a\x17.google.protobuf.Struct\"\"\x82\xd3\xe4\x93\x02\x1c\"\x1a/inventory/v1/regions/statb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_query__pb2.DESCRIPTOR,])




_CREATEREGIONREQUEST = _descriptor.Descriptor(
  name='CreateRegionRequest',
  full_name='spaceone.api.inventory.v1.CreateRegionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.inventory.v1.CreateRegionRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_code', full_name='spaceone.api.inventory.v1.CreateRegionRequest.region_code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='provider', full_name='spaceone.api.inventory.v1.CreateRegionRequest.provider', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='spaceone.api.inventory.v1.CreateRegionRequest.tags', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.CreateRegionRequest.domain_id', index=4,
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
  serialized_start=193,
  serialized_end=325,
)


_UPDATEREGIONREQUEST = _descriptor.Descriptor(
  name='UpdateRegionRequest',
  full_name='spaceone.api.inventory.v1.UpdateRegionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='region_id', full_name='spaceone.api.inventory.v1.UpdateRegionRequest.region_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.inventory.v1.UpdateRegionRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='spaceone.api.inventory.v1.UpdateRegionRequest.tags', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.UpdateRegionRequest.domain_id', index=3,
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
  serialized_start=327,
  serialized_end=439,
)


_REGIONREQUEST = _descriptor.Descriptor(
  name='RegionRequest',
  full_name='spaceone.api.inventory.v1.RegionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='region_id', full_name='spaceone.api.inventory.v1.RegionRequest.region_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.RegionRequest.domain_id', index=1,
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
  serialized_start=441,
  serialized_end=494,
)


_GETREGIONREQUEST = _descriptor.Descriptor(
  name='GetRegionRequest',
  full_name='spaceone.api.inventory.v1.GetRegionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='region_id', full_name='spaceone.api.inventory.v1.GetRegionRequest.region_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.GetRegionRequest.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='only', full_name='spaceone.api.inventory.v1.GetRegionRequest.only', index=2,
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
  serialized_start=496,
  serialized_end=566,
)


_REGIONQUERY = _descriptor.Descriptor(
  name='RegionQuery',
  full_name='spaceone.api.inventory.v1.RegionQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.inventory.v1.RegionQuery.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_id', full_name='spaceone.api.inventory.v1.RegionQuery.region_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.inventory.v1.RegionQuery.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_key', full_name='spaceone.api.inventory.v1.RegionQuery.region_key', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_code', full_name='spaceone.api.inventory.v1.RegionQuery.region_code', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='provider', full_name='spaceone.api.inventory.v1.RegionQuery.provider', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.RegionQuery.domain_id', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=569,
  serialized_end=737,
)


_REGIONINFO = _descriptor.Descriptor(
  name='RegionInfo',
  full_name='spaceone.api.inventory.v1.RegionInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='region_id', full_name='spaceone.api.inventory.v1.RegionInfo.region_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.inventory.v1.RegionInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_key', full_name='spaceone.api.inventory.v1.RegionInfo.region_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_code', full_name='spaceone.api.inventory.v1.RegionInfo.region_code', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='provider', full_name='spaceone.api.inventory.v1.RegionInfo.provider', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='spaceone.api.inventory.v1.RegionInfo.tags', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.RegionInfo.domain_id', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='spaceone.api.inventory.v1.RegionInfo.created_at', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='spaceone.api.inventory.v1.RegionInfo.updated_at', index=8,
      number=9, type=9, cpp_type=9, label=1,
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
  serialized_start=740,
  serialized_end=942,
)


_REGIONSINFO = _descriptor.Descriptor(
  name='RegionsInfo',
  full_name='spaceone.api.inventory.v1.RegionsInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='spaceone.api.inventory.v1.RegionsInfo.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.inventory.v1.RegionsInfo.total_count', index=1,
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
  serialized_start=944,
  serialized_end=1034,
)


_REGIONSTATQUERY = _descriptor.Descriptor(
  name='RegionStatQuery',
  full_name='spaceone.api.inventory.v1.RegionStatQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.inventory.v1.RegionStatQuery.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.inventory.v1.RegionStatQuery.domain_id', index=1,
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
  serialized_start=1036,
  serialized_end=1126,
)

_CREATEREGIONREQUEST.fields_by_name['tags'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_UPDATEREGIONREQUEST.fields_by_name['tags'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_REGIONQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._QUERY
_REGIONINFO.fields_by_name['tags'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_REGIONSINFO.fields_by_name['results'].message_type = _REGIONINFO
_REGIONSTATQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
DESCRIPTOR.message_types_by_name['CreateRegionRequest'] = _CREATEREGIONREQUEST
DESCRIPTOR.message_types_by_name['UpdateRegionRequest'] = _UPDATEREGIONREQUEST
DESCRIPTOR.message_types_by_name['RegionRequest'] = _REGIONREQUEST
DESCRIPTOR.message_types_by_name['GetRegionRequest'] = _GETREGIONREQUEST
DESCRIPTOR.message_types_by_name['RegionQuery'] = _REGIONQUERY
DESCRIPTOR.message_types_by_name['RegionInfo'] = _REGIONINFO
DESCRIPTOR.message_types_by_name['RegionsInfo'] = _REGIONSINFO
DESCRIPTOR.message_types_by_name['RegionStatQuery'] = _REGIONSTATQUERY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateRegionRequest = _reflection.GeneratedProtocolMessageType('CreateRegionRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEREGIONREQUEST,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.CreateRegionRequest)
  })
_sym_db.RegisterMessage(CreateRegionRequest)

UpdateRegionRequest = _reflection.GeneratedProtocolMessageType('UpdateRegionRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEREGIONREQUEST,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.UpdateRegionRequest)
  })
_sym_db.RegisterMessage(UpdateRegionRequest)

RegionRequest = _reflection.GeneratedProtocolMessageType('RegionRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGIONREQUEST,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.RegionRequest)
  })
_sym_db.RegisterMessage(RegionRequest)

GetRegionRequest = _reflection.GeneratedProtocolMessageType('GetRegionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETREGIONREQUEST,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.GetRegionRequest)
  })
_sym_db.RegisterMessage(GetRegionRequest)

RegionQuery = _reflection.GeneratedProtocolMessageType('RegionQuery', (_message.Message,), {
  'DESCRIPTOR' : _REGIONQUERY,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.RegionQuery)
  })
_sym_db.RegisterMessage(RegionQuery)

RegionInfo = _reflection.GeneratedProtocolMessageType('RegionInfo', (_message.Message,), {
  'DESCRIPTOR' : _REGIONINFO,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.RegionInfo)
  })
_sym_db.RegisterMessage(RegionInfo)

RegionsInfo = _reflection.GeneratedProtocolMessageType('RegionsInfo', (_message.Message,), {
  'DESCRIPTOR' : _REGIONSINFO,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.RegionsInfo)
  })
_sym_db.RegisterMessage(RegionsInfo)

RegionStatQuery = _reflection.GeneratedProtocolMessageType('RegionStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _REGIONSTATQUERY,
  '__module__' : 'spaceone.api.inventory.v1.region_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.RegionStatQuery)
  })
_sym_db.RegisterMessage(RegionStatQuery)



_REGION = _descriptor.ServiceDescriptor(
  name='Region',
  full_name='spaceone.api.inventory.v1.Region',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1129,
  serialized_end=1922,
  methods=[
  _descriptor.MethodDescriptor(
    name='create',
    full_name='spaceone.api.inventory.v1.Region.create',
    index=0,
    containing_service=None,
    input_type=_CREATEREGIONREQUEST,
    output_type=_REGIONINFO,
    serialized_options=b'\202\323\344\223\002\027\"\025/inventory/v1/regions',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='update',
    full_name='spaceone.api.inventory.v1.Region.update',
    index=1,
    containing_service=None,
    input_type=_UPDATEREGIONREQUEST,
    output_type=_REGIONINFO,
    serialized_options=b'\202\323\344\223\002\"\032 /inventory/v1/region/{region_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete',
    full_name='spaceone.api.inventory.v1.Region.delete',
    index=2,
    containing_service=None,
    input_type=_REGIONREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\"* /inventory/v1/region/{region_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get',
    full_name='spaceone.api.inventory.v1.Region.get',
    index=3,
    containing_service=None,
    input_type=_GETREGIONREQUEST,
    output_type=_REGIONINFO,
    serialized_options=b'\202\323\344\223\002\"\022 /inventory/v1/region/{region_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='list',
    full_name='spaceone.api.inventory.v1.Region.list',
    index=4,
    containing_service=None,
    input_type=_REGIONQUERY,
    output_type=_REGIONSINFO,
    serialized_options=b'\202\323\344\223\0027\022\025/inventory/v1/regionsZ\036\"\034/inventory/v1/regions/search',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='stat',
    full_name='spaceone.api.inventory.v1.Region.stat',
    index=5,
    containing_service=None,
    input_type=_REGIONSTATQUERY,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\034\"\032/inventory/v1/regions/stat',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_REGION)

DESCRIPTOR.services_by_name['Region'] = _REGION

# @@protoc_insertion_point(module_scope)
