from typing import List
from datetime import datetime
from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.meteringpoints import MeteringPoint
from energytt_platform.models.certificates import GranularCertificate


# -- Action requests ---------------------------------------------------------


@dataclass
class IssueCertificate(Serializable):
    """
    A request to issue a new Granular Certificate.
    """
    begin: datetime
    end: datetime
    sector: str
    amount: int
    technology_code: str
    fuel_code: str


# -- Action recipes ----------------------------------------------------------


@dataclass
class CertificateIssued(Serializable):
    """
    A new Granular Certificate has been issued.
    """
    certificate: GranularCertificate


@dataclass
class CertificateTransferred(Serializable):
    """
    A Granular Certificate has been transferred to a new owner.
    """
    certificate: GranularCertificate
    child: GranularCertificate


@dataclass
class CertificateSplit(Serializable):
    """
    A Granular Certificate has been split into multiple new certificates.
    """
    certificate: GranularCertificate
    children: List[GranularCertificate]


@dataclass
class CertificateRetired(Serializable):
    """
    A Granular Certificate has been retired onto a Metering Point.
    """
    certificate: GranularCertificate
    meteringpoint: MeteringPoint
