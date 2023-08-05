# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.cost_analysis.v1 import data_source_pb2 as spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2


class DataSourceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.register = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/register',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.RegisterDataSourceRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/update',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.UpdateDataSourceRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
                )
        self.update_plugin = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/update_plugin',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.UpdateDataSourcePluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
                )
        self.verify_plugin = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/verify_plugin',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/enable',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/disable',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
                )
        self.deregister = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/deregister',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.sync = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/sync',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.SyncDataSourceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/get',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.GetDataSourceRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/list',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourcesInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSource/stat',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class DataSourceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_plugin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def verify_plugin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deregister(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sync(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataSourceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.RegisterDataSourceRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.UpdateDataSourceRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.SerializeToString,
            ),
            'update_plugin': grpc.unary_unary_rpc_method_handler(
                    servicer.update_plugin,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.UpdateDataSourcePluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.SerializeToString,
            ),
            'verify_plugin': grpc.unary_unary_rpc_method_handler(
                    servicer.verify_plugin,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.SerializeToString,
            ),
            'deregister': grpc.unary_unary_rpc_method_handler(
                    servicer.deregister,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'sync': grpc.unary_unary_rpc_method_handler(
                    servicer.sync,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.SyncDataSourceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.GetDataSourceRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourcesInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.cost_analysis.v1.DataSource', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataSource(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/register',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.RegisterDataSourceRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/update',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.UpdateDataSourceRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_plugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/update_plugin',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.UpdateDataSourcePluginRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def verify_plugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/verify_plugin',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/enable',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/disable',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deregister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/deregister',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sync(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/sync',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.SyncDataSourceRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/get',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.GetDataSourceRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/list',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceQuery.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourcesInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.DataSource/stat',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__pb2.DataSourceStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
