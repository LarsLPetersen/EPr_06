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

MSG_CANCEL_BOOKING_OK = "Die Buchung wurde storniert."
MSG_CANCEL_BOOKING_FAIL = "Die Buchung konnte nicht storniert werden."
MSG_PAY_BILL_OK = "Die Rechnung wurde bezahlt."
MSG_PAY_BILL_FAIL = "Die Rechnung konnte nicht bezahlt werden."


class Guest:
    """Represents a usual guest of the hotel."""
    
    def __init__(self, first_name, last_name, id, is_active = True):
        """Creates a guest."""
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.bookings = []
        self.bookings_by_id = {}
        self.bills = []
        self.bills_by_id = {}
        
    def update(self, first_name, last_name, is_active):
        """Changes the personal attributes of a guest."""
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        
    def make_booking(self, start, end, room, hotel):
        """Allows the guest to make a booking."""
        booking = Booking(self, start, end, room, len(hotel.bookings))
        self.bookings.append(booking)
        self.bookings_by_id[len(hotel.bookings)] = booking
        room.bookings.append(booking)
        room.bookings_by_id[len(hotel.bookings)] = booking
        hotel.bookings.append(booking)
        hotel.bookings_by_id[len(hotel.bookings)] = booking
             
    def cancel_booking(self, booking):
        """Allows the guest to cancel one of his bookings."""
        if booking not in self.bookings:
            return [False, MSG_CANCEL_BOOKING_FAIL]
        elif booking.is_cancelled:
            return [False, MSG_CANCEL_BOOKING_FAIL]
        else:
            booking.is_cancelled = True
            return [True, MSG_CANCEL_BOOKING_OK]
            
    def pay(self, bill, date, hotel):
        """Allows the guest to pay one of his bills."""
        if bill not in self.bill:
            return [False, MSG_PAY_BILL_FAIL]
        elif bill.is_cancelled:
            return [False, MSG_PAY_BILL_FAIL]
        else:
            bill.pay_date = date
            bill.is_paid = True
            return [True, MSG_PAY_BILL_OK]
            
        
class Receptionist:
    """Represents a receptionist of the hotel."""
    
    def __init__(self, id, shift_plan = ""):
        """Creates a receptionist."""
        self.id = id
        self.shift_plan = shift_plan
        
    def __str__(self):
        """Print receptionist's data."""
        pretty_id = "RE-" + "{:0>3d}".format(self.id)
        return "{} {}".format(pretty_id, self.shift_plan)  
     
    def bill(self, booking, hotel):
        """Allows the receptionist to bill one of the bookings."""
        bill = Bill(booking.guest, booking, len(hotel.bills))
        booking.guest.bills.append(bill)
        booking.guest.bills_by_id[len(hotel.bills)] = bill
        hotel.bills.append(bill)
        hotel.bills_by_id[len(hotel.bills)] = bill
        
    def handout_keys(self, guest, room, num, hotel):
        """Hand out a key to the guest for a given room."""
        if hotel.key_table[room.id][0] + num >= 3:
            return [False, MSG_KEY_FAIL]
        else:
           hotel.key_table[room.id][0] += num
           hotel.key_table[room.id][1].append(guest.id)
           return [True, None]
    
    def receive_keys(self, guest, room, num, hotel):
        """Hand out a key to the guest for a given room."""
        if (hotel.key_table[room.id][0] + num >= 3) or \
           (hotel.key_table[room.id][0] < num) or \
           (guest.id not in hotel.key_table[room.id][1]):
            return [False, MSG_KEY_FAIL]
        else:
           hotel.key_table[room.id][0] -= num
           hotel.key_table[room.id][1].remove(guest.id)
           return [True, None]            