import tkinter as tk
import frames as frame
import os
from tkinter import Menu, messagebox, filedialog
import yaml
import contants
import json


class Master:
    def __init__(self, logger):
        self.master = tk.Tk()
        self.logger = logger
        self.master.resizable(False, False)
        self.master.title('Topological Navigation Editor')
        self.window_height = 800
        self.window_width = 1250
        self.master.geometry('{}x{}'.format(self.window_width, self.window_height))
        self.launched = False
        self.logger.info("Window Created")
        self.master.iconbitmap(contants.ICON_LOC)
        self.data_loaded = False
        with open('.version', 'r') as file:
            self.version = file.read()
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        # Extra menu to test functions quickly (ignore this)
        self.filemenu.add_command(label="Save                   Ctrl+S", command=lambda: self.save_filename(0))
        self.filemenu.add_command(label="Save As", command=lambda: self.save_filename(1))
        self.helpmenu.add_command(label="About", command=lambda: self.open_help())

        self.master.config(menu=self.menubar)
        self.master.bind("<Control-s>", self.save_shortcut_event)

    def save_shortcut_event(self, event):
        self.save_filename(0)

    @staticmethod
    def open_help():
        file = "notepad.exe help.txt"
        os.system(file)

    def save_filename(self, save_as):
        if self.data_loaded:
            if save_as == 1:
                self.logger.info("Opening File Save Dialog box")
                files2 = [('TMAP Files', '*.tmap')]
                file = filedialog.asksaveasfilename(filetypes=files2, defaultextension='.tmap')
                if self.from_recent:
                    with open('data/RecentProjects.json', 'r') as f:
                        data = json.loads(f.read())
                    for item in data:
                        if data[item]["project_name"] == self.from_recent["project_name"] and data[item][
                            "last_opened"] == \
                                self.from_recent["last_opened"]:
                            data[item]["files"]["tmap"] = file
                    with open('data/RecentProjects.json', 'w') as fp:
                        json.dump(data, fp, indent=2)

            else:
                file = self.files["tmap"]

            if file == "":
                self.logger.info("Saving Cancelled")
                return 0

            self.logger.info("Saving tmap data to: {}".format(file))
            with open(file, "w") as outfile:
                yaml.dump(self.tmapdata, outfile, default_flow_style=False)
            self.logger.info("Save Complete")

        else:
            messagebox.showerror("Can't save data", "Can not save because no data is loaded to save")

    @staticmethod
    def frame_swap(old_frame, new_frame):
        old_frame.element.destroy()
        new_frame()


def launch(logging):
    frame.LaunchFrame(Master(logging))
