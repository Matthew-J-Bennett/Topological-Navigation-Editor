from tkinter import filedialog, messagebox

import elements
import frames


class LaunchFrame:
    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        self.frame = elements.Frame(master=self.window, bg="grey24")

        swap_frame_tmp = elements.Button(master=master.master, x=10, y=10, text="Swap Frame to Main Project Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.MainFrame(
                                                                                           master=self.master)))

        import_button = elements.Button(master=master.master, x=800, y=600, text="Import Files", width=20,
                                        func=lambda: self.getimportfilename())

        open_button = elements.Button(master=master.master, x=1000, y=600, text="Open Files", width=20,
                                      func=lambda: messagebox.showinfo("Title", "a box"))

        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    def getimportfilename(self):
        self.master.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
