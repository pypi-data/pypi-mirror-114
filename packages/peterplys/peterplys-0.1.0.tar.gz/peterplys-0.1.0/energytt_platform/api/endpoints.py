from typing import Optional
from abc import abstractmethod


class Endpoint(object):
    """
    Abstract base class for http controllers, written specifically for Flask.
    """

    # Request and response schemas
    Request = None
    Response = None

    @abstractmethod
    def handle_request(self, **kwargs) -> Optional[Response]:
        """
        Handle the HTTP request. Overwritten by subclassing.
        """
        raise NotImplementedError

    # async def handle_request_async(self, **kwargs) -> Optional[Response]:
    #     """
    #     Handle the HTTP request. Overwritten by subclassing.
    #     """
    #     return self.handle_request(**kwargs)
