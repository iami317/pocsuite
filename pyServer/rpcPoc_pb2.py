# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpcPoc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0crpcPoc.proto\"R\n\x1a\x45xecPythonSerializeRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\t\"\x1a\n\nResultByte\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32\xb8\x01\n\x04\x43\x61ll\x12\x41\n\x13\x45xecPythonSerialize\x12\x1b.ExecPythonSerializeRequest\x1a\x0b.ResultByte\"\x00\x12\x42\n\x14\x43heckPythonSerialize\x12\x1b.ExecPythonSerializeRequest\x1a\x0b.ResultByte\"\x00\x12)\n\x0bhealthCheck\x12\x0b.ResultByte\x1a\x0b.ResultByte\"\x00\x42\rZ\x0b./;pocsuiteb\x06proto3')



_EXECPYTHONSERIALIZEREQUEST = DESCRIPTOR.message_types_by_name['ExecPythonSerializeRequest']
_RESULTBYTE = DESCRIPTOR.message_types_by_name['ResultByte']
ExecPythonSerializeRequest = _reflection.GeneratedProtocolMessageType('ExecPythonSerializeRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXECPYTHONSERIALIZEREQUEST,
  '__module__' : 'rpcPoc_pb2'
  # @@protoc_insertion_point(class_scope:ExecPythonSerializeRequest)
  })
_sym_db.RegisterMessage(ExecPythonSerializeRequest)

ResultByte = _reflection.GeneratedProtocolMessageType('ResultByte', (_message.Message,), {
  'DESCRIPTOR' : _RESULTBYTE,
  '__module__' : 'rpcPoc_pb2'
  # @@protoc_insertion_point(class_scope:ResultByte)
  })
_sym_db.RegisterMessage(ResultByte)

_CALL = DESCRIPTOR.services_by_name['Call']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\013./;pocsuite'
  _EXECPYTHONSERIALIZEREQUEST._serialized_start=16
  _EXECPYTHONSERIALIZEREQUEST._serialized_end=98
  _RESULTBYTE._serialized_start=100
  _RESULTBYTE._serialized_end=126
  _CALL._serialized_start=129
  _CALL._serialized_end=313
# @@protoc_insertion_point(module_scope)
