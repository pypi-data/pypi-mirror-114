from datetime import datetime

from energytt_platform.bus.messages import NewMeasurement
from energytt_platform.bus.serialize import MessageSerializer
from energytt_platform.models.measurements import Measurement


class TestMessageSerializer:

    def test__should_serialize_and_deserialize_correctly(self):

        # -- Arrange ---------------------------------------------------------

        obj = NewMeasurement(
            measurement=Measurement(
                gsrn='12345',
                amount=123,
                begin=datetime.now(),
                end=datetime.now(),
            )
        )

        uut = MessageSerializer()

        # -- Act -------------------------------------------------------------

        serialized = uut.serialize(obj)
        deserialized = uut.deserialize(serialized)

        # -- Assert ----------------------------------------------------------

        assert isinstance(deserialized, NewMeasurement)
        assert deserialized == obj
