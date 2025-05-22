from app.db.session import SessionLocal
from app.db.models.observation import Observation
from app.db.models.family import Family
from app.utils.geo_helpers import haversine_miles
from datetime import datetime

def add_observation(family_id, latitude, longitude, size, health_rating):
    # Check that lat & long are valid coordinates
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180.")
    # Check that health rating is between 1 and 10
    if not (1 <= health_rating <= 10):
        raise ValueError("Health rating must be an integer between 1 and 10.")

    db = SessionLocal()

    # Check that family exists
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise ValueError(f"Family with id {family_id} does not exist.")

    observation = Observation(
        family_id=family_id,
        latitude=latitude,
        longitude=longitude,
        size=size,
        health_rating=health_rating
    )
    db.add(observation)
    db.commit()
    db.refresh(observation)
    return observation

def get_observations_near_location(lat, lon, radius_miles, start_time=None, end_time=None):
    db = SessionLocal()
    query = db.query(Observation)

    if start_time:
        query = query.filter(Observation.timestamp >= start_time)
    if end_time:
        query = query.filter(Observation.timestamp <= end_time)

    all_observations = query.all()

    nearby = [
        obs for obs in all_observations
        if haversine_miles(lat, lon, obs.latitude, obs.longitude) <= radius_miles
    ]
    return nearby