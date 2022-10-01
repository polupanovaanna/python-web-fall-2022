from typing import List
from booking_process_client import get_booking_by_id, add_booking, get_all_user_bookings
from common_serv import Booking
import booking_process_server
from serv_db import DataBase
from builds.booking_pb2_grpc import (
    add_ProcessBookingRequestServiceServicer_to_server as add_to_server,
)

import grpc
from concurrent.futures import ThreadPoolExecutor
import unittest
import unittest.mock
from parameterized import parameterized


class TestServer(unittest.TestCase):
    port = 4326

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.booking_db = DataBase.bookings

    def setUp(self) -> None:
        super().setUp()
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        add_to_server(booking_process_server.Service(), self.server)
        self.server.add_insecure_port('[::]:4326')
        self.server.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.server.stop(None)

    def testNoBookings(self):
        with unittest.mock.patch.dict(DataBase.bookings, self.booking_db):
            response = get_booking_by_id(1)
            self.assertEqual(response, False)
            response = get_all_user_bookings()
            self.assertEqual(response, [])

    @parameterized.expand(
        [([Booking(1, 'Radisson', '2002.11.11', '2003.01.10', 1000000)]),
         ([Booking(1, 'Plaza', '2002.11.11', '2003.01.10', 900000)]),
         ([Booking(1, 'Plaza', '2002.11.11', '2003.01.10', 900000, "Comment")])]
    )
    def testAddOneBooking(self, bookings: List[Booking]):
        with unittest.mock.patch.dict(DataBase.bookings, self.booking_db):
            response = add_booking(bookings)
            self.assertEqual(response, True)
            self.assertEqual(DataBase.bookings, {1: bookings})
            response = get_booking_by_id(0)
            self.assertEqual(response, False)
            response = get_booking_by_id(1)
            self.assertEqual(response, bookings)
            response = get_all_user_bookings()
            self.assertEqual(response[0].id, bookings.id)
            self.assertEqual(response, [bookings])

    @parameterized.expand(
        [[Booking(1, 'Radisson', '2002.11.11', '2003.01.10', 1000000),
          Booking(2, 'Plaza', '2002.11.11', '2003.01.10', 900000)]]
    )
    def testAddMultipleBooking(self, booking1, booking2):
        with unittest.mock.patch.dict(DataBase.bookings, self.booking_db):
            response = add_booking(booking1)
            self.assertEqual(response, True)
            response = add_booking(booking2)
            self.assertEqual(response, True)
            self.assertEqual(DataBase.bookings, {1: booking1, 2: booking2})
            response = get_booking_by_id(0)
            self.assertEqual(response, False)
            response = get_booking_by_id(1)
            self.assertEqual(response, booking1)
            response = get_booking_by_id(2)
            self.assertEqual(response, booking2)
            response = get_all_user_bookings()
            self.assertEqual(response, [booking1, booking2]) 


