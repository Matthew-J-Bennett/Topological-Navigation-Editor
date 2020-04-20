import tkinter as tk
import frames as frame

from tkinter import Menu, messagebox, filedialog
import yaml
import contants


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

        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        # Extra menu to test functions quickly (ignore this)
        self.filemenu.add_command(label="Save                   Ctrl+S", command=lambda: self.save_filename())
        self.filemenu.add_command(label="Quit", command=lambda: self.master.quit())
        self.helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About",
                                                                                     "Topological-Navigation-Editor "
                                                                                     "v0.3.3"))

        self.master.config(menu=self.menubar)
        self.master.bind("<Control-s>", self.save_shortcut_event)

    def save_shortcut_event(self, event):
        self.save_filename()

    def save_filename(self):
        if self.data_loaded:
            self.logger.info("Opening File Save Dialog box")
            files2 = [('TMAP Files', '*.tmap')]
            file = filedialog.asksaveasfilename(filetypes=files2, defaultextension='.tmap')

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
