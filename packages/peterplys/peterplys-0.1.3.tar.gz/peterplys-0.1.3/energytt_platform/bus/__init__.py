from typing import List

from .broker import MessageBroker
from .kafka import KafkaMessageBroker
from .serialize import MessageSerializer
from .dispatcher import MessageDispatcher


def get_default_broker(servers: List[str]) -> MessageBroker:
    """
    Creates and returns an instance of the default message broker.

    :param List[str] servers:
    :rtype: MessageBroker
    :return: An instance of the default message broker
    """
    return KafkaMessageBroker(
        servers=servers,
        serializer=MessageSerializer(),
    )
