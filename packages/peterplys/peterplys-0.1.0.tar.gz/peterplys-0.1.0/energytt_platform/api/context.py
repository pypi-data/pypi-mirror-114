from abc import abstractmethod
from typing import Dict, Optional


class HttpContext(object):
    """
    Context for a single incoming HTTP request.
    """

    @property
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        """
        Returns request headers.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def token(self) -> Optional[str]:
        """
        Returns request Bearer token.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def subject(self) -> Optional[str]:
        """
        Returns request headers.
        """
        raise NotImplementedError
