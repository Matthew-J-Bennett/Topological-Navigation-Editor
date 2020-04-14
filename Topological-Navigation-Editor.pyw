import json
import logging
import math
import os
import platform
import re
import subprocess
import sys
import time
from urllib import request, parse
import tkinter as tk
import contants

import master

ACTIVE_SYMBOL = '✕'
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if platform.system() == 'Windows':
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Matthew-J-Bennett.Topological-Navigation-Editor')


# Declare Top Level Functions
def has_internet(site='http://google.co.uk'):
    try:
        _request = request.Request(site, headers={'User-Agent': 'python'})
        request.urlopen(_request, timeout=1)
        return True
    except:
        return False


def updates_enabled():
    return not os.path.isfile(".disableupdates")


def cause_update():
    dir_name = os.getcwd()
    addr = dname + '/updater.pyw'
    subprocess.Popen(['', addr], executable=sys.executable)
    os._exit(1)


def post_request(address, dictionary, headers=None):
    if headers is None:
        headers = {'user-agent': 'python'}
    data = parse.urlencode(dictionary).encode()
    _request = request.Request(address, data=data, headers=headers)
    response = request.urlopen(_request, timeout=5).read().decode()
    return response


def get_request(address, headers=None):
    if headers is None:
        headers = {'user-agent': 'python'}
    _request = request.Request(address, headers=headers)
    response = request.urlopen(_request, timeout=5).read().decode()
    return response


def pagerise(x, per=10000):
    pages = int(math.ceil(len(x) / per))
    output = []
    for i in range(pages):
        output.append(x[per * i:per * (i + 1)])
    return output


# Grab Current Version
with open('.version', 'r') as file:
    version = file.read()

internet_connected = has_internet()
updates_enabled = updates_enabled()

if internet_connected and updates_enabled and has_internet(
        'https://api.github.com/repos/Matthew-J-Bennett/Topological-Navigation-Editor/releases/latest'):
    print('Checking for updates...')
    query_address = 'https://api.github.com/repos/Matthew-J-Bennett/Topological-Navigation-Editor/releases/latest'
    data = request.urlopen(query_address).read().decode('utf-8')
    latest_version = json.loads(data)['tag_name']
    version_nums = re.findall(r'\d+', version)
    latest_version_nums = re.findall(r'\d+', latest_version)

    if len(version_nums) != len(latest_version_nums):
        if len(version_nums) > len(latest_version_nums):
            latest_version_nums += (len(version_nums) - len(latest_version_nums)) * [0]
        else:
            version_nums += (len(latest_version_nums) - len(version_nums)) * [0]

    comp = list(zip([int(x) for x in latest_version_nums], [int(x) for x in version_nums]))

    for each in comp:
        if each[0] > each[1]:
            temp_window = tk.Tk()
            try:
                temp_window.iconbitmap(contants.ICON_LOC)
            except TclError:
                print('Your version of Python has errors relating to icons. An icon will not be used.')
            update_text = 'Your version of the Topological Navigation Editor (' + version + \
                          ') is not the latest available version (' + latest_version + \
                          '). Do you wish to update the software?'
            result = tk.messagebox.askyesno('Update Available', update_text, master=temp_window)
            temp_window.destroy()
            if result:
                cause_update()
            else:
                break
else:
    print("Updates will not be performed!")


# exceptions handler


def execp_handler(type, value, tb):
    logger.exception("Exception: {}".format(value))


# Initiates the logger


if __name__ == "__main__":

    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger("Topological-Navigation-Editor")
    # Creates a console log with timestamp
    handler = logging.FileHandler('logs/{}.log'.format(time.strftime("%Y-%m-%d %H-%M-%S")))
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler2 = logging.StreamHandler()
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    logger.setLevel(logging.DEBUG)
    logger.info('{}'.format(time.asctime()))

    sys.excepthook = execp_handler

    master.launch(logger)
