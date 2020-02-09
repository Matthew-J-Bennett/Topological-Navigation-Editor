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

        # active_files_canvas = elements.Canvas(master=master.master,width = 200, height = 200)
        # active_files_canvas.pack()
        canvas = Canvas(self.window, width=1250, height=800)
        canvas.pack()
        img = PhotoImage(file="tempDir/test.pgm")
        canvas.create_image(10, 20, anchor=NW, image=img)

        scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview)
        scroll_x.grid(row=1, column=1, sticky="ew")

        scroll_y = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        canvas.configure(scrollregion=canvas.bbox("all"))
        mainloop()

        # canvas = Canvas(self.window, width=1250, height=800, scrollregion=(0, 0, 500, 500))
        # canvas.pack()
        # img = PhotoImage(file="tempDir/test.pgm")
        # canvas.create_image(20, 20, anchor=NW, image=img)
        # mainloop()
