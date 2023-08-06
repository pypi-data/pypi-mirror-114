import io
from typing import Callable, Any, Dict, Optional, TypeVar, Tuple, BinaryIO
from urllib.parse import urljoin

from requests import Session, Response

from native_rpc.exceptions import exceptions_map
from native_rpc_client.deserializer import Deserializer, JsonDeserializer
from native_rpc_client.serializer import JsonSerializer, Serializer


def _raise_for_status(response: Response) -> None:
    if 400 <= response.status_code < 600:
        err = response.json()
        type = err.pop('type')
        raise exceptions_map[type](**err)


class Client:
    def __init__(self, base_url):
        self._base_url = base_url
        self._session = Session()

        self._deserializers: Dict[str, Deserializer] = {}
        self._default_deserializer: Deserializer = JsonDeserializer()
        self._serializer: Serializer = JsonSerializer()

    def _get_url(self, path: str) -> str:
        return urljoin(self._base_url, path)

    def _get_deserializer(self, type: str) -> Deserializer:
        return self._deserializers.get(type, self._default_deserializer)

    def _deserialize(self, response: Response) -> Any:
        deserializer = self._get_deserializer(response.headers['Content-Type'])
        # TODO: stream response
        return deserializer.deserialize(io.BytesIO(response.content))

    def register_deserializer(self, deserializer: Deserializer) -> None:
        self._deserializers[deserializer.content_type] = deserializer

    def _serialize(self, obj: Any) -> BinaryIO:
        stream = io.BytesIO()
        self._serializer.serialize(obj, stream)
        stream.seek(0, io.SEEK_SET)
        return stream

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

    def call_func(self, namespace: str, name: str, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        data = self._serialize((args, kwargs))
        headers = {'content-type': self._serializer.content_type}
        res = self._session.post(self._get_url(f'/functions/{namespace}/{name}'), data=data,
                                 headers=headers)
        _raise_for_status(res)
        return self._deserialize(res)

    def create_obj(self, namespace: str, name: str, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> int:
        data = self._serialize((args, kwargs))
        headers = {'content-type': self._serializer.content_type}
        res = self._session.post(self._get_url(f'/classes/{namespace}/{name}'), data, headers=headers)
        _raise_for_status(res)
        res = res.json()
        return res['index']

    def delete_obj(self, idx: int) -> None:
        res = self._session.delete(self._get_url(f'/objects/{idx}'))
        _raise_for_status(res)

    def get_obj_attr(self, idx: int, attr: str) -> Any:
        res = self._session.get(self._get_url(f'/objects/{idx}/{attr}'))
        _raise_for_status(res)
        return self._deserialize(res)

    def set_obj_attr(self, idx: int, attr: str, val: Any) -> None:
        data = self._serialize(val)
        headers = {'content-type': self._serializer.content_type}
        res = self._session.post(self._get_url(f'/objects/{idx}/{attr}'), data, headers=headers)
        _raise_for_status(res)

    def call_obj_method(self, idx: int, attr: str, args: Tuple[Any, ...], kwargs: Dict[str, Any]):
        data = self._serialize((args, kwargs))
        headers = {'content-type': self._serializer.content_type}
        res = self._session.post(self._get_url(f'/objects/{idx}/{attr}/call'), data, headers=headers)
        _raise_for_status(res)
        return self._deserialize(res)

    def namespace(self, ns: str = 'default') -> 'Namespace':
        return Namespace(self, ns)


T = TypeVar('T')


class Namespace:
    def __init__(self, client: Client, ns: str) -> None:
        self._client: Client = client
        self._ns: str = ns

    def remote_class(self, cls: T, name: str = None) -> T:
        if name is None:
            name = cls.__name__
        ns = self

        class RemoteClass(cls):
            def __init__(self, *args, **kwargs):
                self.__remoteinit__(*args, **kwargs)

            def __remoteinit__(self, *args, **kwargs):
                self._native_rpc_client = ns._client
                self._native_rpc_obj_index = ns._client.create_obj(ns._ns, name, args, kwargs)

        return RemoteClass

    def remote_func(self, name: str, *args, **kwargs) -> Any:
        return self._client.call_func(self._ns, name, args, kwargs)

    def __getattr__(self, name: str) -> Callable:
        def func(*args, **kwargs):
            return self.remote_func(name, *args, **kwargs)

        return func


def remote_method(name: Optional[str] = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__

        def wrapper(*args, **kwargs):
            self, *args = args
            client: Client = self._native_rpc_client
            idx: int = self._native_rpc_obj_index
            return client.call_obj_method(idx, name, args, kwargs)

        return wrapper

    return decorator
