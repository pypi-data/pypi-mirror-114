from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.meteringpoints import MeteringPoint


@dataclass
class MeteringPointAdded(Serializable):
    """
    A new MeteringPoint has been added to the system.
    """
    subject: str
    meteringpoint: MeteringPoint


@dataclass
class MeteringPointRemoved(Serializable):
    """
    A MeteringPoint has been remove from the system.
    """
    subject: str
    gsrn: str
