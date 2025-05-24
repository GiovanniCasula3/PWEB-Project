from sqlmodel import SQLModel, Field

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username", ondelete="CASCADE")
    event_id: int = Field(primary_key=True, foreign_key="event.id", ondelete="CASCADE")

class RegistrationPublic(Registration):
    """
    Modello utilizzato per restituire tutti i dati delle registrazioni nelle risposte API.
    Estende Registration e include i campi necessari per la visualizzazione pubblica.
    """
    pass

class RegistrationCreate(Registration):
    """
    Modello per la creazione di una nuova registrazione, estende Registration senza ID.
    """
    pass  # Non ha bisogno di ulteriori campi, poiché eredita tutto da Registration