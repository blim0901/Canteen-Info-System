"""
Real-time Canteen Information System
Written by Bryan Lim, Bian Hengwei, Cheng Yu Feng
Basic algorithms that reads connects data files to GUI
"""

# import python build-in time
from datetime import *


# returns the stalls list stored in stalls_list.txt
def get_stalls():

    # opens the stalls list
    # prints an error message if the file is not found
    try:
        stalls_list_file = open('data/stalls_list.txt', 'rt')

    except FileNotFoundError:
        return 'Cannot Find Stalls List'

    # reads the file and convert it into a list object
    # returns the list
    stalls_list_text = stalls_list_file.read()
    stalls_list = stalls_list_text.splitlines()
    return stalls_list


# return the information of a specific store
def get_info(stall_name):

    # opens the info file
    # prints an error message if the file is not found
    try:
        filename = 'data/' + stall_name + '.txt'
        info_file = open(filename, 'rt')
    except FileNotFoundError:
        return 'Cannot find the info file'

    # reads the file and convert it into a list object
    info_text = info_file.read()
    info_list = info_text.splitlines()

    # info_list[0] is the operating hours
    # info_list[1] is the queue factor
    # info_list[2:] is the menu data
    # return a tuple of the above mentioned information
    return info_list[0], info_list[1], info_list[2:]


# class Time that records the time
class Time:

    # initialize an empty Time object
    def __init__(self):

        # time values
        self.day_of_week = None
        self.date = None
        self.month = None
        self.year = None
        self.hour = None
        self.minute = None

        # allows conversion between string and index
        self.months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # set the time instances to current time value
    def get_current_time(self):

        # set time to current time with datetime.now
        self.day_of_week = datetime.now().weekday()
        self.date = datetime.now().strftime('%d')
        self.month = datetime.now().strftime('%m')
        self.year = datetime.now().strftime('%Y')
        self.hour = datetime.now().strftime('%H')
        self.minute = datetime.now().strftime('%M')

    # return a string representation of any Time object
    # allows str(self)
    def __repr__(self):

        # creates a string representation of the time object
        time_string = ''
        time_string += self.days_of_week[self.day_of_week] + ', '
        time_string += self.date + ' ' + self.months[int(self.month)]
        time_string += ' ' + self.year + ', ' + self.hour + ':' + self.minute

        # returns the result string
        return time_string

    # reads a string representation of time and set the time data to the object
    def change_date(self, new_time):

        # check if new_time is the default value
        # set time to now
        if new_time == ('reset',):
            self.get_current_time()
            return

        # else set time according to new_time
        self.date = new_time[0]
        self.month = str(self.months.index(new_time[1]))
        self.year = new_time[2]
        self.hour = new_time[3]
        self.minute = new_time[4]
        try:
            self.day_of_week = datetime(int(self.year), int(self.month), int(self.date)).weekday()
        except ValueError:
            return 'Invalid Date'


# class period that represents a time period
class Period:

    # initializes an period with a given string
    # string format: days of the week|start-end
    # string example: 'Mon,Tue,Wed,Thu,Fri,Sat|08:30-20:30'
    def __init__(self, period_string):

        # split string
        # set the period values
        days_of_week_string, hours = period_string.split('|')
        self.days_of_week = days_of_week_string.split(',')
        self.start_hour = hours[0:2]
        self.start_minute = hours[3:5]
        self.end_hour = hours[6:8]
        self.end_minute = hours[9:11]

    # returns a string representation of the period object
    # allows str(self)
    def __repr__(self):

        # check if we can shorten the day_of_week list
        string_representation = ''
        if self.days_of_week == ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
            string_representation += 'Weekdays'
        elif len(self.days_of_week) == 7:
            pass
        else:
            for days_of_week_string in self.days_of_week:
                string_representation += days_of_week_string + ', '
            string_representation = string_representation[:-1]

        # creates the string representation of the period object
        string_representation += ' ' + self.start_hour + ':' + self.start_minute + ' - ' + self.end_hour + \
                                 ':' + self.end_minute

        # returns the string representation
        return string_representation

    # check if a certain time is in the period
    def __contains__(self, time_item):

        # checks day_of_week
        if not time_item.days_of_week[time_item.day_of_week] in self.days_of_week:
            return False
        # checks start time
        elif not (self.start_hour < time_item.hour or (self.start_hour == time_item.hour and
                                                       self.start_minute <= time_item.minute)):
            return False
        # checks end time
        elif not (self.end_hour > time_item.hour or (self.end_hour == time_item.hour and
                                                     self.end_minute > time_item.minute)):
            return False

        # returns true if passes all if statements
        return True


# stall class that represents a stall
class Stall:

    # initialize the stall according to its name
    def __init__(self, stall_name):

        # store name
        self.name = stall_name

        # reads file with the function written above
        # sets the data
        hours_string, queue_string, menu_list = get_info(stall_name)
        self.hours = Period(hours_string)
        self.queue = float(queue_string)

        # sets the menu dictionary
        self.menu = dict()
        self.build_menu(menu_list)

    # builds the menu variable
    def build_menu(self, menu_list):

        # split according to format
        # dish name&price&period
        for menu in menu_list:
            dish = menu.split('&')
            price = dish[1]
            # check if is available at all times
            if dish[2] == 'ALL':
                hours = self.hours
            else:
                hours = Period(dish[2])

            # append to dictionary
            self.menu[dish[0]] = price, hours
