"""
RTX
===
Decorator Module For RTX
~~~~~~~~~~~~~~~~~~~~~~~~
Interactions & UI handler for Pycord
Built for the everyday User & Developer

:copyright: 2021 VincentRPS
:license: Apache-2.0
"""

__title__ = "rtx"
__author__ = "VincentRPS"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2021 VincentRPS"
__version__ = "0.1.0"

import logging
from typing import NamedTuple, Literal


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=1, micro=0, releaselevel="alpha", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
