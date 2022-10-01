import unittest
import unittest.mock

from datetime import datetime
from app.booking import process_booking
from app.booking.hotels_text_database import bookings as bookings_db
from app import common


class TestBookings(unittest.TestCase):
    test_booking = common.Booking(1, 'Radisson', '2020-09-04', '2020-09-05', 10000)
    test_booking_2 = common.Booking(2, 'Plaza', '2020-10-04', '2020-10-05', 10000)
    test_booking_comment = common.Booking(1, 'Plaza', '2020-10-04', '2020-10-05', 10000,
                                          'Some description')

    def test_add_booking(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            self.assertTrue(datetime.fromisoformat(bookings_db[1].start_date)
                            and datetime.fromisoformat(bookings_db[1].end_date))
            self.assertEqual(bookings_db, {1: self.test_booking})

    def test_add_multiple_bookings(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            process_booking.add_booking(self.test_booking_2)
            self.assertEqual(bookings_db, {1: self.test_booking,
                                           2: self.test_booking_2})

    def test_add_with_description(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking_comment)
            self.assertEqual(len(bookings_db), 1)
            self.assertEqual(bookings_db, {1: self.test_booking_comment})

    def test_get_booking_by_id(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            booking = process_booking.get_booking_by_id(1)
            self.assertEqual(booking, self.test_booking)

    def test_get_booking_by_id_when_multiple(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            process_booking.add_booking(self.test_booking_2)
            booking = process_booking.get_booking_by_id(1)
            self.assertEqual(booking, self.test_booking)
            booking = process_booking.get_booking_by_id(2)
            self.assertEqual(booking, self.test_booking_2)

    def test_get_booking_by_id_when_no_booking(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            booking = process_booking.get_booking_by_id(1)
            self.assertEqual(booking, {})
            process_booking.add_booking(self.test_booking)
            booking = process_booking.get_booking_by_id(48)
            self.assertEqual(booking, {})

    def test_get_all_bookings(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            process_booking.add_booking(self.test_booking_2)
            bookings = process_booking.get_all_user_bookings()
            self.assertEqual(len(bookings), 2)
            self.assertEqual(bookings_db, {1: bookings[0], 2: bookings[1]})

    def test_get_all_bookings_when_empty(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            bookings = process_booking.get_all_user_bookings()
            self.assertEqual(len(bookings), 0)
            self.assertEqual(bookings_db, {})

    def test_get_all_bookings_when_one_booking(self):
        with unittest.mock.patch.dict(bookings_db, {}):
            process_booking.add_booking(self.test_booking)
            bookings = process_booking.get_all_user_bookings()
            self.assertEqual(len(bookings), 1)
            self.assertEqual(bookings_db, {1: bookings[0]})
