from dlist_top.types.timestamp import Timestamp
from types import SimpleNamespace
from typing import Any
from .entity import EntityType
from .timestamp import Timestamp
from .base import Base

class VoteData(Base):
    authorID: str
    entityType: EntityType
    entityID: str
    date: Timestamp
    totalVotes: int
    userVotes: int

class RateData(Base):
    authorID: str
    entityType: EntityType
    entityID: str
    rating: int
    details: str
    date: Timestamp

event_classes = {
    'VOTE': VoteData,
    'RATE': RateData
}