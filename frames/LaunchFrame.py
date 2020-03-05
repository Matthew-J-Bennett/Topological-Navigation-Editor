import datetime
import json
import os
import random
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import yaml
import contants as const
import elements
import frames


class LaunchFrame:

    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        if not os.path.exists("data/"):
            os.mkdir("data/")
        if not os.path.exists("data/RecentProjects.json"):
            with open('data/RecentProjects.json', 'w') as fp:
                json.dump({}, fp, indent=2)

        # Creates the launch frame
        self.frame = elements.Frame(master=self.window)

        # Adds Decorative Image
        label = elements.Photo(master=master.master, x=100, y=150, imgpath="logo.png", height=200, width=200,
                               relief=tk.RIDGE, bd=3)

        # Adds a title to the top of the screen
        title_label = elements.Label(master=master.master, text="Topological-Navigation-Editor", x=625, y=50,
                                     font=("Roboto", 44),
                                     fg='white', anchor=tk.CENTER)
        # Import files button
        import_button = elements.Button(master=master.master, x=800, y=650, text="Import Files", width=20,
                                        func=lambda: self.get_import_filename())
        # Open files button - To be considered
        open_button = elements.Button(master=master.master, x=1000, y=650, text="Open Project", width=20,
                                      func=lambda: messagebox.showinfo("Title", "a box"))
        # Creates a frame to display recent files
        recent_files_frame = elements.Frame(master=master.master, x=750, y=150, height=450, width=450,
                                            bg=const.tertiary_colour,
                                            relief=tk.RIDGE, bd=3)
        # Placeholder text
        temp_recent_files_text = elements.Label(master=master.master, text="Here is where Recent Projects will go", x=755,
                                                y=160, font=("Roboto", 14), fg='white', bg=const.tertiary_colour)

        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    # Import Files function
    def get_import_filename(self):
        # Produces a Dialog window to allow the user to select files
        self.master.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                            filetypes=(
                                                                ("Map files", ".yaml .pgm .tmap"),
                                                                ("All files", "*.*")))

        # File Validation/Duplication
        if self.set_filenames() == 1:
            self.read_tmap()
            self.read_yaml()
            self.read_pgm()
            self.logging.info("pgm x:" + str(self.master.pgm["width"]) + " pgm y:" + str(self.master.pgm["height"]))

        if len(self.master.filenames) == 3:
            self.master.frame_swap(old_frame=self.frame,
                                   new_frame=lambda: frames.MainFrame(
                                       master=self.master))

    def save_filename(self):
        files2 = [('TMAP Files', '*.*')]
        file = filedialog.asksaveasfilename(filetypes=files2, defaultextension='.tmap')
        with open(file, "w") as outfile:
            yaml.dump(self.master.tmapdata, outfile, default_flow_style=False)

    # Ensures that Files have been imported successfully
    def set_filenames(self):
        # Creates an array to store file names
        self.master.files = {}
        num_files = 0
        # Compares a file to ensure that it is correct
        for x in self.master.filenames:
            # Checks the suffix
            if Path(x).suffix == ".pgm":
                self.master.files["pgm"] = x
                # Logs a file has been imported
                self.logging.info("PGM file imported: {}".format(x))
                # Adds to the file counter
                num_files += 1
            elif Path(x).suffix == ".tmap":
                self.master.files["tmap"] = x
                self.logging.info("TMAP file imported: {}".format(x))
                num_files += 1
            elif Path(x).suffix == ".yaml":
                self.master.files["yaml"] = x
                self.logging.info("YAML file imported: {}".format(x))
                num_files += 1
            else:
                self.logging.info("Invalid file type selected: {}".format(x))
        # If not enough files are provided then it will fail
        if num_files != 3:
            self.logging.info("Not all files selected. Please select again.")
            return 0
        # If successful - then return TRUE condition
        else:
            # Opens and reads previous json as a dict
            with open('data/RecentProjects.json', 'r') as f:
                file_location_dict = json.loads(f.read())
            # Creates the new entry as a separate dict
            random_id = random.randint(1245, 99999)
            new_dict = {
                str(random_id): {"files": self.master.files, "last_opened": str(datetime.datetime.now())}
            }

            # Combines the two dicts to one and then saves it to the files making sure the path is still valid
            file_location_dict = {**file_location_dict, **new_dict}
            if not os.path.exists("data/"):
                os.mkdir("data/")

            with open('data/RecentProjects.json', 'w') as fp:
                json.dump(file_location_dict, fp, indent=2)
            return 1

    # Reads in and stores the data of the YAML file
    def read_yaml(self):
        with open(self.master.files["yaml"]) as file:
            self.master.yaml_data = yaml.load(file, Loader=yaml.FullLoader)

    # Reads in and stores the data of the TMAP file
    def read_tmap(self):
        with open(self.master.files["tmap"]) as file:
            self.master.tmapdata = yaml.load(file, Loader=yaml.FullLoader)
        self.master.data_loaded = True

    # Reads in and stores pgm width and height used on cavas
    def read_pgm(self):
        value, pgm_x, pgm_y, max_val = 0, 0, 0, 0
        image = open(self.master.files["pgm"], 'r')
        x = 0
        while x < 4:
            line = image.readline()
            if x == 0:
                value = line
            if x == 2:
                size = line.split()
                pgm_x = float(size[0])
                pgm_y = float(size[1])
            if x == 3:
                max_val = line
            x += 1
        self.master.pgm = {"id": value, "width": pgm_x, "height": pgm_y, "maxval": max_val}
