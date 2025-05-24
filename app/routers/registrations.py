from fastapi import APIRouter
from sqlmodel import delete, select
from app.data.db import SessionDep
from app.models.registration import Registration
from app.models.registration import RegistrationPublic

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.get("/")
def get_all_registrations(
    session: SessionDep # Dipendenza per ottenere una sessione del database
) -> list[RegistrationPublic]:
    """
    Recupera tutte le registrazioni dal database.
    """
    statement = select(Registration)
    # Esegue la query per selezionare tutte le registrazioni
    results = session.exec(statement).all()
    # Converte i risultati in una lista di modelli pubblici
    return results

@router.delete("/")
def delete_registration(
    username: str,
    event_id: int,
    session: SessionDep):
    """
    Cancella una registrazione esistente dato username ed event_id.
    """
    statement = delete(Registration).where(
        (Registration.username == username) & (Registration.event_id == event_id)
    )
    result = session.exec(statement)
    session.commit()
    if result.rowcount == 0: # Se non sono state cancellate righe, significa che la registrazione non esiste
        return {"Registrazione non trovata."}
    return {"Registrazione cancellata con successo."}