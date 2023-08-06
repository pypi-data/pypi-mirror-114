from typing import Callable, Any

from aiohttp import web

from native_rpc.deserializer import Deserializer, JsonDeserializer
from native_rpc.exceptions import AttrNotFoundException, InvalidParamException, DeserializationException, \
    NamespaceNotFoundException, RequestException, InternalProcedureException
from native_rpc.namespace import Namespace
from native_rpc.obj_pool import ObjectPool
from native_rpc.serializer import JsonSerializer, Serializer
from native_rpc.stream import ResponseStreamWriter, BytesStreamWriter


def _get_path_param(request: web.Request, name: str, type: Callable[[str], Any] = str) -> Any:
    try:
        return type(request.match_info[name])
    except ValueError:
        raise InvalidParamException(name)


@web.middleware
async def _error_middleware(request, handler):
    try:
        return await handler(request)
    except RequestException:
        raise
    except Exception as ex:
        raise InternalProcedureException(str(ex))


class Server:
    def __init__(self, use_stream=False):
        self._use_stream = use_stream

        self._namespaces: dict[str, Namespace] = {}
        self._deserializers: dict[str, Deserializer] = {}
        self._default_deserializer: Deserializer = JsonDeserializer()
        self._serializer: Serializer = JsonSerializer()

        self._obj_pool = ObjectPool()

        self._app = web.Application(middlewares=[_error_middleware])
        self._app.add_routes([
            web.post('/functions/{namespace}/{name}', self._handle_call_func),
            web.post('/classes/{namespace}/{name}', self._handle_create_obj),
            web.delete('/objects/{idx}', self._handle_delete_obj),
            web.get('/objects/{idx}/{attr}', self._handle_get_obj_attr),
            web.post('/objects/{idx}/{attr}', self._handle_set_obj_attr),
            web.post('/objects/{idx}/{attr}/call', self._handle_call_obj_method)
        ])

    def _get_namespace(self, name: str) -> Namespace:
        ns = self._namespaces.get(name)
        if ns is None:
            raise NamespaceNotFoundException(name)
        return ns

    def _get_remote_func(self, namespace: str, name: str) -> Callable:
        ns = self._get_namespace(namespace)
        return ns.get_remote_func(name)

    def _get_remote_class(self, namespace: str, name: str) -> Any:
        ns = self._get_namespace(namespace)
        return ns.get_remote_class(name)

    def _get_deserializer(self, type: str) -> Deserializer:
        return self._deserializers.get(type, self._default_deserializer)

    async def _deserialize(self, request: web.Request) -> Any:
        deserializer = self._get_deserializer(request.content_type)
        try:
            return await deserializer.deserialize(request.content)
        except Exception as ex:
            raise DeserializationException(str(ex))

    async def _serialize_response(self, request: web.Request, obj: Any) -> web.StreamResponse:
        if self._use_stream:
            res = web.StreamResponse()
            res.content_type = self._serializer.content_type
            writer = ResponseStreamWriter(res)

            await res.prepare(request)
            await self._serializer.serialize(obj, writer)
            await res.write_eof()
            return res
        else:
            writer = BytesStreamWriter()
            await self._serializer.serialize(obj, writer)
            return web.Response(body=writer.data, content_type=self._serializer.content_type)

    async def _handle_call_func(self, request: web.Request) -> web.StreamResponse:
        namespace = _get_path_param(request, 'namespace')
        name = _get_path_param(request, 'name')
        func = self._get_remote_func(namespace, name)

        args, kwargs = await self._deserialize(request)
        ret = func(*args, **kwargs)
        return await self._serialize_response(request, ret)

    async def _handle_create_obj(self, request: web.Request) -> web.StreamResponse:
        namespace = _get_path_param(request, 'namespace')
        name = _get_path_param(request, 'name')
        cls = self._get_remote_class(namespace, name)

        args, kwargs = await self._deserialize(request)
        obj = cls(*args, **kwargs)
        idx = await self._obj_pool.append(obj)
        return web.json_response({'index': idx})

    async def _handle_delete_obj(self, request: web.Request) -> web.StreamResponse:
        idx = _get_path_param(request, 'idx', int)
        await self._obj_pool.pop(idx)
        return web.HTTPNoContent()

    async def _handle_get_obj_attr(self, request: web.Request) -> web.StreamResponse:
        idx = _get_path_param(request, 'idx', int)
        attr = _get_path_param(request, 'attr')
        entry = await self._obj_pool.get(idx)

        async with entry as obj:
            try:
                attr = getattr(obj, attr)
            except AttributeError:
                raise AttrNotFoundException(idx, attr)

            return await self._serialize_response(request, attr)

    async def _handle_set_obj_attr(self, request: web.Request) -> web.StreamResponse:
        idx = _get_path_param(request, 'idx', int)
        attr = _get_path_param(request, 'attr')
        entry = await self._obj_pool.get(idx)
        val = await self._deserialize(request)

        async with entry as obj:
            setattr(obj, attr, val)
            return web.HTTPNoContent()

    async def _handle_call_obj_method(self, request: web.Request) -> web.StreamResponse:
        idx = _get_path_param(request, 'idx', int)
        attr = _get_path_param(request, 'attr')
        entry = await self._obj_pool.get(idx)
        args, kwargs = await self._deserialize(request)

        async with entry as obj:
            try:
                func = getattr(obj, attr)
            except AttributeError:
                raise AttrNotFoundException(idx, attr)

            ret = func(*args, **kwargs)
            return await self._serialize_response(request, ret)

    def register_deserializer(self, deserializer: Deserializer) -> None:
        self._deserializers[deserializer.content_type] = deserializer

    @property
    def default_deserializer(self) -> Deserializer:
        return self._default_deserializer

    @default_deserializer.setter
    def default_deserializer(self, val: Deserializer):
        self._default_deserializer = val

    @property
    def serializer(self) -> Serializer:
        return self._serializer

    @serializer.setter
    def serializer(self, val: Serializer):
        self._serializer = val

    def add_namespace(self, ns: Namespace):
        old_ns = self._namespaces.get(ns.name)
        if old_ns is None:
            self._namespaces[ns.name] = ns
        else:
            self._namespaces[ns.name] = old_ns.merge(ns)

    def run(self, **kwargs):
        web.run_app(self._app, **kwargs)
