from concurrent.futures import ThreadPoolExecutor
import grpc

from serv_db import DataBase
import common_serv
from builds.booking_pb2 import Booking, BookingList, Null
from builds.booking_pb2_grpc import (
    ProcessBookingRequestServiceServicer as ServiceServicer,
    add_ProcessBookingRequestServiceServicer_to_server as add_to_server)


class Service(ServiceServicer):

    def AddBooking(self, request, context):
        '''
        Parses proto into booking class and adds to database
        :param request: Booking proto
        :returns: Null
        '''
        booking = common_serv.Booking(len(DataBase.bookings) + 1, request.hotels_name,
                                      request.start_date,
                                      request.end_date, request.price, request.comments)
        DataBase.bookings[len(DataBase.bookings) + 1] = booking
        return Null()
                           
    def GetBooking(self, request, context):
        '''
        Parses Id proto and gets booking by id from database
        :param request: Id proto
        :returns: Booking proto
        '''
        id = request.value
        if id in DataBase.bookings:
            booking = DataBase.bookings[id]
            booking_proto = Booking(hotels_name=booking.hotels_name,
                                    start_date=str(booking.start_date),
                                    end_date=str(booking.end_date), price=booking.price,
                                    comments=booking.comments)
            booking_proto.id.value = id
            return booking_proto
        else:
            return Null()

    def GetAllBookings(self, request, context):
        '''
        Gets all bookings from database
        :param request: Id proto
        :returns: Booking proto
        '''
        bookings = DataBase.bookings
        bookings_proto = BookingList()
        for id in bookings:
            booking = bookings[id]
            booking_proto = bookings_proto.items.add()
            booking_proto.id.value = id
            booking_proto.hotels_name = booking.hotels_name
            booking_proto.start_date = str(booking.start_date)
            booking_proto.end_date = str(booking.end_date)
            booking_proto.price = booking.price
            if (booking.comments):
                booking_proto.comments = booking.comments
        return bookings_proto


def execute_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_to_server(Service(), server)
    server.add_insecure_port("[::]:4326")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    execute_server()
