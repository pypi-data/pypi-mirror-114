from datetime import datetime
from dataclasses import dataclass

from energytt_platform.serialize import Serializable


@dataclass
class Measurement(Serializable):
    gsrn: str
    amount: int
    begin: datetime
    end: datetime
