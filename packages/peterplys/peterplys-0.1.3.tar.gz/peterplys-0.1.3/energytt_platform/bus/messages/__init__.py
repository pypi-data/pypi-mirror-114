from energytt_platform.bus.registry import MessageRegistry

from .auth import UserOnboarded
from .measurements import MeasurementAdded
from .meteringpoints import MeteringPointAdded, MeteringPointRemoved


# A registry of all messages understood by the message bus:

registry = MessageRegistry.from_message_types(
    UserOnboarded,
    MeasurementAdded,
    MeteringPointAdded,
    MeteringPointRemoved,
)
