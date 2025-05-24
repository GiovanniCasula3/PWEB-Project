from sqlmodel import SQLModel, Field #Importa le classi necessarie da SQLModel
from typing import Annotated #Consente di usare annotazioni per i tipi
from datetime import datetime #Importa la classe datetime per gestire le date e le ore

class EventBase(SQLModel):
    """
    Classe base che definisce i campi comuni per tutti i modelli di evento.
    """
    title: str
    description: str
    date: datetime
    location: str

class Event(EventBase, table=True):
    """
    Modello di evento che estende EventBase e rappresenta una tabella nel database.
    """
    id: int = Field(default=None, primary_key=True) # Campo ID che funge da chiave primaria, con valore predefinito None e marcato come chiave primaria

class EventCreate(EventBase): # Modello per la creazione di un nuovo evento
    """
    Modello per la creazione di un nuovo evento, estende EventBase senza ID.
    """
    pass  # Non ha bisogno di ulteriori campi, poiché eredita tutto da EventBase

class EventPublic(EventBase): # Modello per la visualizzazione pubblica degli eventi  (ovvero per le risposte API)
    """
    Modello utilizzato per restituire tutti i dati degli eventi nelle risposte API.
    Estende EventBase e include l'ID dell'evento.
    """
    id :int