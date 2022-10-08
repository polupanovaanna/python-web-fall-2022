import grpc

import common_serv
from builds.booking_pb2 import Booking, Id, Null
from builds.booking_pb2_grpc import ProcessBookingRequestServiceStub


def add_booking(booking: common_serv.Booking):
    '''
    Parse booking into proto and sends it to server
    :returns: bool
    '''
    with grpc.insecure_channel('localhost:4326') as channel:
        client = ProcessBookingRequestServiceStub(channel)
        booking_proto = Booking()
        booking_proto.hotels_name = booking.hotels_name
        booking_proto.start_date = str(booking.start_date)
        booking_proto.end_date = str(booking.end_date)
        booking_proto.price = booking.price
        if (booking.comments):
            booking_proto.comments = booking.comments
        client.AddBooking(Booking(hotels_name=booking.hotels_name,
                                  start_date=str(booking.start_date),
                                  end_date=str(booking.end_date), price=booking.price,
                                  comments=booking.comments))
        return True
       

def get_booking_by_id(id: int):
    '''
    Asks server for Booking proto by ir and parse it to Booking
    :returns: Booking
    '''
    with grpc.insecure_channel('localhost:4326') as channel:
        client = ProcessBookingRequestServiceStub(channel)
        id_proto = Id(value=id)
        booking = client.GetBooking(id_proto)
        if not booking.hotels_name:
            return False
        else:
            return common_serv.Booking(booking.id.value,
                                       booking.hotels_name,
                                       booking.start_date, booking.end_date,
                                       booking.price, booking.comments)


def get_all_user_bookings():
    '''
    Asks server for BookingsList proto and parse it to list of Booking elements
    :returns: List[Booking]
    '''
    with grpc.insecure_channel('localhost:4326') as channel:
        client = ProcessBookingRequestServiceStub(channel)
        bookings = client.GetAllBookings(Null())
        bookings_list = []
        for booking in bookings.items:
            bookings_list.append(common_serv.Booking(booking.id.value,
                                 booking.hotels_name,
                                 booking.start_date, booking.end_date,
                                 booking.price, booking.comments))
        return bookings_list
