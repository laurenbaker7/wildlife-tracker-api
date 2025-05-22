from app.db.models.herd import Herd
from app.db.session import SessionLocal
from sqlalchemy.orm import joinedload
from app.db.models.observation import Observation
from app.db.models.event import Event

def get_all_herds():
    db = SessionLocal()
    return db.query(Herd).all()

# Creating a new herd for registerHerd API
def create_herd(species: str):
    db = SessionLocal()
    new_herd = Herd(species=species)
    db.add(new_herd)
    db.commit()
    db.refresh(new_herd)
    return new_herd

# Getting families in a herd with observations and events
def get_herd(herd_id: int, start_time=None, end_time=None):
    db = SessionLocal()

    herd = db.query(Herd).options(
        joinedload(Herd.families)
    ).filter(Herd.id == herd_id).first()

    if not herd:
        return None

    for family in herd.families:
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

    return herd