"""This programm will simulate an hotel reception."""

__author__ = "5625448: Lilian Mendoza de Sudan, 6xxxxxx: Lars Petersen"
__copyright__ = "Copyright 2016/2017 – EPR1-Goethe-Universitaet" 
__email__ = "lilian_mendoza@hotmail.com, petersen@informatik.uni-frankfurt.de" 


import datetime
import random

class Guest(object):
    """Create an hotel guest"""

    def __init__(self, guest_id, arrival, departure, ):
        pass


class Receptionist(object):
    """Create an hotel reception employee"""

    TOTAL_NUM = 10

    def __init__(self, employee_id, shift = ""):
        """Initialize a receptionist"""

        self.employee_id = "RE-" + "{:0>3d}".format(employee_id)
        self.shift = shift

def get_date():
    """Retrieve a date from a the calendar."""

    chosen_date = datetime.date(2017, 12, 2)

    return chosen_date


def employee_shift(week, for_n_weeks, employee_list, empl):
    """Create a shift plan for an employee for n weeks.

    Start from a given date.
    """

    
    shift = ["--NNNN-", "--FFF--", "SSS---N","NN---FF","FF-SSSS"]
    shift_employee = ""
    
    for j in range(0, for_n_weeks):

        week_shift_employee = shift[((week + j)
                                     + employee_list.index(empl)) % 5]
        shift_employee += week_shift_employee

    return shift_employee
    
def work_plan(week, for_n_weeks, employee_list):
    """Summarize the shift plan for all employees for n weeks."""

    header = ("KW" + str(week + 1) + " - KW" +
              str(week + for_n_weeks)
              ).ljust(11) + " MO Di Mi Do Fr Sa So" * for_n_weeks
    
    print(header)
    
    for empl in employee_list:
        
        print(empl.employee_id.ljust(12) + "  ".join(
            k for k in employee_shift(week, for_n_weeks, employee_list, empl)))
    

def main():

    employee_list = []
    week = get_date().isocalendar()[1] - 1

    for i in range(1, Receptionist.TOTAL_NUM + 1):
        employee = Receptionist(i)
        employee_list.append(employee)

    for empl in employee_list:
        empl.shift = employee_shift(week, 4, employee_list, empl)

    work_plan(week, 5, employee_list)



    

main()
