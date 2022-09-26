
from app.booking import contracts
from app.booking.hotels_text_database import bookings as bookings_db
from app import common

from datetime import date


def add_booking(
    booking: contracts.Booking
):
    booking_item = common.Booking(len(bookings_db) + 1, booking.hotels_name, 
                                  booking.start_date, booking.end_date,
                                  booking.price, booking.comments)
    bookings_db[len(bookings_db) + 1] = booking_item
    return True


def get_all_user_bookings():
    bookings_list = []
    for key in bookings_db:
        bookings_list.append(get_booking_by_id(key))
    return bookings_list


def get_booking_by_id(booking_id: int):
    if booking_id in bookings_db:
        return bookings_db[booking_id]
    return {}
