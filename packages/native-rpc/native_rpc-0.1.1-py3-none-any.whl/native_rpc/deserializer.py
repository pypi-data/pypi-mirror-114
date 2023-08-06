import json
import pickle
from typing import Any

from aiohttp.streams import StreamReader


class Deserializer:
    def __init__(self):
        pass

    @property
    def content_type(self) -> str:
        return 'application/octet-stream'

    async def deserialize(self, data: StreamReader) -> Any:
        pass


class JsonDeserializer(Deserializer):
    def __init__(self):
        super().__init__()

    @property
    def content_type(self) -> str:
        return 'application/json'

    async def deserialize(self, data: StreamReader) -> Any:
        return json.loads(await data.read())


class PickleDeserializer(Deserializer):
    def __init__(self):
        super().__init__()

    @property
    def content_type(self) -> str:
        return 'application/x-pickle'

    async def deserialize(self, data: StreamReader) -> Any:
        return pickle.loads(await data.read())
