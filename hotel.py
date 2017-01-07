"""Contains the main internal classes Hotel, Room, Booking and Bill."""

__author__ = "5625448: Lilian Mendoza de Sudan, 6290157: Lars Petersen"
__copyright__ = ""
__credits__ = "" 
__email__ = "lilian_mendoza@hotmail.com, petersen@informatik.uni-frankfurt.de"


# built-in modules
import time
import datetime
import sys
import pickle
import os, os.path
import random
import string

# customized modules
from actors import *


MSG_CANCEL_BILL_OK = "Die Rechnung wurde storniert."
MSG_CANCEL_BILL_FAIL = "Die Rechnung konnte nicht storniert werden."
MSG_INTERSECTION_EMPTY = "Es gibt keine Überschneidung."

def list_days(start, end):
    """Returns the list of all days from start-day to end-day."""
    return [start + datetime.timedelta(i) for i in \
            range((end - start).days + 1)]       


def list_nights(start, end):
    """Lists all nights [day_before, day_after] from start-day to end-day."""
    result = []
    for i in range((end - start).days):
        result.append([start + datetime.timedelta(i), \
                       start + datetime.timedelta(i + 1)])
    return result

class Key:
    """ """
    def __init__(self, id, room, guest = None):
        """ """
        self.id = id
        self.room = room
        self.guest = guest
        
                
class Bill:
    """Represents a bill derived from a booking."""
    
    def __init__(self, guest, booking, id):
        """Creates a bill for a given guest and a given booking."""
        self.id = id
        self.guest = guest
        self.booking = booking
        self.value = booking.price
        self.is_cancelled = False
        self.pay_date = None
        
    def update_price(self, price):
        """Allows to modify the price of the given booking."""
        self.price = price
        
    def cancel(self):
        """Allows to cancel the bill."""
        if self.is_cancelled:
            return [False, MSG_CANCEL_BILL_FAIL]
        else:
            self.is_cancelled = True
            return [True, MSG_CANCEL_BILL_OK]
        
            
class Booking:
    """Represents a booking made by a guest."""
    
    def __init__(self, guest, start, end, room, id):
        """Creates a booking"""
        self.id = id
        self.guest = guest
        self.start = start
        self.end = end
        self.room = room
        self.price = self.get_price()
        self.wlan_key = self.generate_wlan_key()
        self.is_cancelled = False
        self.is_billed = False
        
    def update(self, start, end, room, is_cancelled, price, is_billed):
        """Allows for a modification of the given booking"""
        self.start = start
        self.end = end
        self.room = room
        self.is_cancelled = is_cancelled
        self.is_billed = is_billed
        
    def get_price(self):
        """Calculates the preliminary price of the booking."""
        return (self.end - self.start).days * self.room.price_per_night
        
    def intersection(self, other):
        """ """
        if not(self.is_cancelled or other.is_cancelled):
            conflict = set(self.get_days()).intersection(set(other.get_days()))
            if len(conflict) < 2:
                return [False, MSG_INTERSECTION_EMPTY]
            else: return [True, list(conflict)]
        else: return [False, MSG_INTERSECTION_EMPTY]
                
    def get_days(self):
        """Returns the list of the days covered by this booking."""
        return list_days(self.start, self.end)
        
    def get_nights(self):
        """Returns the list of the nights covered by this booking."""
        return list_nights(self.start, self.end)
        
    def generate_wlan_key(self, size = 10):
        """Returns the list of the days covered by this booking."""
        preface = str(self.room.id)
        characters = string.ascii_letters + string.punctuation + string.digits
        random_part = "".join(random.choice(characters) for _ in range(size))
        return preface + random_part
        
        
class Room:
    """Represents a room in the hotel."""
     
    def __init__(self, type, number, price_per_night, num_keys, id):
        """Creates a room."""
        self.id = id
        self.type = type
        self.number = number
        self.price_per_night = price_per_night
        self.num_keys = num_keys
        self.bookings = []
        self.bookings_by_id = {}
        
    def is_available(self, start, end):
        """Checks if the given room is available within the given timeframe."""
        days = set(list_days(start, end))
        conflicts = []
        for booking in self.bookings:
            conflict = set(booking.get_days()).intersection(days)
            if len(conflict) >= 2:
                conflicts.append(list(conflict))
        return [True if len(conflicts) == 0 else False, conflicts]
        
    def evaluate_occupation(self):
        """Lists all the nights for which this room is booked."""
        result = []
        for booking in self.bookings:
            if not booking.is_cancelled:
                result.extend(booking.get_nights())
        return sorted(result)
        
INIT_TYPES = ["single", "double"]
INIT_NUM_ROOMS = [20, 40]
INIT_PRICES = [48, 78]
INIT_NUM_KEYS_PER_ROOM = [3, 3]
INIT_NUM_BOOKINGS = 12
INIT_NUM_GUESTS = 10
INIT_NUM_RECEPTIONISTS = 5    

