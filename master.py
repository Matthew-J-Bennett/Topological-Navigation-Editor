import tkinter as tk
import frames as frame

from tkinter import Menu, messagebox, filedialog
import yaml


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
        self.data_loaded = False

        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        helpmenu = Menu(menubar, tearoff=0)
        # funcmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        # menubar.add_cascade(label="Function Tests", menu=funcmenu)
        # Extra menu to test functions quickly (ignore this)
        filemenu.add_command(label="Open", command=lambda: messagebox.showinfo("Open", "Open a file"))
        filemenu.add_command(label="Save                   Ctrl+S", command=lambda: self.save_filename())
        filemenu.add_command(label="Save As", command=lambda: messagebox.showinfo("Save As", "Save as a file"))
        filemenu.add_command(label="Recent Files/Projects", command=lambda: messagebox.showinfo("Recent Files/Projects",
                                                                                                "Open an Recent "
                                                                                                "Files/Projects"))
        filemenu.add_command(label="Quit", command=lambda: self.master.quit())
        helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "About the program"))

        self.master.config(menu=menubar)
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
                yaml.dump(self.master.tmapdata, outfile, default_flow_style=False)
            self.logger.info("Save Complete")
        else:
            messagebox.showerror("Can't save data", "Can not save because no data is loaded to save")

    @staticmethod
    def frame_swap(old_frame, new_frame):
        old_frame.element.destroy()
        new_frame()


def launch(logging):
    frame.LaunchFrame(Master(logging))
