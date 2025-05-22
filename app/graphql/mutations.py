import strawberry
from app.graphql.types import FamilyType, HerdType, ObservationType, EventType
from app.services.family_service import create_family
from app.services.herd_service import create_herd
from app.services.observation_service import add_observation
from app.services.event_service import add_event
from strawberry.exceptions import GraphQLError

@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_family(self, name: str, herd_id: int, species: str) -> FamilyType:
        try:
            return create_family(name, herd_id, species)
        except ValueError as e:
            raise GraphQLError(str(e))

    @strawberry.mutation
    def register_herd(self, species: str) -> HerdType:
        return create_herd(species)

    @strawberry.mutation
    def record_observation(
        self,
        family_id: int,
        latitude: float,
        longitude: float,
        size: int,
        health_rating: int
    ) -> ObservationType:
        try:
            return add_observation(family_id, latitude, longitude, size, health_rating)
        except ValueError as e:
            raise GraphQLError(str(e))

    @strawberry.mutation
    def record_event(
        self,
        family_id: int,
        latitude: float,
        longitude: float,
        description: str
    ) -> EventType:
        try:
            return add_event(family_id, latitude, longitude, description)
        except ValueError as e:
            raise GraphQLError(str(e))