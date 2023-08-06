from energytt_platform.models.infrastructure import Service


class EndpointGuard(object):
    def allow_access(self):
        pass


class ServiceGuard(EndpointGuard):
    """
    Allows only specific services to access this endpoint.
    """
    def __init__(self, *services: Service):
        self.services = services


s = ServiceGuard(
    Service(name='Service A'),
    Service(name='Service B'),
)
