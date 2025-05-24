from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey

class Registration(SQLModel, table=True):
    username: str = Field(
        sa_column=Column(
            "username",
            str,
            ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
        )
    )
    event_id: int = Field(
        sa_column=Column(
            "event_id",
            int,
            ForeignKey("event.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
        )
    )

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