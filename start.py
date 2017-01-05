"""This programm will simulate an hotel reception."""

__author__ = "5625448: Lilian Mendoza de Sudan, 6290157: Lars Petersen"
__copyright__ = "Copyright 2016/2017 – EPR1-Goethe-Universitaet" 
__email__ = "lilian_mendoza@hotmail.com, petersen@informatik.uni-frankfurt.de" 


from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import datetime
import time
import random
from displaycal import select_date

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

    def __str__(self):
        """Output receptionist's data"""

        return "{} {}".format(self.employee_id, self.shift)
    


def employee_shift(week, employee_list, empl, for_n_weeks = 4):
    """Create a shift plan for an employee for n weeks.

    Start from a given date.
    """

    shift = ["--NNNN-", "--EEE--", "LLL---N","NN---EE","FF-LLLL"]

    # Every five weeks the sequence of the shift will change
    if week % 5 == 0:

        random.shuffle(shift)
        
    shift_employee = ""
    
    for j in range(0, for_n_weeks):

        # get the week shift sequence for an employee j
        week_shift_employee = shift[((week -1 + j)
                                     + employee_list.index(empl)) % 5]
        
        # adds the next weeks' sequences
        shift_employee += week_shift_employee

    return shift_employee

def create_receptionist_list():
    """Create a list with all reception employees."""
    
    employee_list = []
    for i in range(1, Receptionist.TOTAL_NUM + 1):
        employee = Receptionist(i)
        employee_list.append(employee)

    for empl in employee_list:
        empl.shift = employee_shift(datetime.datetime.today().isocalendar()[1],
                                    employee_list, empl)

    return employee_list

    
def save_shift_plan(employee_list):
    """Save the current 4-week shift plan to a .txt file."""

    save_as = filedialog.asksaveasfile(mode = "w",
                                       defaultextension = ".txt")

    # if the save action was not cancelled...
    if save_as:

        # write the shift plan for each receptionist
        for empl in employee_list:
            save_as.write(str(empl) + "\n")
        save_as.close()

        messagebox.showinfo("Saved", "The shift plan has been saved.")

    else:
        #if the save action was cancelled, show error
        messagebox.showerror("", "Save was cancelled")
        
        
def load_shift_plan():
    pass



class MyHotel():
    
    def __init__(self, root, employee_list):

        self.root = root
        self.employee_list = employee_list
        self.root.title("My Hotel")

        self.top_menu = Menu(self.root)
        self.shift_menu = Menu(self.top_menu, tearoff = 0)
        self.top_menu.add_cascade(label = "Shift Plan", menu = self.shift_menu)
        self.shift_menu.add_command(label = "Create shift plan",
                           command = lambda: shift_plan(self.employee_list))
        self.shift_menu.add_command(label = "Save shift plan",
                           command = lambda: save_shift_plan(self.employee_list))
        self.shift_menu.add_command(label = "Load shift plan",
                           command = load_shift_plan)

        self.root.config(menu = self.top_menu)


def get_date():
    """Retrieve a date from a the calendar."""

    # select a date from the pop-up calendar from the module displaycal.py
   
    chosen_date = select_date()

    # or take the current date
    if not chosen_date:
        chosen_date = datetime.datetime.today()

    return chosen_date

    
def shift_plan(employee_list, for_n_weeks = 4):
    """Summarize the shift plan for all employees for n weeks."""

    week = get_date().isocalendar()[1]
    
    plan = Tk()
    plan.title("Shift plan")

    end_week = 52 if (week + for_n_weeks -1) % 52 == 0 \
               else (week + for_n_weeks -1) % 52
    
    header = ("KW" + str((week)) + " - KW" +
              str(end_week)
              ).ljust(12) + "   " + " MO Di Mi Do Fr Sa So" * for_n_weeks

    frame1 = Frame(plan)
    frame1.pack()
    Label(frame1, text = header, anchor = W, justify = RIGHT,
          font = ("Arial", 15)).pack()

    frame2 = Frame(plan)
    frame2.pack()
    scroll = Scrollbar(frame2)
    employee = Text(frame2, height = len(employee_list),
                    width = len(header) + 5)
    scroll.pack(side = RIGHT, fill = Y)
    employee.pack()
    scroll.config(command = employee.yview)
    employee.config(yscrollcommand = scroll.set)
    
    for empl in employee_list:
        employee.insert(END, "   " + empl.employee_id.ljust(12) + "     "+
                        "  ".join(
                            k for k in employee_shift(
                                week, employee_list, empl)
                            ) + "\n")
        
    frame3 = Frame(plan)
    frame3.pack()
    Label(frame3, text = "E : Early shift from 6:00 to 14:00 \n"\
                "L : Late shift from 14:00 to 22:00 \n"\
                "N : Night shift from 22:00 to 6:00",
          height = 4).pack(side = BOTTOM)

    for empl in employee_list:
        print(str(empl))
        
    plan.mainloop()
             


def create_wlan():
    """Create a 12-character-long code with p = 5.94e-72 """
    
    char = "0123456789" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
           "abcdefghijklmnopqrstuvwxyz" + "!?*#"
    
    key = ""
    
    for i in range(12):
        key += random.choice(char)

    return key


def main():
    """Run the program."""

    employee_list = create_receptionist_list()

    root = Tk()
    main_window = MyHotel(root, employee_list)
    root.mainloop()

   
if __name__ == "__main__":
    main()
