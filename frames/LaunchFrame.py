from tkinter import filedialog
from pathlib import Path
import elements
import frames
import yaml
import PIL
from PIL import Image
import os
import shutil
from shutil import copy2


class LaunchFrame:
    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        self.frame = elements.Frame(master=self.window)
        swap_frame_tmp = elements.Button(master=master.master, x=10, y=10, text="Swap Frame to Main Project Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.MainFrame(
                                                                                           master=self.master)))
        import_button = elements.Button(master=master.master, x=10, y=40, text="Import Files", width=20,
                                        func=lambda: self.getimportfilename())
        temp_save_button = elements.Button(master=master.master, x=10, y=90, text="Save Files", width=20)

        if not self.master.launched:
            self.logging.info("Creating Launch Frame")
            self.window.mainloop()

    def getimportfilename(self):
        dirName = 'tempDir'

        try:
            os.mkdir(dirName)
            print("Directory ", dirName, " Created")
        except FileExistsError:
            print("Directory ", dirName, " already exists")

        self.master.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                            filetypes=(
                                                                ("Map files", ".yaml .pgm .tmap"),
                                                                ("all files", "*.*")))

        if self.setfilenames() == 1:
            self.readyaml()
            self.readpgm()

    def setfilenames(self):
        self.master.files = ["", "", ""]
        numfiles = 0
        for x in self.master.filenames:
            if Path(x).suffix == ".pgm" and self.master.files[0] == "":
                self.master.files[0] = x
                print("PGM file imported: ", x, "\n")
                numfiles += 1
            elif Path(x).suffix == ".tmap" and self.master.files[1] == "":
                self.master.files[1] = x
                print("TMAP file imported: ", x, "\n")
                copy2(self.master.files[1], 'tempDir')
                print("TMAP file saved to temporary directory. \n")
                numfiles += 1
            elif Path(x).suffix == ".yaml" and self.master.files[2] == "":
                self.master.files[2] = x
                print("YAML file imported: ", x, "\n")
                copy2(self.master.files[2], 'tempDir')
                print("YAML file saved to temporary directory. \n")
                numfiles += 1
            else:
                print("Invalid file type selected: ", x, "\n")
        if numfiles != 3:
            print("Not all files selected. Please select again.")
            return 0
        else:
            return 1

    def readyaml(self):
        with open(self.master.files[2]) as file:
            self.master.yamldata = yaml.load(file, Loader=yaml.FullLoader)
            print(self.master.yamldata)

    def readpgm(self):
        image = PIL.Image.open(self.master.files[0])
        rgb_im = image.convert('RGB')
        rgb_im.save('tempDir\map.jpg')
        print(".pgm successful converted to .jpg.")
