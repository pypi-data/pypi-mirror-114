from enum import Enum
from typing import Optional
from dataclasses import dataclass

from energytt_platform.serialize import Serializable

from .common import Address, Technology


class MeteringPointType(Enum):
    PRODUCTION = 'PRODUCTION'  # E18
    CONSUMPTION = 'CONSUMPTION'  # E17


@dataclass
class MeteringPoint(Serializable):
    """
    A single Metering Point.

    TODO Add physical address
    """
    gsrn: str
    type: MeteringPointType
    sector: str
    type: Optional[MeteringPointType]
    technology: Optional[Technology]
    address: Optional[Address]
    # technology_code: Optional[str]
    # fuel_code: Optional[str]


@dataclass
class MeteringPointMetaData(Serializable):
    """
    MeteringPoint meta data.

    TODO Add physical address
    """
    gsrn: str
    type: Optional[MeteringPointType]
    technology: Optional[Technology]
    address: Optional[Address]
