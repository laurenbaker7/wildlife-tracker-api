import strawberry
from typing import List, Optional
from app.graphql.types import FamilyType, HerdType, EventType, ObservationType
from app.services.family_service import get_all_families, get_family
from app.services.herd_service import get_all_herds, get_herd
from app.services.event_service import get_events_near_location
from app.services.observation_service import get_observations_near_location
from datetime import datetime
from app.services.family_service import get_families_near_location

@strawberry.type
class Query:
    @strawberry.field
    def families(self) -> List[FamilyType]:
        return get_all_families()

    @strawberry.field
    def herds(self) -> List[HerdType]:
        return get_all_herds()

    @strawberry.field
    def herd(
        self, 
        id: int, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> Optional[HerdType]:
        return get_herd(id, start_time, end_time)

    @strawberry.field
    def family(
        self, 
        id: int, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> Optional[FamilyType]:
        return get_family(id, start_time, end_time)

    @strawberry.field
    def events_nearby(
        self, 
        latitude: float, 
        longitude: float, 
        radius_miles: float, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> List[EventType]:
        return get_events_near_location(latitude, longitude, radius_miles, start_time, end_time)

    @strawberry.field
    def observations_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_miles: float,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[ObservationType]:
        return get_observations_near_location(latitude, longitude, radius_miles, start_time, end_time)

    @strawberry.field
    def families_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_miles: float,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[FamilyType]:
        return get_families_near_location(latitude, longitude, radius_miles, start_time, end_time)

