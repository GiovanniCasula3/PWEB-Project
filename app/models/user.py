from sqlmodel import SQLModel, Field

class BaseUser(SQLModel):
    """
    Modelo base per gli utenti, definisce i campi comuni per tutti i modelli di utente.
    """
    name: str
    email: str
    
    
    
class User(BaseUser, table=True):
    """
    Modello di utente che estende BaseUser e rappresenta una tabella nel database.
    """
    username: str = Field(primary_key=True) 
    
    
class UserPublic(BaseUser):
    """
    Modello utilizzato per restituire tutti i dati degli utenti nelle risposte API.
    """
    username: str 

class UserCreate(BaseUser):
    """
    Modello per la creazione di un nuovo utente, estende BaseUser senza ID.
    """
    pass  # Non ha bisogno di ulteriori campi, poiché eredita tutto da BaseUser

