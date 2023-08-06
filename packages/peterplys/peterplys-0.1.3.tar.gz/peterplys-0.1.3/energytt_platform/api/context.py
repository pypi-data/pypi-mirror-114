from re import compile
from abc import abstractmethod
from typing import Dict, Optional
from functools import cached_property


class Context(object):
    """
    Context for a single incoming HTTP request.
    """

    TOKEN_HEADER = 'Authorization'
    TOKEN_PATTERN = compile(r'^Bearer:\s*(.+)$')

    @property
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        """
        Returns request headers.
        """
        raise NotImplementedError

    @cached_property
    def token(self) -> Optional[str]:
        """
        Returns request Bearer token.
        """
        if self.TOKEN_HEADER in self.headers:
            matches = self.TOKEN_PATTERN.findall(self.headers[self.TOKEN_HEADER])
            if matches:
                return matches[0]
