from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.db.base import Base
from app.db.session import engine
from app.db.models.herd import Herd
from app.db.models.family import Family
from app.db.models.observation import Observation
from app.db.models.event import Event
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware BEFORE you mount GraphQL router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)