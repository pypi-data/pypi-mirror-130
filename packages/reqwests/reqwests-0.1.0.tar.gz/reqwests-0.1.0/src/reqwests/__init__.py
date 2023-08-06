"""
reqwests
~~~~~~~~
Pythonic API Wrapper For Discord And Anime Enjoyers

:copyright: 2021-present RPS
:license: MIT
"""

__title__ = "reqwests"
__author__ = "RPS"
__license__ = "MIT"
__copyright__ = "Copyright 2021 RPS"
__version__ = "0.1.0"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from .internal.v1.core import *

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=0, micro=1, releaselevel="candidate", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
