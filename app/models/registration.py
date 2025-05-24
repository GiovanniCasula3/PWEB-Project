from sqlmodel import SQLModel, Field


class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username")
    event_id: int = Field(primary_key=True, foreign_key="event.id")
    

class RegistrationPublic(Registration):
    """
    Modello utilizzato per restituire tutti i dati delle registrazioni nelle risposte API.
    Estende Registration e include i campi necessari per la visualizzazione pubblica.
    """
    pass