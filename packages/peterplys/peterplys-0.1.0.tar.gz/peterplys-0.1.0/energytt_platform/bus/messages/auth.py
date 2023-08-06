from dataclasses import dataclass

from energytt_platform.serialize import Serializable


@dataclass
class UserOnboarded(Serializable):
    """
    A new user has been onboarded to the system.
    """
    subject: str
    name: str
