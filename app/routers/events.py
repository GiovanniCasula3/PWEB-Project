from fastapi import APIRouter, HTTPException, Path, Request
from app.models.event import Event, EventPublic, EventCreate
from app.data.db import SessionDep
from sqlmodel import select
from typing import Annotated

router = APIRouter(prefix="/events")

# GET /events/
@router.get("/", response_model=list[EventPublic])
def get_all_events(session: SessionDep, request: Request):
    statement = select(Event)
    events = session.exec(statement).all()
    return events

# GET /events/{id}
@router.get("/{id}", response_model=EventPublic)
def get_event_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to retrieve.")]
):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# POST /events/
@router.post("/", response_model=EventPublic)
def add_event(session: SessionDep, event_data: EventCreate):
    new_event = Event.model_validate(event_data)
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event

# DELETE /events
@router.delete("/")
def delete_all_events(session: SessionDep):
    events = session.exec(select(Event)).all()
    if not events:
        raise HTTPException(status_code=404, detail="No events found to delete")
    for event in events:
        session.delete(event)
    session.commit()
    return {"detail": "All events successfully deleted"}