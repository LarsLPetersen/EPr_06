"""This programm will simulate an hotel reception."""

__author__ = "5625448: Lilian Mendoza de Sudan, 6xxxxxx: Lars Petersen"
__copyright__ = "Copyright 2016/2017 – EPR1-Goethe-Universitaet" 
__email__ = "lilian_mendoza@hotmail.com, petersen@informatik.uni-frankfurt.de" 


from tkinter import *
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox
import datetime
from time import *
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

    shift = ["--NNNN-", "--EEE--", "LLL---N","NN---EE","EE-LLLL"]

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



class MyHotel(tk.Frame):
    
    def __init__(self):
        self.root = Tk()

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
        
        # Date and clock
        self.frame0 = Frame(self.root)
        self.frame0.pack()
        self.clock = Label(self.frame0, text = "")
        self.clock.pack()
        self.update_clock()

        self.group1 = LabelFrame(self.root, text = "Buchungen",
                                 font = ("Arial", 18))
        self.group1.pack()

        header1 = "ID".center(11) + "Gast Nachnahme".center(20) + \
                 "Zimmer Nr.".center(15) + "Raum Typ".center(15) + \
                 "Von:".center(15) + "Bis:".center(15)
        
        self.columns = Label(self.group1, text = header1, height = 2,
                             width = len(header1))
        self.columns.pack()
        
        self.frame1a = Frame(self.group1)
        self.frame1a.pack()
        self.scroll1 = Scrollbar(self.frame1a, orient = VERTICAL)
        self.select1 = Listbox(self.frame1a, yscrollcommand = self.scroll1.set,
                               width = 60)
        self.scroll1.config (command = self.select1.yview)
        self.scroll1.pack(side = RIGHT, fill = Y)
        self.select1.pack(side = RIGHT, fill = BOTH)
        self.select1.bind("<Double-1>", lambda x: self.load_booking())
        
        self.frame1b = Frame(self.group1)
        self.frame1b.pack()
        b1 = Button(self.frame1b, text = "Bearbeiten",
                    command = self.edit_booking)
        b1.pack(side = LEFT)
        b2 = Button(self.frame1b, text = "Stornieren",
                    command = self.cancel_booking)
        b2.pack(side = LEFT)
        b3 = Button(self.frame1b, text ="Neue Buchung",
                    command = self.new_booking)
        b3.pack(side = LEFT)
        b4 = Button(self.frame1b, text = "Rechnung",
                    command = self.print_bill)
        b4.pack(side = RIGHT)

        self.group2 = LabelFrame(self.root, text = "Kapazitäten")
        self.group2.pack(side = LEFT)

        self.group2a = LabelFrame(self.group2, text = "")
        self.group2a.pack(side = LEFT)

        self.frame2 = Frame(self.group2a)
        self.frame2.pack(side = LEFT)

        # Start and End entries
        self.from_date_var = StringVar()
        self.to_date_var = StringVar()
        self.room_type_var = StringVar()

        self.start_date = Frame(self.frame2)
        self.start_date.pack()
        self.from_date = Label(self.start_date, text = "Von:")
        self.from_date.pack(side = LEFT)
        self.from_date_field = Entry(self.start_date, width = 12,
                                     textvariable = self.from_date_var)
        self.from_date_field.pack(side = RIGHT)

        self.end_date = Frame(self.frame2)
        self.end_date.pack()
        self.to_date = Label(self.end_date, text = "Bis: ")
        self.to_date.pack(side = LEFT)
        self.to_date_field = Entry(self.end_date, width = 12,
                                     textvariable = self.to_date_var)
        self.to_date_field.pack(side = RIGHT)

        # room type
        self.room_t = Frame(self.frame2)
        self.room_t.pack()
        self.room_name = Label(self.room_t, text = "Typ:".ljust(4))
        self.room_name.pack(side = LEFT)
        self.room_type_sb = Spinbox(self.room_t, values = ("S", "D"),
                                 state = "readonly", width = 2,
                                 textvariable = self.room_type_var,
                                 command = lambda: self.room_type_var.get())
        self.room_type_sb.pack(side = RIGHT)

        self.search_button = Frame(self.frame2)
        self.search_button.pack()
        b5 = Button(self.search_button, text = "Suchen", height = 3,
                    command = self.search_crit)
        b5.pack()
        b6 = Button(self.search_button, text = "Zurücksetzen", height = 2,
                    command = self.clear_search)
        b6.pack()

        self.frame3 = LabelFrame(self.group2a, text = "Ergebnisse")
        self.frame3.pack(side = RIGHT)

        self.results = Label(self.frame3, text = "Raum ID".center(10) + \
                             "Raum Nr".center(10))
        self.results.pack()
        self.scroll2 = Scrollbar(self.frame3, orient = VERTICAL)
        self.select2 = Listbox(self.frame3, yscrollcommand = self.scroll2.set)
        self.scroll2.config (command = self.select2.yview)
        self.scroll2.pack(side = RIGHT, fill = Y)
        self.select2.pack(fill = BOTH)

        self.group3 = LabelFrame(self.root, text = "Rechnungen")
        self.group3.pack()

        self.billing = Frame(self.group3)
        self.billing.pack()
        self.billing_label = Label(self.billing, text = "Rech. ID".center(15) +
                             "Buchung ID".center(15) +
                             "Preis".center(20), height = 2)
        self.billing_label.pack()

        self.scroll3 = Scrollbar(self.billing, orient = VERTICAL)
        self.select3 = Listbox(self.billing, yscrollcommand = self.scroll3.set)
        self.scroll3.config(command = self.select3.yview)
        self.scroll3.pack(side = RIGHT, fill = Y)       
        self.select3.pack(fill = BOTH)

        b7 = Button(self.group3, text = "Stornieren", height = 2,
                    command = self.cancel_bill)
        b7.pack(side = LEFT)
        b8 = Button(self.group3, text = "Bezahlen", height = 2,
                    command = self.pay_bill)
        b8.pack(side = RIGHT)
        
        
        
        self.root.mainloop()


    def update_clock(self):
        """Update the clock"""
        
        now = time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.localtime())
        self.clock.configure(text = now)

        self.root.after(200, self.update_clock)

    def load_booking(self):
        pass

    def edit_booking(self):
        pass

    def cancel_booking(self):
        pass

    def new_booking(self):
        pass

    def print_bill(self):
        pass

    def search_crit(self):
        pass

    def clear_search(self):
        pass

    def cancel_bill(self):
        pass

    def pay_bill(self):
        pass
    
