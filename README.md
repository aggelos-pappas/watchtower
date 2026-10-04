# Watchtower

Watchtower is a modular backend for personal monitoring and calendar organization.

## Features
- monitor websites and sources
- extract structured events from HTML
- reconcile and persist changes
- export iCalendar data
- FastAPI + Typer backend foundation

## Local installation
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head

## Running the API
uvicorn watchtower.interfaces.api.app:app --reload

## Running the worker
watchtower worker

## CLI
watchtower health
watchtower watch add https://example.com --name "Example" --source-type http --extraction-type html
watchtower watch list
watchtower event export-ics output.ics
