"""
Real-time Canteen Information System
Written by Bryan Lim, Bian Hengwei, Cheng Yu Feng
Functions that builds the graphical user interface
Built with Tkinter
"""

# import tkinter for GUI
from tkinter import *

# file that processes all the data
from Canteen_Info_Sys import *


# initializes data
# images MUST be initialized in the main() function
# which calls initialize(data) in the main file
def initialize(data):

    # opens the cover image
    data.cover = PhotoImage(file='images/cover.png')

    # check if list of stalls name is available
    data.stalls_list = get_stalls()
    if isinstance(data.stalls_list, str):
        error_page(data.stalls_list)

    # try to initialize all backgrounds
    data.backgrounds = []
    for stall_name in data.stalls_list:
        try:
            data.backgrounds.append(PhotoImage(file='images/' + stall_name + '.png'))
        # if there is no background available use the default one
        except TclError:
            data.backgrounds.append(PhotoImage(file='images/cover.png'))

    # set time to current time
    data.time = Time()
    data.time.get_current_time()

    # a stall object that keep track of information in current selected stalls
    # initially set to None
    data.current_stall = None


# draws the cover
def cover(root, data):

    # clears the root
    for canvas in root.winfo_children():
        canvas.destroy()

    # creates a new canvas for the cover page
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(highlightthickness=0)
    canvas.pack()

    # draws a background image
    canvas.create_image(data.width // 2, data.height // 2, image=data.cover)

    # shows current time
    canvas.create_text(data.width // 2, data.height * 9 // 10, text=str(data.time),
                       font='Times 25 bold', fill='white')

    # title text
    canvas.create_text(data.width // 4, data.height // 2 - 20, text='North Spine\nCanteen\nInformation\nSystem',
                       font='Noteworthy 60 bold italic', fill='white', justify='center')

    # a button that directs to the select store window
    select_stall_button = Button(canvas, text='SELECT\nSTORE', font='Times 30 bold',
                                 command=lambda: change_date(root, data))
    select_stall_button.place(x=data.width * 3 // 4, y=data.height // 3 - 20,
                              width=300, height=120, anchor=CENTER)

    # exit button
    Button(canvas, text='Exit', font='Times 30 bold',
           command=root.destroy).place(x=data.width * 3 // 4,
                                       y=data.height * 2 // 3 - 20, width=300, height=120, anchor=CENTER)

    # draws the drop down lists that allows user to set a different time
    draw_change_date(root, canvas, data)


# draws change date buttons and drop-down lists on cover
def draw_change_date(root, canvas, data):

    # a constant for drop-down list
    margin = 55

    # date drop-down list
    dates_list = ['0' + str(x) for x in range(1, 10)] + [str(x) for x in range(10, 32)]

    date_variable = StringVar(root)
    date_variable.set(str(data.time)[5:7])  # default value

    date_drop_down_list = OptionMenu(root, date_variable, *dates_list)
    date_drop_down_list.place(x=605, y=data.height // 2 - 7, width=margin, anchor=SW)

    # month drop-down list
    months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    month_variable = StringVar(root)
    month_variable.set(str(data.time)[8:11])  # default value

    month_drop_down_list = OptionMenu(root, month_variable, *months_list)
    month_drop_down_list.place(x=605 + margin, y=data.height // 2 - 7, width=margin, anchor=SW)

    # year drop-down list
    years_list = [str(x) for x in range(2000, 2030)]

    year_variable = StringVar(root)
    year_variable.set(str(data.time)[12:16])  # default value

    year_drop_down_list = OptionMenu(root, year_variable, *years_list)
    year_drop_down_list.place(x=605 + 2 * margin, y=data.height // 2 - 7, width=margin + 15, anchor=SW)

    # hour drop-down list
    hours_list = ['0' + str(x) for x in range(10)] + [str(x) for x in range(10, 24)]

    hour_variable = StringVar(root)
    hour_variable.set(str(data.time)[18:20])  # default value

    hour_drop_down_list = OptionMenu(root, hour_variable, *hours_list)
    hour_drop_down_list.place(x=605 + 3 * margin + 15, y=data.height // 2 - 7, width=margin, anchor=SW)

    # minute drop-down list
    minutes_list = ['0' + str(x) for x in range(10)] + [str(x) for x in range(10, 60)]

    minute_variable = StringVar(root)
    minute_variable.set(str(data.time)[21:23])  # default value

    minute_drop_down_list = OptionMenu(root, minute_variable, *minutes_list)
    minute_drop_down_list.place(x=605 + 4 * margin + 15, y=data.height // 2 - 7, width=margin, anchor=SW)

    # get all the above drop-down list value
    def get_var():

        # get values from StringVars
        date_str = date_variable.get()
        month_str = month_variable.get()
        year_str = year_variable.get()
        hour_str = hour_variable.get()
        minute_str = minute_variable.get()

        # call change_date wrapper with the user inputs
        new_time = date_str, month_str, year_str, hour_str, minute_str
        change_date(root, data, new_time)

    # Change date button
    change_date_button = Button(canvas, font='Times 30 bold', text="VIEW STORE BY:\n\nEnter",
                                command=get_var)
    change_date_button.place(x=data.width * 3 // 4, y=data.height // 2 - 20, width=300, height=120, anchor=CENTER)


# changes current date
def change_date(root, data, new_time=('reset',)):

    # calls the change_date function of the time object
    # calls select_stall page
    error_message = data.time.change_date(new_time)
    if error_message is not None:
        error_page(error_message)
        return
    select_stall(root, data)


# pops up an error page
def error_page(error_message='Unexpected Error'):

    # creates a new pop up error window
    window = Tk()
    window.title('ERROR')
    error_label = Label(window, text=error_message)
    error_label.pack()
    window.mainloop()


# draws a canvas that shows the stalls list
def select_stall(root, data):

    # clears the root
    for canvas in root.winfo_children():
        canvas.destroy()

    # creates a new canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(highlightthickness=0)
    canvas.pack()

    # draws a background image
    canvas.create_image(data.width // 2, data.height // 2, image=data.cover)

    # a back button
    back_button = Button(canvas, text='BACK', font='Times 30 bold', command=lambda: cover(root, data))
    back_button.place(x=0, y=data.height, width=100, height=80, anchor=SW)

    # shows current time
    canvas.create_text(data.width // 2, data.height * 9 // 10, text=str(data.time),
                       font='Times 25 bold', fill='white')

    # reads the open stalls list
    stalls_list = list()
    for stall in data.stalls_list:
        if data.time in Stall(stall).hours:
            stalls_list.append(stall)
    stalls_count = len(stalls_list)

    # check if no stall is open
    # show message and stop drawing this frame
    if stalls_count == 0:
        canvas.create_text(data.width // 2, data.height // 2, text='Canteen Closed', font='Arial 50', fill='white')
        return

    # builds the buttons
    # initialize button constants
    margin_height = data.height // (stalls_count * 2 + 1)
    button_height = min(margin_height * 2, 400)
    margin_width = data.width // 7
    button_width = margin_width * 2

    # draws and places the buttons
    # auto adjust the size according to number of stalls available
    for stall_name in stalls_list:
        stall_index = stalls_list.index(stall_name)
        if stall_index >= stalls_count // 2:
            x = margin_width * 2 + button_width
            y_index = stall_index - stalls_count // 2
        else:
            x = margin_width
            y_index = stall_index
        y = (y_index + 1) * margin_height + y_index * button_height
        stall = Button(canvas, text=stall_name, font='Times 25 bold',
                       command=lambda name=stall_name: go_to_stall(root, data, name))
        stall.place(x=x, y=y + 40, width=button_width, height=button_height, anchor=NW)


# change data.current_stall
def go_to_stall(root, data, stall_name):

    # calls the current_stall method
    # calls operating hours page as default
    data.current_stall = Stall(stall_name)
    operating_hours(root, data)


# display the basic stall window
# called by specific stall functions
def display_stall(root, data):

    # clears the root
    for canvas in root.winfo_children():
        canvas.destroy()

    # creates a new canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(highlightthickness=0)
    canvas.pack()

    # give a background for store
    stall_index = data.stalls_list.index(data.current_stall.name)
    canvas.create_image(data.width // 2, data.height // 2, image=data.backgrounds[stall_index])

    # menu button
    menu_button = Button(canvas, text='Menu', font='Times 20',
                         command=lambda: menu(root, data))
    menu_button.place(x=data.width // 3, y=data.height // 15 + 30, width=data.width // 10,
                      height=data.height // 15, anchor=CENTER)
    # queue time button
    queue_time_button = Button(canvas, text='Queue\nTime', font='Times 20',
                               command=lambda: queue_time(root, data))
    queue_time_button.place(x=data.width // 2, y=data.height // 15 + 30, width=data.width // 10,
                            height=data.height // 15, anchor=CENTER)
    # operating hours button
    operating_hours_button = Button(canvas, text='Operating\nHours',
                                    font='Times 20',
                                    command=lambda:operating_hours(root, data))
    operating_hours_button.place(x=data.width * 2 // 3, y=data.height // 15 + 30, width=data.width // 10,
                                 height=data.height // 15, anchor=CENTER)

    # stall name
    canvas.create_text(data.width // 2, data.height // 7 + 50,
                       text=data.current_stall.name, font='Impact 60', fill='white')

    # a back button
    back_button = Button(canvas, text='BACK', font='Times 30 bold', command=lambda: select_stall(root, data))
    back_button.place(x=0, y=data.height, width=100, height=80, anchor=SW)

    return canvas


# display the menu of any specific stall
def menu(root, data):

    # draws the shared stall window
    canvas = display_stall(root, data)

    # prints stalls menu
    x_base, y_base, margin = 220, 270, 50
    counter = 0
    for dish in data.current_stall.menu:
        if data.time in data.current_stall.menu[dish][1]:
            # prints dish name and price separately
            canvas.create_text(x_base, y_base + counter * margin, text=dish, anchor=W, font='Arial 30', fill='white')
            canvas.create_text(data.width - x_base, y_base + counter * margin, text=data.current_stall.menu[dish][0],
                               anchor=W, font='Arial 30', fill='white')
            counter += 1


# allows calculation for queue time
# takes in any user input and shows queue time
def queue_time(root, data):

    # draws the shared window
    canvas = display_stall(root, data)

    # function for showing queue time
    def show_queue_time():

        # delete the last text if there is one
        canvas.delete('queue_time')

        # get the value from the entry below
        queue_length = queue_enter.get()

        try:

            # calculate the queue time
            queue = int(queue_length)

            # check if the number is valid
            assert 0 <= queue < 100
            waiting_time = str(int(queue * data.current_stall.queue))

            # create text to show the queuing time message
            show_var = 'Estimated queuing time is: ' + waiting_time + ' minutes'
            canvas.create_text(data.width // 2, data.height * 2 // 3 - 20, text=show_var, font='Arial 35',
                               fill='white', tag='queue_time')

        # if the user input is not valid
        except AssertionError:

            # create a pop up window for error message
            error_page('Queue Length Should Be Between 1 and 99!')

        # if the user input is not an integer
        except ValueError:

            # create a pop up window for error message
            error_page('Please Enter An Integer')

    # show_queue_time wrapper
    def show_queue_time_wrapper(event):

        # show queue time if 'Return' is pressed
        if event.keysym == 'Return':
            show_queue_time()

    # asks for user input
    canvas.create_text(data.width // 2, data.height // 3 + 40, text='Please Enter The Number of Pax Queuing:'
                       , font='Arial 35', fill='white')

    # the entry for the number of queuing people
    queue_enter = Entry(root, font='Arial 30', width=15)
    queue_enter.place(x=data.width // 2 - 70, y=data.height // 2 + 10, anchor=CENTER)

    # a button for calculate the time
    calculate_btn = Button(root, text='Calculate', width=9, height=2, command=show_queue_time,
                           font='Arial 19')
    calculate_btn.place(x=data.width // 2 + 115, y=data.height // 2 + 10, anchor=CENTER)

    # bind ENTER button to call show_queue_time
    root.bind('<KeyPress>', lambda event: show_queue_time_wrapper(event))


# shows the operating hours of any stall
def operating_hours(root, data):

    # draws the window
    canvas = display_stall(root, data)

    # display operating hour
    canvas.create_text(data.width // 2, 300, text='Operating Hour', font='Arial 45', fill='white')
    canvas.create_text((data.width // 2, 410), text=str(data.current_stall.hours),
                       anchor=CENTER, font='Arial 45', fill='white')
