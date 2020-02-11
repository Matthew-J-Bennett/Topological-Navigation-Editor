import frames
import elements
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk


class MainFrame:
    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        self.frame = elements.Frame(master=self.window)

        # Creates a button to switch between frames
        swap_frame_tmp = elements.Button(master=master.master, x=10, y=750, text="Swap Frame to Launch Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.LaunchFrame(
                                                                                           master=self.master)))
        # This block imports the pgm file.
        # Sets a variable for the background image
        img = PhotoImage(file=self.master.files[0])
        # Creates a canvas and sets the size of the canvas - NEED TO USE IMAGE VARIABLE WIDTHS
        canvas = Canvas(self.window, width=1250, height=800, scrollregion=(0, 0, 1583, 1806))
        canvas.pack(expand=YES, fill=BOTH)
        # Adds the image to the canvas
        canvas.create_image(10, 20, anchor=NW, image=img)

        # Creates a horizontal scrollbar
        scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview, jump=1)
        # Sets the location of the scroll bar
        scroll_x.pack(side=BOTTOM, fill=X)
        # Defines what the scroll bar will do
        scroll_x.config(command=canvas.xview)
        canvas.config(xscrollcommand=scroll_x.set)

        # Creates a vertical scrollbar
        scroll_y = Scrollbar(canvas, orient="vertical", command=canvas.yview, jump=1)
        # Sets the location of the scroll bar
        scroll_y.pack(side=RIGHT, fill=Y)
        # Defines what the scroll bar will do
        scroll_y.config(command=canvas.yview)
        canvas.config(yscrollcommand=scroll_y.set)

        mainloop()
