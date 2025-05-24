from fastapi import APIRouter # Serve per definire le rotte API
from sqlmodel import delete, select # Serve per interagire con il database
from data.db import SessionDep # Importa la dipendenza per ottenere una sessione del database

from models.registration import Registration # Importa il modello di registrazione pubblica
from models.registration import RegistrationPublic # Importa il modello di registrazione pubblica



routers = APIRouter(prefix="/registrations", tags=["registrations"])



@routers.get("/")
def get_all_registrations(
    session: SessionDep # Dipendenza per ottenere una sessione del database
) -> list[RegistrationPublic]:
    """
    Recupera tutte le registrazioni dal database.
    
    Args:
        session (SessionDep): Sessione del database.

    Returns:
        list[RegistrationPublic]: Lista di registrazioni pubbliche.
    """
    statement = select(Registration)
    # Esegue la query per selezionare tutte le registrazioni
    results = session.exec(statement).all()
    # Converte i risultati in una lista di modelli pubblici
    return results



@routers.delete("/")
def delete_registration(
    username: str, 
    event_id: int, 
    session: SessionDep):
    """
    Cancella una registrazione esistente dato username ed event_id.
    Args:
        username (str): Username dell'utente.
        event_id (int): ID dell'evento.
        session (SessionDep): Sessione del database.
    Returns:
        dict: Messaggio di conferma o errore.
    """
    statement = delete(Registration).where(
        (Registration.username == username) & (Registration.event_id == event_id)
    )
    result = session.exec(statement)
    session.commit()
    if result.rowcount == 0: # Se non sono state cancellate righe, significa che la registrazione non esiste
        return {"detail": "Registrazione non trovata."}
    return {"detail": "Registrazione cancellata con successo."}