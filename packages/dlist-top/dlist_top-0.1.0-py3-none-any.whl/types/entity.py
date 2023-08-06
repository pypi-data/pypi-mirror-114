from enum import Enum
from .base import Base

class EntityType(Enum):
    BOT = 'bots'
    SERVER = 'servers'

class Entity(Base):
    type: EntityType
    id: str
    name: str