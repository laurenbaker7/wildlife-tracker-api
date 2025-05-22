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