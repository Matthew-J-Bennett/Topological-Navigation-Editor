import tkinter as tk
import frames as frame

from tkinter import Menu, messagebox


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

        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        helpmenu = Menu(menubar, tearoff=0)
        # funcmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        # menubar.add_cascade(label="Function Tests", menu=funcmenu)
        # Extra menu to test functions quickly (ignore this)
        filemenu.add_command(label="Open", command=lambda: messagebox.showinfo("Open", "Open a file"))
        filemenu.add_command(label="Save", command=lambda: messagebox.showinfo("Save", "Save a file"))
        filemenu.add_command(label="Save As", command=lambda: messagebox.showinfo("Save As", "Save as a file"))
        filemenu.add_command(label="Save All", command=lambda: messagebox.showinfo("Save All", "Save all files"))
        filemenu.add_command(label="Recent Files/Projects", command=lambda: messagebox.showinfo("Recent Files/Projects",
                                                                                                "Open an Recent "
                                                                                                "Files/Projects"))
        filemenu.add_command(label="Quit", command=lambda: self.master.quit())
        helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "About the program"))
        self.master.config(menu=menubar)

    @staticmethod
    def frame_swap(old_frame, new_frame):
        old_frame.element.destroy()
        new_frame()


def launch(logging):
    frame.LaunchFrame(Master(logging))
