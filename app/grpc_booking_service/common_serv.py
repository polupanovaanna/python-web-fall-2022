from datetime import date


class Booking:
    def __init__(
        self,
        id: int,
        hotels_name: str,
        start_date: date,
        end_date: date,
        price: int,
        comments: str | None = None
    ):   
        self.id = id
        self.hotels_name = hotels_name
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.comments = comments

    def __eq__(self, __o: object):
        if not isinstance(__o, Booking):
            return False
        
        booking: Booking = __o
        return self.id == booking.id
