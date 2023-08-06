import serpyco
from typing import Type
from abc import abstractmethod
from functools import lru_cache
from dataclasses import dataclass


@dataclass
class Serializable:
    """
    Base class for dataclasses that can be serialized and deserialized.
    Subclasses must be defined as dataclasses.
    """
    @property
    def object_name(self) -> str:
        return self.__class__.__name__


class SerializeError(Exception):
    pass


class DeserializeError(Exception):
    pass


class Serializer(object):
    """
    An interface for serializing and deserializing dataclasses.
    """

    @abstractmethod
    def serialize(self, obj: Serializable) -> bytes:
        """
        Serialize an object to bytes.

        :param Serializable obj: Object to serialize
        :raise SerializeError: Raised when serialization fails
        :rtype: bytes
        :return: Byte-representation of object
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, data: bytes, cls: Type[Serializable]) -> Serializable:
        """
        Deserialize bytes to an object.

        :param bytes data: Byte-representation of object
        :param Type[Serializable] cls: Class to deserialize into
        :raise DeserializeError: Raised when deserialization fails
        :rtype: Serializable
        :return: Deserialized object
        """
        raise NotImplementedError


class JsonSerializer(Serializer):
    """
    Serialize and deserialize to and from JSON.
    """
    def serialize(self, msg: Serializable) -> bytes:
        return self.get_serializer(msg.__class__) \
            .dump_json(msg) \
            .encode()

    def deserialize(self, data: bytes, cls: Type[Serializable]) -> Serializable:
        return self.get_serializer(cls) \
            .load_json(data.decode('utf8'))

    # -- Serializers ---------------------------------------------------------

    @lru_cache
    def get_serializer(self, cls: Type[Serializable]) -> serpyco.Serializer:
        return self.build_serializer(cls)

    def build_serializer(self, cls: Type[Serializable]) -> serpyco.Serializer:
        return serpyco.Serializer(cls)
