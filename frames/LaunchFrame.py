import os
import tkinter as tk
from pathlib import Path
from shutil import copy2
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename

import yaml

import contants as const
import elements
import frames


class LaunchFrame:

    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        self.frame = elements.Frame(master=self.window)

        label = elements.Photo(master=master.master, x=100, y=150, imgpath="test.png", height=450, width=300,
                               relief=tk.RIDGE, bd=3)
        swap_frame_tmp = elements.Button(master=master.master, x=10, y=750, text="Swap Frame to Main Project Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.MainFrame(
                                                                                           master=self.master)))

        title_label = elements.Label(master=master.master, text="Topological-Navigation-Editor", x=625, y=50,
                                     font=("Verdana", 44),
                                     fg='white', anchor=tk.CENTER)
        import_button = elements.Button(master=master.master, x=800, y=650, text="Import Files", width=20,
                                        func=lambda: self.getimportfilename())

        open_button = elements.Button(master=master.master, x=1000, y=650, text="Open Files", width=20,
                                      func=lambda: messagebox.showinfo("Title", "a box"))

        recent_files_frame = elements.Frame(master=master.master, x=750, y=150, height=450, width=450,
                                            bg=const.tertiary_colour,
                                            relief=tk.RIDGE, bd=3)

        temp_recent_files_text = elements.Label(master=master.master, text="Here is where Recent Files will go", x=755,
                                                y=160, font=("Verdana", 14), fg='white', bg=const.tertiary_colour)

        temp_save_button = elements.Button(master=master.master, x=10, y=90, text="Save Files", width=20,
                                           func=lambda: self.savefilename())
        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    def getimportfilename(self):
        dirName = 'tempDir'
        try:
            os.mkdir(dirName)
            self.logging.info("Directory {} Created".format(dirName))
        except FileExistsError:
            self.logging.info("Directory {} already exists".format(dirName))

        self.master.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                            filetypes=(
                                                                ("Map files", ".yaml .pgm .tmap"),
                                                                ("All files", "*.*")))

        if self.setfilenames() == 1:
            self.readyaml()
            self.readpgm()

    def savefilename(self):
        files2 = [('TMAP Files', '*.*')]
        file = asksaveasfilename(filetypes=files2, defaultextension='.tmap')
        copy2(self.master.files[1], file)

    def setfilenames(self):
        self.master.files = ["", "", ""]
        numfiles = 0
        for x in self.master.filenames:
            if Path(x).suffix == ".pgm" and self.master.files[0] == "":
                self.master.files[0] = x
                self.logging.info("PGM file imported: ".format(x))
                copy2(self.master.files[0], 'tempDir')
                self.logging.info("PGM file saved to temporary directory.")
                numfiles += 1
            elif Path(x).suffix == ".tmap" and self.master.files[1] == "":
                self.master.files[1] = x
                self.logging.info("TMAP file imported: {}".format(x))
                copy2(self.master.files[1], 'tempDir')
                self.logging.info("TMAP file saved to temporary directory.")
                numfiles += 1
            elif Path(x).suffix == ".yaml" and self.master.files[2] == "":
                self.master.files[2] = x
                self.logging.info("YAML file imported: {}".format(x))
                copy2(self.master.files[2], 'tempDir')
                self.logging.info("YAML file saved to temporary directory.")
                numfiles += 1
            else:
                self.logging.info("Invalid file type selected: {}".format(x))
        if numfiles != 3:
            self.logging.info("Not all files selected. Please select again.")
            return 0
        else:
            return 1

    def readyaml(self):
        with open(self.master.files[2]) as file:
            self.master.yamldata = yaml.load(file, Loader=yaml.FullLoader)
            self.logging.info(self.master.yamldata)

    # needs a def readtmap() function here

    def readtmap(self):
        with open(self.master.files[1]) as file:
            self.master.tmapdata = yaml.load(file, Loader=yaml.FullLoader)
            print(self.master.tmapdata)

    # This is my attempt as replicating the readtmap and readyaml functions

    def readpgm(self):
        image = open(self.master.files[0], 'r')
        x = 0
        while x < 4:
            line = image.readline()
            if x == 0:
                id = line
            if x == 2:
                size = line.split()
                pgmX = size[0]
                pgmY = size[1]
            if x == 3:
                maxval = line
            x += 1
        self.master.pgm = pgm(id, pgmX, pgmY, maxval)


class pgm():
    def __init__(self, id, width, height, maxval):
        self.id = id
        self.width = width
        self.height = height
        self.maxval = maxval
