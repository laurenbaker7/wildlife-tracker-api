from app.db.session import SessionLocal
from app.db.models.event import Event
from app.db.models.family import Family
from app.utils.geo_helpers import haversine_miles

def add_event(family_id, latitude, longitude, description):
    # Check that lat & long are valid coordinates
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180.")

    db = SessionLocal()

    # Check that family exists
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise ValueError(f"Family with id {family_id} does not exist.")

    event = Event(
        family_id=family_id,
        latitude=latitude,
        longitude=longitude,
        description=description
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_events_near_location(lat, lon, radius_miles, start_time=None, end_time=None):
    db = SessionLocal()
    query = db.query(Event)

    if start_time:
        query = query.filter(Event.timestamp >= start_time)
    if end_time:
        query = query.filter(Event.timestamp <= end_time)

    all_events = query.all()
    
    nearby = [
        event for event in all_events
        if haversine_miles(lat, lon, event.latitude, event.longitude) <= radius_miles
    ]
    
    return nearby
