import datetime
import json
import os
import random
import tkinter as tk
from pathlib import Path
import shutil
from tkinter import filedialog, simpledialog, messagebox
import yaml
import contants as const
import elements
import frames
import requests


class YamlDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Free Thresh:").grid(row=0)
        tk.Label(master, text="Negate:").grid(row=1)
        tk.Label(master, text="Occupied Thresh:").grid(row=2)
        tk.Label(master, text="Origin:").grid(row=3)
        tk.Label(master, text="Resolution:").grid(row=4)
        self.free_thresh = tk.Entry(master)
        self.negate = tk.Entry(master)
        self.occupied_thresh = tk.Entry(master)
        self.origin_x = tk.Entry(master)
        self.origin_y = tk.Entry(master)
        self.origin_z = tk.Entry(master)
        self.resolution = tk.Entry(master)

        self.free_thresh.grid(row=0, column=1)
        self.negate.grid(row=1, column=1)
        self.occupied_thresh.grid(row=2, column=1)
        self.origin_x.grid(row=3, column=1)
        self.origin_y.grid(row=3, column=2)
        self.origin_z.grid(row=3, column=3)
        self.resolution.grid(row=4, column=1)

    def apply(self):
        self.result = [self.free_thresh.get(), self.negate.get(), self.occupied_thresh.get(), self.origin_x.get(),
                       self.origin_y.get(), self.origin_z.get(), self.resolution.get()]
        error = 0
        for result in self.result:
            try:
                float(result)
            except ValueError:
                if error == 0:
                    messagebox.showerror("Error", "YAML data must be float values.")
                error = 1
                self.result = 0
        if error == 0:
            if float(self.resolution.get()) <= 0:
                messagebox.showerror("Error", "Resolution must be greater than zero.")
                self.result = 0


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

        url = 'https://api.github.com/repos/Matthew-J-Bennett/Topological-Navigation-Editor/releases'
        try:
            response = requests.get(url)
            response.raise_for_status()
            resdata = response.json()
            version = resdata[0]["tag_name"]
            notes = resdata[0]["body"]
            notes2 = notes.split("##")[1] + notes.split("##")[2]
        except:
            notes2 = "There was a problem fetching the latest release notes."
            version = ""

        # Creates the launch frame
        self.frame = elements.Frame(master=self.window)
        self.master.from_recent = 0
        self.master.from_new = 0
        self.master.changes = 0

        # Adds Decorative Image
        logo = elements.Photo(master=master.master, x=80, y=150, imgpath="logo.png", height=200, width=200,
                              relief=tk.RIDGE, bd=3)
        elements.Label(master=master.master, text="Release Notes:", x=180, y=400, font=("Roboto", 18), fg='white',
                       anchor=tk.CENTER)
        elements.Label(master=master.master, text=notes2, x=80, y=430, font=("Roboto", 16), fg='white', anchor='nw')
        elements.Label(master=master.master, text=version, x=40, y=760, font=("Roboto", 18), fg='white',
                       anchor=tk.CENTER)

        # Adds a title to the top of the screen
        elements.Label(master=master.master, text="Topological-Navigation-Editor", x=625, y=50, font=("Roboto", 44),
                       fg='white', anchor=tk.CENTER)
        # Creates a frame to display recent files
        elements.Frame(master=master.master, x=340, y=180, height=132.5, width=310, bg=const.tertiary_colour,
                       relief=tk.RIDGE, bd=3)
        elements.Button(master=master.master, x=350, y=195, text="Start New Project From PGM", width=40,
                        func=lambda: self.new_project())
        # Import files button
        elements.Button(master=master.master, x=350, y=255, text="Import Loose Files", width=40,
                        func=lambda: self.get_import_filename(0))
        # Adds a title to the recent files display
        elements.Label(master=master.master, text="Recent files", x=850, y=130, font=("Roboto", 24),
                       fg='white', anchor=tk.CENTER)
        # Creates a frame to display recent files
        elements.Frame(master=master.master, x=750, y=150, height=460, width=450, bg=const.tertiary_colour,
                       relief=tk.RIDGE, bd=3)
        y_pos = 0
        max_val = 0
        self.sort_by_date()
        data = self.master.json_data
        for item in data:
            max_val += 1
            if max_val < 10:
                y_pos = y_pos + 50
                elements.Button(master=master.master, x=759, y=110 + y_pos,
                                text=(data[item]["project_name"] + "  -/-  " + data[item]["last_opened"].split(".")[0]),
                                width=60,
                                func=lambda j=item: self.get_import_filename(j))
        if max_val == 0:
            elements.Label(master=master.master, text="Recent files go here...", x=975, y=200, font=("Roboto", 24),
                           fg='white', anchor=tk.CENTER)

        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    def sort_by_date(self):
        with open('data/RecentProjects.json') as data_file:
            self.master.json_data = json.load(data_file)
        data = self.master.json_data
        num_data = len(data)
        for i in range(num_data):
            for j in range(0, num_data - i - 1):
                date_1 = (data[list(data.keys())[j]]["last_opened"]).split(" ")[0]
                date_2 = (data[list(data.keys())[j + 1]]["last_opened"]).split(" ")[0]
                time_1 = (data[list(data.keys())[j]]["last_opened"]).split(" ")[1]
                time_2 = (data[list(data.keys())[j + 1]]["last_opened"]).split(" ")[1]
                if (date_1 <= date_2 and time_1 < time_2) or (date_1 < date_2):
                    data[list(data.keys())[j]], data[list(data.keys())[j + 1]] = data[list(data.keys())[j + 1]], \
                                                                                 data[list(data.keys())[j]]
        self.master.json_data = data

    # Import Files function
    def get_import_filename(self, file_names):
        if self.master.from_new == 0:
            if file_names == 0:
                # Produces a Dialog window to allow the user to select files
                self.master.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(
                    ("Map files", ".yaml .pgm .tmap"),
                    ("All files", "*.*")))
            else:
                file_names = self.master.json_data[file_names]
                self.master.filenames = [file_names["files"]["pgm"], file_names["files"]["yaml"],
                                         file_names["files"]["tmap"]]
                self.logging.info(self.master.filenames)
                self.master.project_name = file_names["project_name"]
                self.master.from_recent = file_names

        # File Validation
        check = 0
        if self.set_filenames() == 1:
            check = check + self.read_tmap()
            check = check + self.read_yaml()
            check = check + self.read_pgm()
            if check == 3:
                self.logging.info("pgm x:" + str(self.master.pgm["width"]) + " pgm y:" + str(self.master.pgm["height"]))
        else:
            self.logging.info("no set file")

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
            if self.master.from_recent == 0:
                # Creates a window to allow the user to select
                ROOT = tk.Tk()
                ROOT.withdraw()
                if self.master.from_new == 0:
                    self.master.project_name = simpledialog.askstring(title="Project Name",
                                                                      prompt="Please choose a name for your collection of files:")
                # Opens and reads previous json as a dict
                with open('data/RecentProjects.json', 'r') as f:
                    file_location_dict = json.loads(f.read())
                # Creates the new entry as a separate dict
                new_dict = {
                    random.randint(1245, 99999): {"project_name": str(self.master.project_name),
                                                  "files": self.master.files,
                                                  "last_opened": str(datetime.datetime.now())}
                }

                # Combines the two dicts to one and then saves it to the files making sure the path is still valid
                file_location_dict = {**file_location_dict, **new_dict}
                if not os.path.exists("data/"):
                    os.mkdir("data/")

                with open('data/RecentProjects.json', 'w') as fp:
                    json.dump(file_location_dict, fp, indent=2)
            else:
                data = self.master.json_data
                for item in data:
                    if data[item]["project_name"] == self.master.from_recent["project_name"] and data[item][
                        "last_opened"] == \
                            self.master.from_recent["last_opened"]:
                        data[item]["last_opened"] = str(datetime.datetime.now())
                with open('data/RecentProjects.json', 'w') as fp:
                    json.dump(data, fp, indent=2)
            return 1

    # Reads in and stores the data of the YAML file
    def read_yaml(self):
        with open(self.master.files["yaml"]) as file:
            self.master.yaml_data = yaml.load(file, Loader=yaml.FullLoader)
        if self.master.yaml_data is not None:
            self.logging.info(self.master.yaml_data)
            return 1
        return 0

    # Reads in and stores the data of the TMAP file
    def read_tmap(self):
        with open(self.master.files["tmap"]) as file:
            self.master.tmapdata = yaml.load(file, Loader=yaml.FullLoader)
        self.master.data_loaded = True
        return 1

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

    def new_project(self):
        self.master.file_name = filedialog.askopenfilename(initialdir="/", title="Select PGM File", filetypes=(
            ("Map files", ".pgm"), ("all files", "*.*")))
        if not self.master.file_name == "":
            if not os.path.exists("files/"):
                os.mkdir("files/")
            shutil.copy2(self.master.file_name, os.getcwd() + "\\files")
            if self.new_yaml() == 1:
                self.master.from_new = 1
                self.get_import_filename(1)

    def new_yaml(self):
        self.master.project_name = simpledialog.askstring(title="Project Name",
                                                          prompt="Please choose a name for your collection of "
                                                                 "files:")
        self.logging.info("file name: {}".format(self.master.project_name))
        user_yaml = YamlDialog(self.window)
        self.logging.info(user_yaml.result)
        map_split = self.master.file_name.split("/")
        map_name = map_split[len(map_split) - 1].replace(".pgm", "")
        if user_yaml.result != 0:
            yaml_data = {'free_thresh': float(user_yaml.result[0]), 'image': str(map_name),
                         'negate': float(user_yaml.result[1]), 'occupied_thresh': float(user_yaml.result[2]),
                         'origin': [float(user_yaml.result[3]), float(user_yaml.result[4]), float(user_yaml.result[5])],
                         'resolution': float(user_yaml.result[6])}
            self.logging.info(yaml_data)
            if not os.path.exists("files/"):
                os.mkdir("files/")
            if not os.path.exists("files/" + self.master.project_name + ".yaml"):
                with open("files/" + self.master.project_name + ".yaml", 'w') as outfile:
                    yaml.dump(yaml_data, outfile, default_flow_style=False)
            if not os.path.exists("files/" + self.master.project_name + ".tmap"):
                with open("files/" + self.master.project_name + ".tmap", 'w') as outfile:
                    pass
            directory = os.getcwd()
            self.master.filenames = [directory + "\\files\\" + map_name + ".pgm",
                                     directory + "\\files\\" + self.master.project_name + ".yaml",
                                     directory + "\\files\\" + self.master.project_name + ".tmap"]
            return 1
        else:
            return 0
