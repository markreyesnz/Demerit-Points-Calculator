#Mark Reyes
#DTEC501
#Speeding Calculator

from tkinter import *
from tkinter.messagebox import *

def get_demerit_points(driving_speed, speed_limit, light_trailer=False, school_zone=False, holiday_period=False):
    """ works out the demerit points for a driving speed in a particular speed limited zone. """

#Find out the difference in driving speed and speed limit.
    acceleration_difference = driving_speed - speed_limit

    
#Validate if in speed limited zone, holiday period, or pulling a trailer with regards to speed differences and return a boolean value. 
    if school_zone or holiday_period:
        if acceleration_difference > 4:
            imposed_penalty = True
        else:
            imposed_penalty = False

    elif light_trailer:
        if acceleration_difference > 5:
            imposed_penalty = True
        else:
            imposed_penalty = False

    else:
        if acceleration_difference > 10:
            imposed_penalty = True
        else:
            imposed_penalty = False


#Validate the speed differences and equate it the correct amount of demerit points. 
    if acceleration_difference <= 0:
        demerit_points = 0

    elif acceleration_difference > 0 and acceleration_difference <= 10:
        demerit_points = 10

    elif acceleration_difference > 10 and acceleration_difference <= 20:
        demerit_points = 20

    elif acceleration_difference > 20 and acceleration_difference <= 30:
        demerit_points = 35

    elif acceleration_difference > 30 and acceleration_difference <= 35:
        demerit_points = 40

    else:
        demerit_points = 50

#Return mandatory penalty and penalty points
    return (imposed_penalty, demerit_points)


def reset_gui():
    """ Reset's all functions back to initial configuration """

    #Variables and how to reset them
    tow_opt.set(0)
    school_opt.set(0)
    holiday_opt.set(0)
    speed_value.set('50')
    driving_speed_entry.delete(0, END)
    msg_label.config(text = '')
    return None

def calculate_points():
    """ Handles the calculation and outputs appropriate information """

    #Variables and appropriate commands
    d_speed = driving_speed_entry.get()
    selection = speed_value.get()
    tow_trailer = tow_opt.get()
    in_school_zone = school_opt.get()
    during_holiday_period = holiday_opt.get()

    #Validate if entry box is empty or not and returns a message
    if len(d_speed) == 0:
        msg_label.config(text = "Please enter a driving speed.")
        return None
            
    elif not d_speed.replace('.','').isdigit():
        msg_label.config(text = "The driving speed needs to be numeric.")
        return None
        

    else:
        #Call get_demerit_points, calculate if a ticket is needed and its appropriate penalty points
        d_speed = eval(d_speed)
        demerit_points = get_demerit_points(d_speed, selection, tow_trailer, in_school_zone, during_holiday_period)
        msg_label.config(text = demerit_points)
        gets_ticket = demerit_points[0]
        penalty_points = demerit_points[1]


        if gets_ticket:
            msg_label.config(text = f"The mandatory penalty for driving at \n{d_speed}km/h in a {selection}km/h zone is {penalty_points} points.")
            return None

        elif gets_ticket is False and penalty_points > 0:
            msg_label.config(text = f"The discretional penalty for driving at \n{d_speed}km/h in a {selection}km/h zone is {penalty_points} points.")
            return None
            
        else:
            msg_label.config(text = f"{d_speed}km/h in a {selection}km/h zone is not speeding.")
            return None
                   
        


def exit_handler():
    """ Function for exit button in the menu """
    
    if askyesno('Demerit points calculator', 'Do you want to exit?'):
        root_window.destroy()
    speed_value.set(0)
    return None



def display_help_display(ver):
    """ Display typical help display instructions """
    
    showinfo('Demerit points calculator', f'{ver}')
    return None

def display_help_about(ver):
    """ Display about information from the menu """
    
    showinfo('Demerit points calculator', f'Version {ver}')
    return None




MAX_TEXT_ENTRY_WIDTH = 10
DISPLAY_INSTRUCTION = 'Enter the driving speed.\nSelect the speed limit.\nSelect trailer/school holiday situation.\nClick calculate points.\nClick Reset to reset the values.'
VERSION = '1.0\nWritten by: Mark Reyes.'

#Window size and title
root_window  = Tk()
root_window.title("Demerit points calculator")
root_window.geometry("400x175")

# Create vars for handling the text that is entered into the boxes.
tow_opt = IntVar()
school_opt = IntVar()
holiday_opt = IntVar()
max_speed = StringVar()
speed_value = IntVar(None, '50')

# Driving speed frame
driving_speed_frame = Frame(root_window)
driving_speed_frame.pack(anchor=W)
driving_speed_label = Label(driving_speed_frame, text = 'Driving speed')
driving_speed_label.pack(side=LEFT)
driving_speed_entry = Entry(driving_speed_frame) #textvariable = driving_speed)
driving_speed_entry.pack(side=LEFT)

# Speed limit frame
max_speed_frame = Frame(root_window)
max_speed_frame.pack(anchor=W)
max_speed_label = Label(max_speed_frame, text = 'Speed limit:')
max_speed_label.pack(side=LEFT)


#Max speed buttons
low_km_button = Radiobutton(max_speed_frame, text='30km/h', variable = speed_value, value = 30)
low_km_button.pack(side=LEFT, padx=10)
mid_km_button = Radiobutton(max_speed_frame, text='50km/h', variable = speed_value, value = 50)
mid_km_button.pack(side=LEFT)
high_km_button = Radiobutton(max_speed_frame, text='100km/h', variable = speed_value, value = 100)
high_km_button.pack(side=LEFT)


#Towing, school zone, holiday period frame
tick_boxes_frame = Frame(root_window)
tick_boxes_frame.pack()

towing_trailer_tick = Checkbutton(tick_boxes_frame, text='Towing light trailer', onvalue = True, offvalue = False, variable = tow_opt)
towing_trailer_tick.pack(side=LEFT)

school_zone_tick = Checkbutton(tick_boxes_frame, text='In school zone', onvalue = True, offvalue = False, variable = school_opt)
school_zone_tick.pack(side=LEFT)

holiday_period_tick = Checkbutton(tick_boxes_frame, text='Holiday period', onvalue = True, offvalue = False, variable = holiday_opt)
holiday_period_tick.pack(side=LEFT)

# Calculate points and reset
calculate_button_frame = Frame(root_window)
calculate_button_frame.pack()
calculate_button = Button(calculate_button_frame, text = 'Calculate points', command = calculate_points) 
calculate_button.pack(side=LEFT) 
reset_button = Button(calculate_button_frame, text = 'Reset', command = reset_gui) 
reset_button.pack(padx=20) 

msg_label = Label(root_window)
msg_label.pack(side = BOTTOM)



# Build the menus
menubar = Menu(root_window)

# Add the speed menus
speed_menu = Menu(menubar, tearoff = 0)
speed_menu.add_command(label = "Calculate points", command = calculate_points)
speed_menu.add_command(label = "Reset", command = reset_gui)
speed_menu.add_command(label = "Exit", command = exit_handler)
menubar.add_cascade(label="Speed", menu = speed_menu)

# Add the Help menus
help_menu = Menu(menubar, tearoff = 0)
help_menu.add_command(label="Display instructions", command = lambda: display_help_display(DISPLAY_INSTRUCTION))
help_menu.add_command(label="About", command = lambda: display_help_about(VERSION))
menubar.add_cascade(label="Help", menu = help_menu)

# Add all the menu's to the window
root_window.config(menu = menubar)




msg_label = Label(root_window)
msg_label.pack(side = BOTTOM )

root_window.resizable(False, False)

root_window.mainloop()
