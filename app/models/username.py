from pydantic import BaseModel, Field
from typing import Annotated

class Username(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=100)] # username deve avere una lunghezza compresa tra 3 e 100 caratteri