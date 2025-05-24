from fastapi import APIRouter, HTTPException, Path, Form, Request
from sqlmodel import select, delete
from app.data.db import SessionDep
from typing import Annotated
from app.models.event import Event, EventCreate
from app.models.user import User, UserCreate
from app.models.registration import Registration

router = APIRouter(prefix='/events')

@router.put('/{id}')
def update_event(
    session: SessionDep,
    id: Annotated[int, Path(description='The Id of the event to update')],
    newevent: EventCreate
):
    """ Update a event by the given id"""
    event = session.get(event, id)
    if event is None:
        raise HTTPException(status_code=404, detail='Event non found')
    event.title = newevent.title
    event.description = newevent.desctription
    event.date = newevent.date
    event.location = newevent.location
    session.add(event)
    session.commit()
    return 'Event successfully updated.'

@router.delete('/{id}')
def delete_book(
    session: SessionDep,
    id: Annotated[int, Path(description='The id of the event to delete')]
):
    """ Deleete the event by the give id"""
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail='Event not found')
    session.delete(event)
    session.commit()
    return 'Event successfully deleted'

@router.post('/{id}/register')
def register(
    request: Request,
    id: Annotated[int, Path(description='Thr id of the event')],
    user: Annotated[str, Path(description='The username of the user')],
    session: SessionDep
):
    """ Register for a event"""
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail='Event not found')
    user = session.get(User, user.username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    registration_check = session.exec(select(Registration).where((Registration.username == event.username) & (Registration.event_id == id))).first()
    if registration_check:
        raise HTTPException(status_code=409, detail='User already registred to the event')
    registration = Registration(username=user.username, event_id=id)
    session.add(registration)
    session.commit()
    return 'User successfully register'

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
