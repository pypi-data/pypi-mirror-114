from typing import Dict, Type

from .broker import TMessage, TMessageHandler


class MessageDispatcher(Dict[Type[TMessage], TMessageHandler]):
    """
    A message handler that dispatches incoming messages to the appropriate
    handler. Each message type can have a single handler associated.
    """
    def __call__(self, msg: TMessage):
        message_type = type(msg)
        if message_type in self:
            handler = self[message_type]
            handler(msg)
