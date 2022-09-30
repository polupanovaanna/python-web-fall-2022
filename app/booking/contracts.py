from datetime import date
from pydantic import BaseModel


class Hotel(BaseModel):
    """Hotel Model"""

    name: str
    country: str
    city: str
    description: str | None = None


class Booking(BaseModel):
    """Booking Model"""
    hotels_name: str
    start_date: date
    end_date: date
    price: int
    comments: str | None = None
