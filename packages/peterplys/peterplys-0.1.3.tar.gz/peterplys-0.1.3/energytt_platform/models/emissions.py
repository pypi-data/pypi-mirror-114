from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

from energytt_platform.serialize import Serializable

from .common import Address, Technology
from .meteringpoints import MeteringPointType


@dataclass
class MeteringPointMetaData(Serializable):
    """
    MeteringPoint meta data.

    TODO Add physical address
    """
    gsrn: str
    address: Optional[Address]
    type: Optional[MeteringPointType]
    technology: Optional[Technology]


@dataclass
class ResidualMixDataPart(Serializable):
    technology: str
    percent: float
    sector: str  # Sector where energy is produced


@dataclass
class ResidualMixData(Serializable):
    sector: str  # Sector where energy is consumed
    begin: datetime
    end: datetime
    emissions: Dict[str, float]  # g/Wh

    # Technologies unique on: (technology, sector) (composite key)
    technologies: List[ResidualMixDataPart]
