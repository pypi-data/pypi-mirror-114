from dataclasses import dataclass

from energytt_platform.serialize import Serializable


@dataclass
class Service(Serializable):
    """
    A microservice running in the ETT platform.
    """
    name: str
