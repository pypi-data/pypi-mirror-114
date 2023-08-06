from enum import Enum
from typing import Optional
from dataclasses import dataclass

from energytt_platform.serialize import Serializable


class Resolution(Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


@dataclass
class Address(Serializable):
    """
    TODO Which international standard does this convey to?
    """
    street_code: Optional[str]
    street_name: Optional[str]
    building_number: Optional[str]
    floor_id: Optional[str]
    room_id: Optional[str]
    post_code: Optional[str]
    city_name: Optional[str]
    city_sub_division_name: Optional[str]
    municipality_code: Optional[str]
    location_description: Optional[str]


@dataclass
class Technology(Serializable):
    """
    TODO Which international standard does this convey to?
    """
    technology_code: str
    fuel_code: str
    label: Optional[str]
