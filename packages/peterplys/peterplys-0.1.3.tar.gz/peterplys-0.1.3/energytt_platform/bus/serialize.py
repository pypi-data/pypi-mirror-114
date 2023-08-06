from energytt_platform.serialize import JsonSerializer, Serializable

from .messages import registry


class MessageSerializer(object):
    """
    A serializer specifically for serializing messages to
    and from the event bus.
    """

    KEY_VALUE_SEPARATOR = b','

    def __init__(self):
        self.serializer = JsonSerializer()

    def serialize(self, msg: Serializable) -> bytes:
        if msg.object_name not in registry:
            raise RuntimeError((
                'Can not send message of type "%s": '
                'Type is not known by the bus.'
            ) % msg.object_name)

        return b'%b%b%b' % (
            msg.object_name.encode(),
            self.KEY_VALUE_SEPARATOR,
            self.serializer.serialize(msg),
        )

    def deserialize(self, data: bytes) -> Serializable:
        separator_index = data.find(self.KEY_VALUE_SEPARATOR)
        object_name = data[:separator_index].decode('utf8')
        object_class = registry[object_name]
        object_data = data[separator_index+1:]

        return self.serializer.deserialize(object_data, object_class)
