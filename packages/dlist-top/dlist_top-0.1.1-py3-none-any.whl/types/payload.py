from dlist_top.types.base import Base
from types import SimpleNamespace
from typing import Any
from enum import Enum
from .base import Base

class GatewayOP(Enum):
    HELLO = 1
    IDENTIFY = 2
    READY = 3
    DISCONNECT = 4
    EVENT = 5

class GatewayPayload(Base):
    op: GatewayOP
    data: Any
    event: str