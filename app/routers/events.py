from fastapi import APIRouter, HTTPException, Path, Form, Request
from sqlmodel import select, delete
from app.data.db import SessionDep
from typing import Annotated
from app.models.event import Event, EventCreate, EventPublic
from app.models.user import User, UserCreate
from app.models.registration import Registration

router = APIRouter(prefix="/events", tags=["Events"])

# GET /events/
@router.get("/", response_model=list[EventPublic])
def get_all_events(session: SessionDep, request: Request):
    """
    Restituisce la lista degli eventi esistenti.
    """
    statement = select(Event)
    events = session.exec(statement).all()
    return events

# GET /events/{id}
@router.get("/{id}", response_model=EventPublic)
def get_event_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="ID dell'evento")]
):
    """
    Restituisci l"evento con l"id dato.
    """
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    return event

# POST /events/
@router.post("/", response_model=EventPublic)
def add_event(session: SessionDep, event_data: EventCreate):
    """
    Crea un nuovo evento.
    """
    new_event = Event.model_validate(event_data)
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event

@router.post("/{id}/register")
def register_event_for_user(
    request: Request,
    id: Annotated[int, Path(description="ID dell'evento")],
    user: Annotated[str, Path(description="L'username dell'utente")],
    session: SessionDep
):
    """
    Registra un utente per l"evento dato.
    """
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    user = session.get(User, user.username)
    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    registration_check = session.exec(select(Registration).where((Registration.username == user.username) & (Registration.event_id == event.id))).first()
    if registration_check:
        raise HTTPException(status_code=409, detail="L'utente è già registrato per l'evento")
    registration = Registration(username=user.username, event_id=event.id)
    session.add(registration)
    session.commit()
    return "Utente registrato"

# DELETE /events
@router.delete("/")
def delete_all_events(session: SessionDep):
    """
    Elimina tutti gli eventi.
    """
    events = session.exec(select(Event)).all()
    if not events:
        raise HTTPException(status_code=404, detail="Nessun evento da eliminare")
    for event in events:
        session.delete(event)
    session.commit()
    return {"detail": "Tutti gli eventi sono stati eliminati"}

@router.delete("/{id}")
def delete_event(
    session: SessionDep,
    id: Annotated[int, Path(description="ID dell'evento")]
):
    """
    Elimina un evento esistente.
    """
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    session.delete(event)
    session.commit()
    return "Evento eliminato"

# PUT
@router.put("/{id}")
def update_event(
    session: SessionDep,
    id: Annotated[int, Path(description="ID dell'evento")],
    newevent: EventCreate
):
    """
    Aggiorna un evento esistente.
    """
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    event.title = newevent.title
    event.description= newevent.description
    event.date = newevent.date
    event.location = newevent.location
    session.add(event)
    session.commit()
    return "Evento aggiornato con successo"