"""
Real-time Canteen Information System
Written by Bryan Lim, Bian Hengwei, Cheng Yu Feng
Main file that runs the whole app
"""

# import GUI and runs
from Canteen_Info_Sys_GUI import *


# main func that runs the whole app
def main(width=1000, height=800):

    # creates a root obj and its canvas
    root = Tk()
    root.title('North Spine Canteen Information System')
    root.geometry(str(width) + 'x' + str(height))
    root.resizable(False, False)

    # an object that stores images
    class Struct:
        pass

    data = Struct()
    initialize(data)
    data.width, data.height = width, height

    # draws the cover
    cover(root, data)

    # launches the app and block until window is closed
    root.mainloop()


# runs the app
if __name__ == '__main__':
    main()
