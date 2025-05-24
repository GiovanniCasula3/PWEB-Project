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