class DateEntry:
    """Window for ..."""
    
    def __init__(self, parent):
        """Creates the SearchChoice-Window"""
        self.root = tk.Toplevel()
        self.container = tk.LabelFrame(self.root, text = "Eingabe")
        self.container.pack()
        self.parent = parent
        
        global entry
        entry = tk.StringVar()
        entry.set(parent.date)
        
        self.entry = tk.Entry(self.container, textvariable = entry)
        self.entry.pack()
        
        self.button = tk.Button(self.container, text = "Weiter", \
                command = lambda: self.get_date(parent))
        self.button.pack()
    
    def get_date(self, parent):
        """Retrieve a date from an entry field."""
        
        parent.date = entry.get()
        
        if parent.date == "":
            self.entry.configure(bg = "yellow")
            messagebox.showwarning("Unvollständig!",
                                   "Bitte füllen Sie das Feld aus!")
        else:
            try:
                x = strptime(parent.date, '%d.%m.%Y')
                x = datetime.datetime(*(x[0:6]))
                self.entry.configure(bg = "white")

                if x < datetime.datetime.today():
                    self.entry.configure(bg = "yellow")
                    messagebox.showwarning("Fehler", "Das Datum "
                                           "liegt in der Vergangenheit!")
                else:
                    parent.date = x

            except ValueError:
                self.entry.configure(bg = "yellow")
                messagebox.showwarning("Fehler!", "Bitte geben Sie "
                                       "ein gültiges Datum ein!"
                                       "\n tt.mm.jjjj")
        
##
##def get_date():
##    """Retrieve a date from a the calendar."""
##
##    # select a date from the pop-up calendar from the module displaycal.py
##   
##    chosen_date = select_date()
##
##    # or take the current date
##    if not chosen_date:
##        chosen_date = datetime.datetime.today()
##
##    return chosen_date
##
    
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
    

    
def main():
    """Run the program."""

    employee_list = create_receptionist_list()
    
    main_window = MyHotel()

            

   
if __name__ == "__main__":
    main()