class Hotel:
    """Represents the main object hotel."""
    
    def __init__(self, file_name = None):
        """Instatiates the fundamental hotel object of the application."""
        if file_name != None:
            self.file_name = file_name
            self.rooms = self.read_from_file(file_name).rooms
            self.rooms_by_id = self.read_from_file(file_name).rooms_by_id
            self.bookings = self.read_from_file(file_name).bookings
            self.bookings_by_id = self.read_from_file(file_name).bookings_by_id
            self.bills = self.read_from_file(file_name).bills
            self.bills_by_id = self.read_from_file(file_name).bills_by_id
            self.guests = self.read_from_file(file_name).guests
            self.guests_by_id = self.read_from_file(file_name).guests_by_id
            self.receptionists = self.read_from_file(file_name).receptionists
            self.receptionists_by_id = \
                    self.read_from_file(file_name).receptionists_by_id
            self.work_plan = self.read_from_file(file_name).work_plan
            self.key_table = self.read_from_file(file_name).key_table
        else:
        # create an example
            self.file_name = "Example_Hotel.pkl"
            self.rooms = []
            self.rooms_by_id = {}
            self.bookings = []
            self.bookings_by_id = {}
            self.bills = []
            self.bills_by_id = {}
            self.guests = []
            self.guests_by_id = {}
            self.receptionists = []
            self.receptionists_by_id = {}
            self.work_plan = {}
            self.key_table = {}
            
            
            # adding single rooms      
            for i in range(INIT_NUM_ROOMS[0]):
                room = Room(INIT_TYPES[0], str(i + 1), INIT_PRICES[0],\
                                       INIT_NUM_KEYS_PER_ROOM[0],i)
                self.rooms.append(room)
                self.rooms_by_id[i] = room
                
            # adding double rooms
            for i in range(INIT_NUM_ROOMS[1]):
                room = Room(INIT_TYPES[1], str(i + 1), INIT_PRICES[1],\
                                       INIT_NUM_KEYS_PER_ROOM[1],i)
                self.rooms.append(room)
                self.rooms_by_id[i] = room
                
            # adding guests
            for i in range(INIT_NUM_GUESTS):
                guest = Guest("Vorname_" + str(i), "Nachname_" + str(i), i)
                self.guests.append(guest)
                self.guests_by_id[i] = guest
                    
            # adding receptionists    
            for i in range(INIT_NUM_RECEPTIONISTS):
                receptionist = Receptionist(i)
                self.receptionists.append(receptionist)
                self.receptionists_by_id[i] = receptionist
                
            # initiating work_plan
            self.generate_shift_plans(datetime.date.today().isocalendar()[1])
            
            # initiating key_table
            self.initiate_key_table()
            
            # adding bookings
            for i in random.sample(range(sum(INIT_NUM_ROOMS)),\
                                                            INIT_NUM_BOOKINGS):
                self.guests[random.randrange(0, INIT_NUM_GUESTS)].make_booking(\
                        datetime.date(2017, 1, 1),\
                        datetime.date(2017, 1, random.randint(2, 15)),\
                        self.rooms[i],\
                        self)
                
            
            self.write_to_file()
        
    def available_rooms(self, type, start, end):
        """Checks which rooms of the given type are available in timeframe"""
        return [room for room in self.rooms if (room.type == type and \
                room.is_available(start, end)[0])]
                
    def get_revenue(self, date):
        """Computes the revenue (by actual payments) made on the given date."""
        return list(map(sum, [bill.value for bill in self.bills \
                                                    if bill.pay_date == date]))

    def update(self):
        """Saves current changes on the hotel and re-creates it."""
        self.write_to_file()
        self.__init__(self.file_name)
        
    def write_to_file(self):
        """Saves the hotel object in a pkl-file."""
        output = open(self.file_name, "wb")
        pickle.dump(self, output)
        output.close()
    
    def read_from_file(self, file_name):
        """Reads entries from a saved hotel into an object."""
        if os.path.isfile(file_name):
            input = open(file_name, "rb")
            data = pickle.load(input)
            return data
            input.close()
        else: pass
    
    def initiate_key_table(self):
        """ """
        # key-disitribution: [num of keys with guests, {guest: num_keys}]
        for id in self.rooms_by_id.keys():
            self.key_table[id] = [0, {}]
        
    def generate_shift_plans(self, week, num_weeks = 4):
        """Create the num_weeks work plan for the receptionists.

        Start from a given date.
        """
        pattern = ["--NNNN-", "--FFF--", "SSS---N","NN---FF", "FF-SSSS"]

        for id in self.receptionists_by_id.keys():
            self.receptionists_by_id[id].shift_plan = ""
            for j in range(num_weeks):
                # get the week shift sequence for an employee j
                week_shift = pattern[((week - 1 + j) + id) % 5]
                # adds the next weeks' sequences
                self.receptionists_by_id[id].shift_plan += week_shift
            self.work_plan[id] = self.receptionists_by_id[id].shift_plan
        
    def short_info(self):
        """Yields info on the bookings of the hotel (auxiliary function)"""
        return [[booking.id, booking.guest.id, booking.room.id, str(booking.start), 
                 str(booking.end)] for booking in self.bookings]

