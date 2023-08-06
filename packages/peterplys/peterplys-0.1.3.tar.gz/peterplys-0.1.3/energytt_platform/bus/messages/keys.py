from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.measurements import Measurement


@dataclass
class PublicKeysUpdates(Serializable):
    """
    PublicKey to verify internal tokens has been updated.
    """
    measurement: Measurement
