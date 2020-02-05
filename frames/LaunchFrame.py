from tkinter import filedialog, messagebox, PhotoImage
import tkinter as tk
import elements
import frames
import contants as const


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

        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    def getimportfilename(self):
        self.master.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
