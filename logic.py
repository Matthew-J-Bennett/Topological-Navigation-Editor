import yaml
from tkinter import filedialog, messagebox


class Logic:
    def __init__(self, master):
        self.master = master

    def save_filename(self):
        if self.master.data_loaded:
            self.master.logger.info("Opening File Save Dialog box")
            files2 = [('TMAP Files', '*.tmap')]
            file = filedialog.asksaveasfilename(filetypes=files2, defaultextension='.tmap')

            if file == "":
                self.master.logger.info("Saving Cancelled")
                return 0

            self.master.logger.info("Saving tmap data to: {}".format(file))
            with open(file, "w") as outfile:
                yaml.dump(self.master.tmapdata, outfile, default_flow_style=False)
            self.master.logger.info("Save Complete")
        else:
            messagebox.showerror("Can't save data", "Can not save because no data is loaded to save")
