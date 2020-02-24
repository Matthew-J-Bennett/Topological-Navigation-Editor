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
        # Creates a imgcanvas and sets the size of the imgcanvas - NEED TO USE IMAGE VARIABLE WIDTHS
        imgcanvas = Canvas(self.window, width=850, height=800, scrollregion=(0, 0, 1583, 1806))
        imgcanvas.pack(expand=YES, side=tk.LEFT, fill=BOTH)
        # Adds the image to the imgcanvas
        imgcanvas.create_image(10, 20, anchor=NW, image=img)

        # Creates the Properties Canvas
        propcanvas = Canvas(self.window, width=400, height=800)
        propcanvas.pack(expand=NO, side=tk.RIGHT, fill=BOTH)

        # Populates text Labels
        tk.Label(propcanvas, text="Node Properties").grid(row=0)
        tk.Label(propcanvas, text="Node Name").grid(row=1)
        tk.Label(propcanvas, text="Action").grid(row=2)
        tk.Label(propcanvas, text="Edge ID").grid(row=3)
        tk.Label(propcanvas, text="Inflation Radius").grid(row=4)
        tk.Label(propcanvas, text="Map").grid(row=5)
        tk.Label(propcanvas, text="Node").grid(row=6)
        tk.Label(propcanvas, text="Top Velocity").grid(row=7)

        # Populates entry boxes
        name = tk.Entry(propcanvas)
        action = tk.Entry(propcanvas)
        edge_id = tk.Entry(propcanvas)
        inflation_radius = tk.Entry(propcanvas)
        map_2d = tk.Entry(propcanvas)
        node = tk.Entry(propcanvas)
        top_vel = tk.Entry(propcanvas)

        name.grid(row=1, column=1)
        action.grid(row=2, column=1)
        edge_id.grid(row=3, column=1)
        inflation_radius.grid(row=4, column=1)
        map_2d.grid(row=5, column=1)
        node.grid(row=6, column=1)
        top_vel.grid(row=7, column=1)

        # Creates a horizontal scrollbar
        scroll_x = Scrollbar(imgcanvas, orient="horizontal", command=imgcanvas.xview, jump=1)
        # Sets the location of the scroll bar
        scroll_x.pack(side=BOTTOM, fill=X)
        # Defines what the scroll bar will do
        scroll_x.config(command=imgcanvas.xview)
        imgcanvas.config(xscrollcommand=scroll_x.set)

        # Creates a vertical scrollbar
        scroll_y = Scrollbar(imgcanvas, orient="vertical", command=imgcanvas.yview, jump=1)
        # Sets the location of the scroll bar
        scroll_y.pack(side=RIGHT, fill=Y)
        # Defines what the scroll bar will do
        scroll_y.config(command=imgcanvas.yview)
        imgcanvas.config(yscrollcommand=scroll_y.set)

        mainloop()
