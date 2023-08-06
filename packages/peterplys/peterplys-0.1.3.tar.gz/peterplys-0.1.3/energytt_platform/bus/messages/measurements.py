from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.measurements import Measurement


@dataclass
class MeasurementAdded(Serializable):
    """
    A new Measurement has been added to the system.
    """
    subject: str
    measurement: Measurement
