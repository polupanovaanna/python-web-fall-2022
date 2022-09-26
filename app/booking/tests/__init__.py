import unittest
import unittest.mock

from app.booking import contracts
from datetime import datetime
from app.booking import process_booking
from app.booking.hotels_text_database import bookings as bookings_db
from app import common


class TestBookings(unittest.TestCase):
    test_hotel = common.Hotel('Radisson', '', 'Russia', 'Moscow')
    test_hotel_2 = common.Hotel('Plaza', '', 'Russia', 'St-Petersburg')
    test_booking = common.Booking(1, 'Radisson', '2020-09-04', '2020-09-05', 10000)
    test_booking_2 = common.Booking(2, 'Plaza', '2020-10-04', '2020-10-05', 10000)

    def test_add_booking(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            self.assertTrue(datetime.fromisoformat(bookings_db[1].start_date)
                            and datetime.fromisoformat(bookings_db[1].end_date))
            self.assertEqual(bookings_db, {1: self.test_booking})

    def test_get_booking_by_id(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            booking = process_booking.get_booking_by_id(1)
            self.assertEqual(booking, self.test_booking)

    def test_get_all_bookings(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            process_booking.add_booking(self.test_booking_2)
            bookings = process_booking.get_all_user_bookings()
            self.assertEqual(len(bookings), 2)
            self.assertEqual(bookings_db, {1: bookings[0], 2: bookings[1]})
