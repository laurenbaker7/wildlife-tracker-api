from app.db.models.family import Family
from app.db.models.herd import Herd
from app.db.session import SessionLocal
from app.db.models.observation import Observation
from app.db.models.event import Event
from math import radians, cos, sin, acos
from datetime import datetime
from typing import Optional
from sqlalchemy import func

def get_all_families():
    db = SessionLocal()
    return db.query(Family).all()

def create_family(name, herd_id, species):
    db = SessionLocal()

    # Check that herd exists
    herd = db.query(Herd).filter(Herd.id == herd_id).first()
    if not herd:
        raise ValueError(f"Herd with id {herd_id} does not exist.")

    # Check that species matches herd species
    if herd.species != species:
        raise ValueError(f"Herd with id {herd_id} is not of species {species}.")

    # Check that family with same name doesn't already exist in the same herd
    existing_family = db.query(Family).filter(Family.name == name, Family.herd_id == herd_id).first()
    if existing_family:
        raise ValueError(f"Family with name {name} already exists in herd {herd_id}.")

    new_family = Family(name=name, herd_id=herd_id)
    db.add(new_family)
    db.commit()
    db.refresh(new_family)
    return new_family

# Getting a family with observations and events
def get_family(family_id: int, start_time=None, end_time=None):
    db = SessionLocal()

    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        return None

    obs_query = db.query(Observation).filter(Observation.family_id == family.id)
    evt_query = db.query(Event).filter(Event.family_id == family.id)

    if start_time:
        obs_query = obs_query.filter(Observation.timestamp >= start_time)
        evt_query = evt_query.filter(Event.timestamp >= start_time)
    if end_time:
        obs_query = obs_query.filter(Observation.timestamp <= end_time)
        evt_query = evt_query.filter(Event.timestamp <= end_time)

    family.observations = obs_query.all()
    family.events = evt_query.all()

    return family

# Getting all families within a radius of a location with observations and events
def get_families_near_location(latitude: float, longitude: float, radius_miles: float, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    db = SessionLocal()

    # Haversine distance calculation (in SQL, in miles)
    def haversine_filter(query, model):
        return query.filter(
            3959 * func.acos(
                func.cos(func.radians(latitude)) * func.cos(func.radians(model.latitude)) *
                func.cos(func.radians(model.longitude) - func.radians(longitude)) +
                func.sin(func.radians(latitude)) * func.sin(func.radians(model.latitude))
            ) <= radius_miles
    )

    # Observations within radius/time
    obs_query = db.query(Observation)
    if start_time:
        obs_query = obs_query.filter(Observation.timestamp >= start_time)
    if end_time:
        obs_query = obs_query.filter(Observation.timestamp <= end_time)
    obs_query = haversine_filter(obs_query, Observation)

    # Events within radius/time
    evt_query = db.query(Event)
    if start_time:
        evt_query = evt_query.filter(Event.timestamp >= start_time)
    if end_time:
        evt_query = evt_query.filter(Event.timestamp <= end_time)
    evt_query = haversine_filter(evt_query, Event)

    # Get unique family_ids from both
    obs_family_ids = {obs.family_id for obs in obs_query.all()}
    evt_family_ids = {evt.family_id for evt in evt_query.all()}
    all_family_ids = obs_family_ids.union(evt_family_ids)

    # Fetch families and attach matching obs/events
    families = db.query(Family).filter(Family.id.in_(all_family_ids)).all()
    for family in families:
        family.observations = [obs for obs in obs_query if obs.family_id == family.id]
        family.events = [evt for evt in evt_query if evt.family_id == family.id]

    return families