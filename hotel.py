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

# customized modules
from actors import *


class Booking:
    """Represents a booking made by a customer"""
    
    complete_list = []
    total_num = 0
    
    def __init__(self, customer_id, start, end, room_id):
        """Creates a booking"""
        self.id = Booking.total_num
        self.customer_id = customer_id
        self.start = start
        self.end = end
        self.room_id = room_id
        self.is_cancelled = False
        self.is_paid = False
        self.price = self.get_price(start, end, room_id)
        Booking.complete_list.append(self)
        Booking.total_num = len(Booking.complete_list)
        
    def update(self, start, end, is_cancelled, price, is_paid):
        """Allows for a modification of the given booking"""
        self.start = start
        self.end = end
        self.is_cancelled = is_cancelled
        self.is_paid = is_paid
        self.id = Booking.total_num
        
    def get_price(self, start, end, room):
        """Calculates the preliminary price of the booking
        
           type(start) = type(end) = datetime.date(y, m , d)
           type(room) = Room 
        """
        return (end - start).days() * room.price_per_night 
        
    def write_to_file():
        """ """
        pass
    
    def read_from_file():
        """ """
        pass
        
            
class Room:
    """Represents a room in the hotel"""
    
    complete_list = []
    total_num = 0
    
    @classmethod
    def available_rooms(cls_obj, type, begin, end):
        """Checks which rooms of the given type are available in timeframe"""
        result = []
        for room in cls_obj.complete_list:
            if room.type == type and room.is_available(begin, end)[0]:
                result.append(room)
        return result
    
    @classmethod
    def num_rooms(cls_obj, type):
        """Counts number of rooms of given type """
        result = 0
        for room in cls_obj.complete_list:
            if room.type == type:
                result += 1
        return result
        
    
    def __init__(self, type, number, price_per_night, num_keys):
        """Creates a room"""
        self.type = type
        self.number = number
        self.price_per_night = price_per_night
        self.num_keys = num_keys
        self.num_keys_customer = 0
        self.num_keys_lobby = self.num_keys - self.num_keys_customer
        self.bookings = []
        self.occupancy = []
        Room.complete_list.append(self)
        Room.total_num = len(Room.complete_list)
        
    def is_available(self, begin, end):
        """Checks is given room is available in given timeframe"""
        result = [True, None]
        for i in range((end - begin).days - 1):
            if self.occupancy.__contains__(begin + datetime.timedelta(i)):
                result = [False, begin + begin + datetime.timedelta(i)]
                break
        return result
    
    
    def write_to_file():
        """ """
        pass
    
    def read_from_file():
        """ """
        pass    


class Hotel:
    """ """
    
    def __init__(self, file_name = None):
        """ """
        if file_name != None:
            self.rooms = self.read_from_file(file_name).rooms
            self.bookings = self.read_from_file(file_name).bookings
            self.customers = self.read_from_file(file_name).customers
            self.receptionists = self.read_from_file(file_name).receptionists
        else:
        # create an example skeleton of a hotel"""
            self.rooms = []
            self.bookings = []
            self.customers = []
            self.receptionists = []
            
            types = ["single", "double"]
            num_rooms = [20, 40]
            prices = [48, 78]
            num_keys_per_room = [3, 3]
            num_customers = 7
            num_receptionists = 5
            # adding single rooms      
            for i in range(20):
                self.rooms.append(Room(types[0], str(i + 1), prices[0], num_keys_per_room[0]))
            # adding double rooms
            for i in range(40):
                self.rooms.append(Room(types[1], str(i + 101), prices[1], num_keys_per_room[1]))
            # adding customers
            for i in range(7):
                self.customers.append(Customer("Vorname_" + str(i), "Nachname_" + str(i)))
            # adding receptionists    
            for i in range(5):
                self.receptionists.append(Receptionist())
                
            self.write_to_file("Example_Hotel.pkl")
        
    def write_to_file(self, file_name):
        """Writes hotel example to a pkl-file"""
        output = open(file_name, "wb")
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
            self.write_to_file(file_name, [])
            return []
        
        
if __name__ == "__main__":
    hotel = Hotel("Example_Hotel.pkl")
    for room in hotel.rooms:
        print(room.number, room.price_per_night, room.type)
    for customer in hotel.customers:
        print(customer.id, customer.first_name, customer.last_name)
    