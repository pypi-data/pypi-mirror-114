import flask
import logging
from functools import cached_property
from typing import List, Iterable, Tuple

from .endpoints import Endpoint
from .guards import EndpointGuard
from .orchestration import \
    RequestOrchestrator, JsonBodyProvider, QueryStringProvider


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
            data_provider = QueryStringProvider()
        elif method == 'POST':
            data_provider = JsonBodyProvider()
        else:
            raise RuntimeError('Unsupported HTTP method for endpoints: %s' % method)

        self._flask_app.add_url_rule(
            rule=path,
            endpoint=path,
            methods=[method],
            view_func=RequestOrchestrator(
                endpoint=endpoint,
                data=data_provider,
                guards=guards,
            ),
        )

    def run_debug(self, host: str, port: int):
        """
        TODO
        """
        self._flask_app.logger.setLevel(logging.DEBUG)
        self._flask_app.run(
            host=host,
            port=port,
            debug=True,
        )
