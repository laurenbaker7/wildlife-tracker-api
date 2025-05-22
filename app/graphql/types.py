import strawberry
from datetime import datetime
from typing import List

@strawberry.type
class ObservationType:
    id: int
    family_id: int
    latitude: float
    longitude: float
    size: int
    health_rating: int
    timestamp: datetime

@strawberry.type
class EventType:
    id: int
    family_id: int
    latitude: float
    longitude: float
    description: str
    timestamp: datetime

@strawberry.type
class FamilyType:
    id: int
    name: str
    herd_id: int
    observations: List[ObservationType]
    events: List[EventType]

@strawberry.type
class HerdType:
    id: int
    species: str
    families: List[FamilyType]