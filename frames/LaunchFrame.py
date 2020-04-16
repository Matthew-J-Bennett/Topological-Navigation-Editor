import datetime
import json
import os
import random
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog
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

        project_button1 = elements.Button(master=master.master, x=759, y=159, text=("Projects to go here"), width=60,
                                          func=lambda: self.get_import_filename())

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
        check = 0
        if self.set_filenames() == 1:
            check = check + self.read_tmap()
            check = check + self.read_yaml()
            check = check + self.read_pgm()
            if check == 3:
                self.logging.info("pgm x:" + str(self.master.pgm["width"]) + " pgm y:" + str(self.master.pgm["height"]))

        if len(self.master.filenames) == 3 and check == 3:
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
                self.master.map_name = x.replace(".pgm", "")
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
            # Creates a window to allow the user to select
            ROOT = tk.Tk()
            ROOT.withdraw()
            self.master.project_name = simpledialog.askstring(title="Project Name",
                                                  prompt="Please choose a name for your collection of files:")
            self.logging.info("Please choose a name for your project:")
            # Opens and reads previous json as a dict
            with open('data/RecentProjects.json', 'r') as f:
                file_location_dict = json.loads(f.read())
            # Creates the new entry as a separate dict
            new_dict = {
                random.randint(1245, 99999): {"project_name": str(self.master.project_name), "files": self.master.files,
                                              "last_opened": str(datetime.datetime.now())}
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
        if self.master.yaml_data is not None:
            return 1
        return 0

    # Reads in and stores the data of the TMAP file
    def read_tmap(self):
        with open(self.master.files["tmap"]) as file:
            self.master.tmapdata = yaml.load(file, Loader=yaml.FullLoader)
        self.master.data_loaded = True
        if self.master.tmapdata is not None:
            return 1
        return 0

    # Reads in and stores pgm width and height used on canvas
    def read_pgm(self):
        value, pgm_x, pgm_y, max_val = 0, 0, 0, 0
        image = open(self.master.files["pgm"], 'r')
        x = 0
        while x < 4:
            line = image.readline()
            size = line.split()
            if len(size) == 2:
                pgm_x = float(size[0])
                pgm_y = float(size[1])
            x += 1
        self.master.pgm = {"id": value, "width": pgm_x, "height": pgm_y, "maxval": max_val}
        return 1
