from dataclasses import dataclass

from energytt_platform.serialize import Serializable


@dataclass
class PublicKeyUpdated(Serializable):
    """
    The public key to decrypt internal tokens has been updated.
    """
    key: str
