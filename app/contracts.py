from pydantic import BaseModel


class Hotel(BaseModel):
    """Contract for item."""

    name: str
    description: str 
    city: str
