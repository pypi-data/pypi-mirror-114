import json
from typing import Dict

from aiohttp import web


class RequestException(Exception):
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> Dict:
        return {
            'type': type(self).__name__,
            **self.__dict__
        }


class NamespaceNotFoundException(web.HTTPNotFound, RequestException):
    def __init__(self, name: str):
        self.name = name
        web.HTTPNotFound.__init__(self, text=self.to_json())


class FuncNotFoundException(web.HTTPNotFound, RequestException):
    def __init__(self, name: str):
        self.name = name
        web.HTTPNotFound.__init__(self, text=self.to_json())


class ClassNotFoundException(web.HTTPNotFound, RequestException):
    def __init__(self, name: str):
        self.name = name
        web.HTTPNotFound.__init__(self, text=self.to_json())


class ObjectNotFoundException(web.HTTPNotFound, RequestException):
    def __init__(self, id: int):
        self.id = id
        web.HTTPNotFound.__init__(self, text=self.to_json())


class InvalidParamException(web.HTTPBadRequest, RequestException):
    def __init__(self, param: str):
        self.param = param
        web.HTTPBadRequest.__init__(self, text=self.to_json())


class AttrNotFoundException(web.HTTPNotFound, RequestException):
    def __init__(self, obj_idx: int, attr: str):
        self.attr = attr
        self.obj_idx = obj_idx
        web.HTTPNotFound.__init__(self, text=self.to_json())


class SerializationException(web.HTTPBadRequest, RequestException):
    def __init__(self, msg: str):
        self.msg = msg
        web.HTTPBadRequest.__init__(self, text=self.to_json())


class DeserializationException(web.HTTPBadRequest, RequestException):
    def __init__(self, msg: str):
        self.msg = msg
        web.HTTPBadRequest.__init__(self, text=self.to_json())


class InternalProcedureException(web.HTTPInternalServerError, RequestException):
    def __init__(self, msg):
        self.msg = msg
        web.HTTPBadRequest.__init__(self, text=self.to_json())


exceptions = [NamespaceNotFoundException, FuncNotFoundException, ClassNotFoundException, ObjectNotFoundException,
              InvalidParamException, AttrNotFoundException, SerializationException, DeserializationException,
              InternalProcedureException]

exceptions_map = dict([(ex.__name__, ex) for ex in exceptions])
