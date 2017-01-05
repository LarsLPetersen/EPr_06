""" ... """

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


class Customer:
    """  """
    
    def __init__(self, first_name, last_name, id, is_active = True):
        """ """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.bookings = []
        
    def update(self, first_name, last_name, is_active):
        """ """
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        
    def make_booking(self, start, end, room, hotel):
        """ """
        booking = Booking(self, start, end, room, len(hotel.bookings))
        self.bookings.append(booking)
        room.bookings.append(booking)
        hotel.bookings.append(booking)
             
    def cancel_booking(self, booking, hotel):
        """ """
        if booking not in self.bookings or booking.is_cancelled:
            pass
        else:
            booking.is_cancelled = True
        
    def pay(self, booking):
        """ """
        pass


class Receptionist:
    """ """
    
    def __init__(self, id):
        """ """
        self.id = id
        self.shift_plan = None