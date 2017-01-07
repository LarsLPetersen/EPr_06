"""Contains the internal classes Guest and Receptionist."""

__author__ = "5625448: Lilian Mendoza de Sudan, 6290157: Lars Petersen"
__copyright__ = ""
__credits__ = "" 
__email__ = "lilian_mendoza@hotmail.com, petersen@informatik.uni-frankfurt.de"


# built-in modules
import time
import datetime
import sys
import pickle

# customized modules
from hotel import *


# constants for user information
MSG_CANCEL_BOOKING_OK = "Die Buchung wurde storniert."
MSG_CANCEL_BOOKING_FAIL = "Die Buchung konnte nicht storniert werden."
MSG_PAY_BILL_OK = "Die Rechnung wurde bezahlt."
MSG_PAY_BILL_FAIL = "Die Rechnung konnte nicht bezahlt werden."
MSG_KEY_FAIl = "Diese Anzahl an Schlüsseln kann nicht ausgegeben werden."


class Guest:
    """Represents a usual guest of the hotel."""
    
    def __init__(self, first_name, last_name, id, is_active = True):
        """Creates a guest."""
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.bookings_by_id = {}
        self.bills_by_id = {}
        
    def update(self, first_name, last_name, is_active):
        """Changes the personal attributes of a guest."""
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        
    def make_booking(self, start, end, room, hotel):
        """Allows the guest to make a booking."""
        booking = Booking(self, start, end, room, len(hotel.bookings_by_id))
        self.bookings_by_id[len(hotel.bookings_by_id)] = booking
        room.bookings_by_id[len(hotel.bookings_by_id)] = booking
        hotel.bookings_by_id[len(hotel.bookings_by_id)] = booking
             
    def cancel_booking(self, booking):
        """Allows the guest to cancel one of his bookings."""
        if booking.id not in self.bookings_by_id:
            return [False, MSG_CANCEL_BOOKING_FAIL]
        elif booking.is_cancelled:
            return [False, MSG_CANCEL_BOOKING_FAIL]
        else:
            booking.is_cancelled = True
            return [True, MSG_CANCEL_BOOKING_OK]
            
    def pay(self, bill, date, hotel):
        """Allows the guest to pay one of his bills."""
        if bill.id not in self.bills_by_id:
            return [False, MSG_PAY_BILL_FAIL]
        elif bill.is_cancelled:
            return [False, MSG_PAY_BILL_FAIL]
        else:
            bill.pay_date = date
            return [True, MSG_PAY_BILL_OK]
            
        
class Receptionist:
    """Represents a receptionist of the hotel."""
    
    def __init__(self, id):
        """Creates a receptionist."""
        self.id = id
        self.shift_plan = ""
        
    def __str__(self):
        """Print receptionist's data."""
        pretty_id = "RE-" + "{:0>3d}".format(self.id)
        return "{} {}".format(pretty_id, self.shift_plan)  
     
    def bill(self, booking, hotel):
        """Allows the receptionist to bill one of the bookings."""
        id = len(hotel.bills_by_id)
        bill = Bill(booking.guest, booking, id)
        booking.guest.bills_by_id[id] = bill
        hotel.bills_by_id[id] = bill
        
    def handout_keys(self, guest, room, num, hotel):
        """Hand out a key to the guest for a given room."""
        if hotel.key_table[room.id][0] + num >= 3:
            return [False, MSG_KEY_FAIL]
        else:
            try:
                hotel.key_table[room.id][1][guest.id] += num
            except KeyError:
                hotel.key_table[room.id][1][guest.id] = num
            hotel.key_table[room.id][0] += num
        return [True, None]
    
    def receive_keys(self, guest, room, num, hotel):
        """Hand out a key to the guest for a given room."""
        if (hotel.key_table[room.id][0] + num >= 3) or \
           (hotel.key_table[room.id][0] < num) or \
           (guest.id not in hotel.key_table[room.id][1].keys()):
            return [False, MSG_KEY_FAIL]
        else:
            try:
                hotel.key_table[room.id][1][guest.id] -= num
                hotel.key_table[room.id][0] -= num
                return [True, None]
            except KeyError:
                return [False, MSG_KEY_FAIL]
          