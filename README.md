# WildlifeTracker API

This is the Python backend for WildlifeTracker, a system designed to help rangers track herds and families, submit observations, and visualize wildlife activity.

## Features

- GraphQL API built with FastAPI + Strawberry
- PostgreSQL database (via Docker)
- Mutations to register herds, families, observations, and events
- Queries for location-based filtering (nearby events/observations)
- Time-based filtering for all data types

## Tech Stack

- FastAPI
- Strawberry GraphQL
- SQLAlchemy ORM
- PostgreSQL
- Docker & Docker Compose

## Setup

1. **Clone the repo** and navigate to the API directory:
   ```bash
   cd wildlife-tracker-api

2. **Create a .env file:**
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=wildlife
   ```

3. **Start the API and DB using Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Access the API at http://localhost:8000/graphql**

## Project Structure
- app/
    - main.py – FastAPI entrypoint with GraphQL router
    - graphql/ – Resolvers, schema, queries, mutations, types
    - db/ – Models, sessions, and base SQLAlchemy setup
    - services/ – Business logic layer (herd_service, family_service, etc.)
    - utils/ – Helper functions (e.g., haversine)
- Dockerfile, docker-compose.yml – Local container orchestration

## Example GraphQL Operations

```graphql
mutation {
  registerFamily(name: "Pack 3", species: "Wolf", herdId: 1) {
    id
    name
  }
}

query {
  familiesNearby(latitude: 44.6, longitude: -110.5, radiusMiles: 10) {
    name
    observations {
      timestamp
      latitude
      longitude
    }
  }
}
```

## Notes
- DB volume is persistent unless removed via docker-compose down --volumes
- The app is ready for scaling enhancements such as PostGIS, caching, or horizontal sharding