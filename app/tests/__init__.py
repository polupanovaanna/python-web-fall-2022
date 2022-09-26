import unittest
import unittest.mock

from app.booking.hotels_text_database import bookings as booking_db
from app.main import app
from fastapi.testclient import TestClient


class IntegrationTests(unittest.TestCase):
    client = TestClient(app)

    def setUp(self) -> None:
        super().setUp()
        self.booking_db = {}

    def testAskForBookingsEmpty(self):
        with unittest.mock.patch.dict(booking_db, self.booking_db):
            response = self.client.get('/users/bookings')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                             {'info': 'There are no booked hotels yet'})

    def testAskForBookingsOneBooking(self):
        with unittest.mock.patch.dict(booking_db, self.booking_db):
            self.client.post(
                '/users/bookings',
                json={'hotels_name': 'Radisson', 'start_date': '2020-09-01',
                      'end_date': '2020-09-10', 'price': 1000},
            )
            response = self.client.get('/users/bookings')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                             {'bookings_list': [{'comments': None,
                              'end_date': '2020-09-10', 'hotels_name': 'Radisson',
                              'id': 1, 'price': 1000, 'start_date': '2020-09-01'}]})

            response = self.client.get('/users/bookings/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                             {'comments': None,
                              'end_date': '2020-09-10', 'hotels_name': 'Radisson',
                              'id': 1, 'price': 1000, 'start_date': '2020-09-01'})

    def testAskForBookingsMultipleBookings(self):
        with unittest.mock.patch.dict(booking_db, self.booking_db):
            self.client.post(
                '/users/bookings',
                json={'hotels_name': 'Radisson', 'start_date': '2020-09-01',
                      'end_date': '2020-09-10', 'price': 1000},
            )
            self.client.post(
                '/users/bookings',
                json={'hotels_name': 'Plaza', 'start_date': '2020-10-11',
                      'end_date': '2020-10-22', 'price': 10330},
            )
            response = self.client.get('/users/bookings')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                             {'bookings_list': [{'comments': None,
                              'end_date': '2020-09-10', 'hotels_name': 'Radisson',
                              'id': 1, 'price': 1000, 'start_date': '2020-09-01'},
                              {'comments': None,
                              'end_date': '2020-10-22', 'hotels_name': 'Plaza',
                              'id': 2, 'price': 10330, 'start_date': '2020-10-11'}]})

            response = self.client.get('/users/bookings/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                             {'comments': None,
                              'end_date': '2020-09-10', 'hotels_name': 'Radisson',
                              'id': 1, 'price': 1000, 'start_date': '2020-09-01'})

            response = self.client.get('/users/bookings/2')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                             {'comments': None,
                              'end_date': '2020-10-22', 'hotels_name': 'Plaza',
                              'id': 2, 'price': 10330, 'start_date': '2020-10-11'})


