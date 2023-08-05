# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: ozonmp/rcn_production_api/v1/rcn_production_api.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import validate.validate_pb2
import google.api.annotations_pb2
import google.protobuf.timestamp_pb2
import ozonmp.rcn_production_api.v1.rcn_production_api_pb2


class RcnProductionApiServiceBase(abc.ABC):

    @abc.abstractmethod
    async def AddProductionV1(self, stream: 'grpclib.server.Stream[ozonmp.rcn_production_api.v1.rcn_production_api_pb2.AddProductionV1Request, ozonmp.rcn_production_api.v1.rcn_production_api_pb2.AddProductionV1Response]') -> None:
        pass

    @abc.abstractmethod
    async def UpdateProductionV1(self, stream: 'grpclib.server.Stream[ozonmp.rcn_production_api.v1.rcn_production_api_pb2.UpdateProductionV1Request, ozonmp.rcn_production_api.v1.rcn_production_api_pb2.UpdateProductionV1Response]') -> None:
        pass

    @abc.abstractmethod
    async def GetProductionV1(self, stream: 'grpclib.server.Stream[ozonmp.rcn_production_api.v1.rcn_production_api_pb2.GetProductionV1Request, ozonmp.rcn_production_api.v1.rcn_production_api_pb2.GetProductionV1Response]') -> None:
        pass

    @abc.abstractmethod
    async def ListProductionV1(self, stream: 'grpclib.server.Stream[ozonmp.rcn_production_api.v1.rcn_production_api_pb2.ListProductionV1Request, ozonmp.rcn_production_api.v1.rcn_production_api_pb2.ListProductionV1Response]') -> None:
        pass

    @abc.abstractmethod
    async def RemoveProductionV1(self, stream: 'grpclib.server.Stream[ozonmp.rcn_production_api.v1.rcn_production_api_pb2.RemoveProductionV1Request, ozonmp.rcn_production_api.v1.rcn_production_api_pb2.RemoveProductionV1Response]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/AddProductionV1': grpclib.const.Handler(
                self.AddProductionV1,
                grpclib.const.Cardinality.UNARY_UNARY,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.AddProductionV1Request,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.AddProductionV1Response,
            ),
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/UpdateProductionV1': grpclib.const.Handler(
                self.UpdateProductionV1,
                grpclib.const.Cardinality.UNARY_UNARY,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.UpdateProductionV1Request,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.UpdateProductionV1Response,
            ),
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/GetProductionV1': grpclib.const.Handler(
                self.GetProductionV1,
                grpclib.const.Cardinality.UNARY_UNARY,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.GetProductionV1Request,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.GetProductionV1Response,
            ),
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/ListProductionV1': grpclib.const.Handler(
                self.ListProductionV1,
                grpclib.const.Cardinality.UNARY_UNARY,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.ListProductionV1Request,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.ListProductionV1Response,
            ),
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/RemoveProductionV1': grpclib.const.Handler(
                self.RemoveProductionV1,
                grpclib.const.Cardinality.UNARY_UNARY,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.RemoveProductionV1Request,
                ozonmp.rcn_production_api.v1.rcn_production_api_pb2.RemoveProductionV1Response,
            ),
        }


class RcnProductionApiServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.AddProductionV1 = grpclib.client.UnaryUnaryMethod(
            channel,
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/AddProductionV1',
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.AddProductionV1Request,
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.AddProductionV1Response,
        )
        self.UpdateProductionV1 = grpclib.client.UnaryUnaryMethod(
            channel,
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/UpdateProductionV1',
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.UpdateProductionV1Request,
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.UpdateProductionV1Response,
        )
        self.GetProductionV1 = grpclib.client.UnaryUnaryMethod(
            channel,
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/GetProductionV1',
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.GetProductionV1Request,
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.GetProductionV1Response,
        )
        self.ListProductionV1 = grpclib.client.UnaryUnaryMethod(
            channel,
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/ListProductionV1',
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.ListProductionV1Request,
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.ListProductionV1Response,
        )
        self.RemoveProductionV1 = grpclib.client.UnaryUnaryMethod(
            channel,
            '/ozonmp.rcn_production_api.v1.RcnProductionApiService/RemoveProductionV1',
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.RemoveProductionV1Request,
            ozonmp.rcn_production_api.v1.rcn_production_api_pb2.RemoveProductionV1Response,
        )
