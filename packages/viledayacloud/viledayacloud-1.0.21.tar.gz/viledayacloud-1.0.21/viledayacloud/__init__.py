# coding=utf-8
"""
viledayacloud
"""

__version__ = "1.0.21"

from typing import Tuple

from .common import getsecret as getsecret, tgmjsoncall as tgmjsoncall, WorkItem as WorkItem

__all__: Tuple[str, ...] = (
        "getsecret",
        "tgmjsoncall",
        "WorkItem"
        )
