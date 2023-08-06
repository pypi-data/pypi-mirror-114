import flask
import logging
from functools import cached_property
from typing import List, Iterable, Tuple

from .endpoints import Endpoint
from .guards import EndpointGuard
from .requests import GetHandler, PostHandler


class Application(object):
    """
    TODO
    """
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def create(cls, *args, endpoints: Iterable[Tuple[str, str, Endpoint]], **kwargs):
        app = cls(*args, **kwargs)

        for method, path, endpoint in endpoints:
            app.add_endpoint(
                method=method,
                path=path,
                endpoint=endpoint,
            )

        return app

    @cached_property
    def _flask_app(self) -> flask.Flask:
        """
        TODO
        """
        print('ASD')
        return flask.Flask(self.name)

    @property
    def wsgi_app(self) -> flask.Flask:
        """
        TODO
        """
        return self._flask_app

    def add_endpoint(
            self,
            method: str,
            path: str,
            endpoint: Endpoint,
            guards: List[EndpointGuard] = None,
    ):
        """
        TODO
        """
        if method == 'GET':
            handler_cls = GetHandler
        elif method == 'POST':
            handler_cls = PostHandler
        else:
            raise RuntimeError('Unsupported HTTP method for endpoints: %s' % method)

        self._flask_app.add_url_rule(
            rule=path,
            endpoint=path,
            methods=[method],
            view_func=handler_cls(
                endpoint=endpoint,
                guards=guards,
            ),
        )

    def run_debug(self, host: str, port: int):
        """
        TODO
        """
        # app = self._flask_app
        self._flask_app.logger.setLevel(logging.DEBUG)
        self._flask_app.run(
            host=host,
            port=port,
            debug=True,
        )
