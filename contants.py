import os

# UI Colour Storage
primary_colour = "#222831"
secondary_colour = "#00ADB5"
tertiary_colour = "#393E46"
active_colour = "grey"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if os.path.isfile('icon.ico'):
    ICON_LOC = dname + '/icon.ico'
elif os.path.isfile('../icon.ico'):
    ICON_LOC = '../icon.ico'
else:
    ICON_LOC = None
