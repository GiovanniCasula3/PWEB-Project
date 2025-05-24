from fastapi import APIRouter # Serve per definire le rotte API
from sqlmodel import delete, select # Serve per interagire con il database
from data.db import SessionDep # Importa la dipendenza per ottenere una sessione del database

from models.registration import Registration # Importa il modello di registrazione pubblica
from models.registration import RegistrationPublic # Importa il modello di registrazione pubblica


routers = APIRouter(prefix="/registrations", tags=["registrations"])



@routers.get("/")
def get_registrations(
    session: SessionDep # Dipendenza per ottenere una sessione del database
) -> list[]

