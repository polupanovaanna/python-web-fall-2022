from fastapi import APIRouter
from datetime import date
from app.booking import contracts
from app.booking import process_booking

router = APIRouter()


@router.get('/users/bookings/{booking_id}')
async def get_user_booking(booking_id: int):
    booking_item = process_booking.get_booking_by_id(booking_id)
    return booking_item


@router.get('/users/bookings')
async def get_all_user_bookings():
    bookings = process_booking.get_all_user_bookings()
    if len(bookings) == 0:
        return {'info': 'There are no booked hotels yet'}
    else:
        return {'bookings_list': bookings}


@router.post('/users/bookings')
async def create_booking(
    booking: contracts.Booking
):
    return process_booking.add_booking(booking)
