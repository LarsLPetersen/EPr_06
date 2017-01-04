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
    complete_list = []
    total_num = 0
    
    def __init__(self, first_name, last_name, is_active = True):
        """ """
        self.id = Customer.total_num
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.bookings = []
        Customer.complete_list.append(self)
        Customer.total_num = len(Customer.complete_list)
        
    def update(self, first_name, last_name, is_active):
        """ """
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        
    def make_booking(self, start, end):
        """ """
        Booking(self.id, start, end)
        pass
             
    def cancel_booking(self, booking):
        """ """
        pass
        
    def pay(self, booking):
        """ """
        pass


class Receptionist:
    """ """
    complete_list = []
    total_num = 0
    work_plan = None
    
    @classmethod
    def create_work_plan(cls_obj, begin, end):
        """ """
        pass
        
    def __init__(self):
        """ """
        self.id = Receptionist.total_num
        self.shift_plan = ""
        Receptionist.complete_list.append(self)
        Receptionist.total_num = len(Receptionist.complete_list)
        