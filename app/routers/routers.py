from fastapi import APIRouter, HTTPException, Path, Form, Request
from sqlmodel import select, delete
from app.data.db import SessionDep
from typing import Annotated
from app.models.event import Event, EventCreate

router = APIRouter(prefix='/events')

@router.put('/{id}')
def update_event(
    session: SessionDep,
    id: Annotated[int, Path(description='The Id of the event to update')],
    newevent: EventCreate
):
    """ Update a book by the given id"""
    event = session.get(event, id)
    if event is None:
        raise HTTPException(status_code=404, detail='Book non found')
    event.title = newevent.title
    event.description = newevent.desctription
    event.date = newevent.date
    event.location = newevent.location
    session.add(event)
    session.commit()
    return 'Book successfully updated.'

@router.delete('/{id}')
def delete_book(
    session: SessionDep,
    id: Annotated[int, Path(description='The id odf the book to delete')]
):
    """ Deleete the book by the give id"""
    event = session.get(Event, id)
    if event is None:
        raise 