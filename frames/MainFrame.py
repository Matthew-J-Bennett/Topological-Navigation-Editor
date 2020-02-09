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

        swap_frame_tmp = elements.Button(master=master.master, x=10, y=750, text="Swap Frame to Launch Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.LaunchFrame(
                                                                                           master=self.master)))
        # This block imports the pgm file.
        img = PhotoImage(file="tempDir/test.pgm")
        canvas = Canvas(self.window, width=1250, height=800, scrollregion=(0, 0, 1583, 1806))
        canvas.pack(expand=YES, fill=BOTH)
        canvas.create_image(10, 20, anchor=NW, image=img)

        scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview, jump=1)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=canvas.xview)
        canvas.config(xscrollcommand=scroll_x.set)

        scroll_y = Scrollbar(canvas, orient="vertical", command=canvas.yview, jump=1)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=canvas.yview)
        canvas.config(yscrollcommand=scroll_y.set)

        mainloop()
