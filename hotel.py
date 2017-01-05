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
import os.path
import random

# customized modules
from actors import *

class Helper:
    """ """
    
    @staticmethod
    def list_days(start, end):
        """ """
        return [start + datetime.timedelta(i) for i in \
                range((end - start).days + 1)]       
    
    
    @staticmethod
    def list_nights(start, end):
        """ """
        result = []
        for i in range((end - start).days):
            result.append([start + datetime.timedelta(i), \
                           start + datetime.timedelta(i + 1)])
        return result

        
class Booking:
    """Represents a booking made by a customer"""
    
    def __init__(self, customer, start, end, room, id):
        """Creates a booking"""
        self.id = id
        self.customer = customer
        self.start = start
        self.end = end
        self.room = room
        self.is_cancelled = False
        self.is_paid = False
        
    def update(self, start, end, room, is_cancelled, price, is_paid):
        """Allows for a modification of the given booking"""
        self.start = start
        self.end = end
        self.room = room
        self.is_cancelled = is_cancelled
        self.is_paid = is_paid
        
    def get_price(self):
        """Calculates the preliminary price of the booking
        
           type(start) = type(end) = datetime.date(y, m, d)
           type(room) = Room 
        """
        return (self.end - self.start).days * self.room.price_per_night
        
    def intersection(self, other):
        """ """
        if not(self.is_cancelled or other.is_cancelled):
            conflict = set(self.get_days()).intersection(set(other.get_days()))
            if len(conflict) < 2:
                return [False, []]
            else: return [True, list(conflict)]
        else: return [False, []]
                
    def get_days(self):
        """ """
        return Helper.list_days(self.start, self.end)
        
    def get_nights(self):
        """ """
        return Helper.list_nights(self.start, self.end)
        
    
    
class Room:
    """Represents a room in the hotel"""
     
    def __init__(self, type, number, price_per_night, num_keys, id):
        """Creates a room"""
        self.id = id
        self.type = type
        self.number = number
        self.price_per_night = price_per_night
        self.num_keys = num_keys
        self.num_keys_customer = 0
        self.num_keys_lobby = self.num_keys - self.num_keys_customer
        self.bookings = []
        
    def is_available(self, start, end):
        """Checks is given room is available in given timeframe"""
        days = set(Helper.list_days(start, end))
        conflicts = []
        for booking in self.bookings:
            conflict = set(booking.get_days()).intersection(days)
            if len(conflict) >= 2:
                conflicts.append(list(conflict))
        return [True if len(conflicts) == 0 else False, conflicts]
        
        
    def evaluate_occupation(self):
        """ """
        result = []
        for booking in self.bookings:
            if not booking.is_cancelled:
                result.extend(booking.get_nights())
        return sorted(result)
        
    

class Hotel:
    """ """
    
    def __init__(self, file_name = None):
        """Instatiates the fundamental hotel object of the application"""
        if file_name != None:
            self.file_name = file_name
            self.rooms = self.read_from_file(file_name).rooms
            self.bookings = self.read_from_file(file_name).bookings
            self.customers = self.read_from_file(file_name).customers
            self.receptionists = self.read_from_file(file_name).receptionists
            self.w_lan_keys = self.read_from_file(file_name).w_lan_keys
            self.work_plan = self.read_from_file(file_name).work_plan
        else:
        # create an example"""
            self.file_name = "Example_Hotel.pkl"
            self.rooms = []
            self.bookings = []
            self.customers = []
            self.receptionists = []
            self.w_lan_keys = dict()  # {customer1:w_lan_key, ...} 
            self.work_plan = None
            
            init_types = ["single", "double"]
            init_num_rooms = [20, 40]
            init_prices = [48, 78]
            init_num_keys_per_room = [3, 3]
            init_num_bookings = 12
            init_num_customers = 10
            init_num_receptionists = 5
            
            # adding single rooms      
            for i in range(init_num_rooms[0]):
                self.rooms.append(Room(init_types[0], str(i + 1),\
                                       init_prices[0],\
                                       init_num_keys_per_room[0],\
                                       i))
            # adding double rooms
            for i in range(init_num_rooms[1]):
                self.rooms.append(Room(init_types[1], str(i + 101),\
                                    init_prices[1], init_num_keys_per_room[1],\
                                    i + init_num_rooms[0]))
                
            # adding customers
            for i in range(init_num_customers):
                self.customers.append(Customer("Vorname_" + str(i),\
                                               "Nachname_" + str(i),\
                                               i))
            # adding bookings
            for i in random.sample(range(sum(init_num_rooms)), init_num_bookings):
                self.customers[random.randrange(0, init_num_customers)].make_booking(\
                        datetime.date(2017, 1, 1),\
                        datetime.date(2017, 1, random.randint(2, 15)),\
                        self.rooms[i],\
                        self)
                
            # adding receptionists    
            for i in range(init_num_receptionists):
                self.receptionists.append(Receptionist(i))
                
            self.write_to_file()
        
    def available_rooms(self, type, start, end):
        """Checks which rooms of the given type are available in timeframe"""
        return [room for room in self.rooms if (room.type == type and \
                room.is_available(start, end)[0])]
                
    def update(self):
        """ """
        self.write_to_file()
        self.__init__(self.file_name)
        
    def write_to_file(self):
        """Writes hotel example to a pkl-file"""
        output = open(self.file_name, "wb")
        pickle.dump(self, output)
        output.close()
    
    def read_from_file(self, file_name):
        """Reads entries from a saved hotel into an object"""
        
        if os.path.isfile(file_name):
            input = open(file_name, "rb")
            data = pickle.load(input)
            return data
            input.close()
        else:
            pass
        
        
if __name__ == "__main__":
    hotel = Hotel("Example_Hotel.pkl")
    
    #start1 = datetime.date(2017, 1, 1)
    #end1 = datetime.date(2017, 1, 19)
    #start2 = datetime.date(2017, 1, 4)
    #end2 = datetime.date(2017, 1, 19)
    
    #for room in hotel.rooms:
    #    print(room.id, room.bookings)
    #print(hotel.rooms[4].evaluate_occupation())
    #print(hotel.rooms[4].is_available(start1, end1))
    #print([room.id for room in hotel.available_rooms("double", start1, end1)])
    