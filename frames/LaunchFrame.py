import os
import tkinter as tk
from pathlib import Path
from shutil import copy2
from tkinter import filedialog, messagebox
import tmap
import yaml
import contants as const
import elements
import frames
import json
import random


class LaunchFrame:

    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master

        # Creates the launch frame
        self.frame = elements.Frame(master=self.window)

        # Adds Decorative Image
        label = elements.Photo(master=master.master, x=100, y=150, imgpath="logo.png", height=200, width=200,
                               relief=tk.RIDGE, bd=3)
        # Creates a button to swap between frames
        swap_frame_tmp = elements.Button(master=master.master, x=10, y=750, text="Swap Frame to Main Project Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.MainFrame(
                                                                                           master=self.master)))
        # Adds a title to the top of the screen
        title_label = elements.Label(master=master.master, text="Topological-Navigation-Editor", x=625, y=50,
                                     font=("Comic Sans MS", 44),
                                     fg='white', anchor=tk.CENTER)
        # Import files button
        import_button = elements.Button(master=master.master, x=800, y=650, text="Import Files", width=20,
                                        func=lambda: self.getimportfilename())
        # Open files button - To be considered
        open_button = elements.Button(master=master.master, x=1000, y=650, text="Open Files", width=20,
                                      func=lambda: messagebox.showinfo("Title", "a box"))
        # Creates a frame to display recent files
        recent_files_frame = elements.Frame(master=master.master, x=750, y=150, height=450, width=450,
                                            bg=const.tertiary_colour,
                                            relief=tk.RIDGE, bd=3)
        # Placeholder text
        temp_recent_files_text = elements.Label(master=master.master, text="Here is where Recent Files will go", x=755,
                                                y=160, font=("Comic Sans MS", 14), fg='white', bg=const.tertiary_colour)
        # Placeholder Button
        temp_save_button = elements.Button(master=master.master, x=10, y=90, text="Save Files", width=20,
                                           func=lambda: self.savefilename())
        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    # Import Files function
    def getimportfilename(self):
        # Produces a Dialog window to allow the user to select files
        self.master.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                            filetypes=(
                                                                ("Map files", ".yaml .pgm .tmap"),
                                                                ("All files", "*.*")))

        # File Validation/Duplication
        if self.setfilenames() == 1:
            self.readtmap()
            self.readyaml()
            self.readpgm()
            data = self.master.tmapdata
            data = tmap.addAction(data, "WayPoint10", "WayPoint20")
            data = tmap.deleteAction(data, "WayPoint10", "WayPoint20")
            orientation = [0.5, 0.6, 0.7, 0.8]
            position = [24, 43, 2.1]
            verts = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9]]
            tmap.printNodeNames(data)
            tmap.addNode(data, "riseholme", "WayPoint225", "riseholme", orientation, position, verts)
            tmap.printNodeNames(data)
            tmap.deleteNode(data, "WayPoint225")
            tmap.printNodeNames(data)

        if len(self.master.filenames) == 3:
            self.master.frame_swap(old_frame=self.frame,
                                   new_frame=lambda: frames.MainFrame(
                                       master=self.master))

    def savefilename(self):
        files2 = [('TMAP Files', '*.*')]
        file = filedialog.asksaveasfilename(filetypes=files2, defaultextension='.tmap')
        copy2(self.master.files["tmap"], file)

    # Ensures that Files have been imported successfully
    def setfilenames(self):
        # Creates an array to store file names
        self.master.files = {}
        numfiles = 0
        # Compares a file to ensure that it is correct
        for x in self.master.filenames:
            # Checks the suffix
            if Path(x).suffix == ".pgm":
                self.master.files["pgm"] = x
                # Logs a file has been imported
                self.logging.info("PGM file imported: ".format(x))
                # Adds to the file counter
                numfiles += 1
            elif Path(x).suffix == ".tmap":
                self.master.files["tmap"] = x
                self.logging.info("TMAP file imported: {}".format(x))
                numfiles += 1
            elif Path(x).suffix == ".yaml":
                self.master.files["yaml"] = x
                self.logging.info("YAML file imported: {}".format(x))
                numfiles += 1
            else:
                self.logging.info("Invalid file type selected: {}".format(x))
        # If not enough files are provided then it will fail
        if numfiles != 3:
            self.logging.info("Not all files selected. Please select again.")
            return 0
        # If successful - then return TRUE condition
        else:
            self.logging.debug(self.master.files)
            filelocdict = {
                "name": random.randint(1245, 99999),
                "files": self.master.files
            }

            if not os.path.exists("data/"):
                os.mkdir("data/")

            with open('data/RecentProjects.json', 'w') as fp:
                json.dump(filelocdict, fp, indent=2)
            return 1

    # Reads in and stores the data of the YAML file
    def readyaml(self):
        with open(self.master.files["yaml"]) as file:
            self.master.yamldata = yaml.load(file, Loader=yaml.FullLoader)

    # Reads in and stores the data of the TMAP file
    def readtmap(self):
        with open(self.master.files["tmap"]) as file:
            self.master.tmapdata = yaml.load(file, Loader=yaml.FullLoader)

    # Reads in the PGM file
    def readpgm(self):
        id, pgmX, pgmY, maxval = 0, 0, 0, 0
        image = open(self.master.files["pgm"], 'r')
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
