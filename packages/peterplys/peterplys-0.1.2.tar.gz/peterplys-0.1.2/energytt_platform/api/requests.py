# import flask
# import serpyco
# import rapidjson
#
# from abc import abstractmethod
# from typing import List, Optional
# from functools import cached_property
#
# from .context import Context
# from .endpoints import Endpoint
# from .guards import EndpointGuard
# from .responses import HttpError, BadRequest
#
#
# class InputParametersParser(object):
#     @abstractmethod
#     def get_input_data(self) -> Dict[str, Any]:
#         raise NotImplementedError
#
#
# class PostJsonBody(InputParametersParser):
#     pass
#
#
# class QueryString(InputParametersParser):
#     pass
#
#
# class RequestHandler(object):
#     """
#     Abstract base class for http controllers, written specifically for Flask.
#     """
#     def __init__(
#             self,
#             endpoint: Endpoint,
#             guards: List[EndpointGuard] = None,
#     ):
#         self.endpoint = endpoint
#         self.guards = guards or []
#
#     # -- Request and Response (de)serialization ------------------------------
#
#     @cached_property
#     def request_serializer(self) -> Optional[serpyco.Serializer]:
#         """
#         TODO
#         """
#         return self.build_request_serializer() \
#             if self.endpoint.Request is not None \
#             else None
#
#     @cached_property
#     def response_serializer(self) -> Optional[serpyco.Serializer]:
#         """
#         TODO
#         """
#         return self.build_response_serializer() \
#             if self.endpoint.Response is not None \
#             else None
#
#     def build_request_serializer(self) -> serpyco.Serializer:
#         """
#         :rtype: Serializer
#         """
#         encoders = {}
#         # encoders.update(default_encoders)
#         # encoders.update(self.get_encoders())
#         return serpyco.Serializer(self.endpoint.Request, type_encoders=encoders)
#
#     def build_response_serializer(self) -> serpyco.Serializer:
#         """
#         :rtype: Serializer
#         """
#         encoders = {}
#         # encoders.update(default_encoders)
#         # encoders.update(self.get_encoders())
#         return serpyco.Serializer(self.endpoint.Response, type_encoders=encoders)
#
#     # -- HTTP request handling -----------------------------------------------
#
#     def __call__(self) -> flask.Response:
#         """
#         Invoked by Flask to handle a HTTP request.
#         """
#         # return self.invoke_endpoint()
#         try:
#             return self.invoke_endpoint()
#         except HttpError as e:
#             raise
#             return self.handle_http_error(e)
#         except Exception as e:
#             raise
#             return self.handle_exception(e)
#
#     def invoke_endpoint(self) -> flask.Response:
#         """
#         TODO
#         """
#         kwargs = {'context': self.context}
#
#         if self.request_serializer is not None:
#             kwargs['request'] = self.get_request_vm()
#
#         # for guard in self.guards:
#         #     if not self.guard.
#
#         response = self.endpoint.handle_request(**kwargs)
#         # response = self.parse_response(handler_response)
#
#         if self.response_serializer is not None:
#             # if not isinstance(response, self.endpoint.Response):
#             #     raise RuntimeError((
#             #         'Endpoint returned an invalid response. '
#             #         'Expected something of type %s, but endpoint returned '
#             #         'something of type %s'
#             #     ) % (type(self.endpoint.Response), type(response)))
#
#             response_body = self.response_serializer.dump_json(response)
#             response_mimetype = 'application/json'
#         else:
#             response_body = ''
#             response_mimetype = 'text/html'
#
#         return flask.Response(
#             status=200,
#             mimetype=response_mimetype,
#             response=response_body,
#         )
#
#     def handle_http_error(self, e: HttpError) -> flask.Response:
#         """
#         TODO
#         """
#         return flask.Response(
#             response=e.msg,
#             status=e.status_code,
#             mimetype='text/html',
#         )
#
#     def handle_exception(self, e: Exception) -> flask.Response:
#         """
#         TODO
#         """
#         return flask.Response(
#             response='Internal Server Error',
#             status=500,
#             mimetype='text/html',
#         )
#
#     @abstractmethod
#     def get_request_vm(self):
#         """
#         Converts JSON provided in the request body according to the Schema
#         defined on self.Request (if any), and returns the model instance.
#         Returns None if self.Requests is None.
#
#         :rtype: typing.Any
#         """
#         raise NotImplementedError
#
#
# class PostHandler(RequestHandler):
#     """
#     Handles HTTP POST requests.
#     """
#     def get_request_vm(self):
#         """
#         :rtype: typing.Any
#         """
#         # TODO Check Content-Type header
#
#         if not flask.request.data:
#             # No request body provided
#             raise BadRequest('No JSON body provided')
#
#         try:
#             return self.request_serializer.load_json(
#                 flask.request.data.decode('utf8'), True)
#         except rapidjson.JSONDecodeError as e:
#             # Invalid JSON document provided in request body
#             raise BadRequest('Invalid JSON body provided')
#         except serpyco.exception.ValidationError as e:
#             # JSON schema validation failed for request body
#             # TODO Parse ValidationError to something useful
#             raise BadRequest(str(e))
#
#
# class GetHandler(RequestHandler):
#     """
#     Handles HTTP GET requests.
#     """
#     def get_request_vm(self):
#         """
#         :rtype: typing.Any
#         """
#         try:
#             return self.request_serializer.load(dict(flask.request.args), True)
#         except rapidjson.JSONDecodeError as e:
#             # Invalid JSON document provided in query parameters
#             raise BadRequest('Invalid JSON body provided')
#         except serpyco.exception.ValidationError as e:
#             # JSON schema validation failed for query parameters
#             # TODO Parse ValidationError to something useful
#             raise BadRequest(str(e))
