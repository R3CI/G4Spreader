import sys, os; sys.dont_write_bytecode = True; os.environ['PYTHONDONTWRITEBYTECODE'] = '1'; os.system('cls'); os.system('title G4Spreader - launching...')
import time
import copy
import uuid
import json
import subprocess
from tkinter import Tk, filedialog, messagebox
from curl_cffi import exceptions as cfex
import re
import traceback
import threading as threadinglib
import webbrowser
import concurrent.futures
import curl_cffi as curlcffi_
from discordrp import Presence
from curl_cffi import requests as curlcffi
from datetime import datetime as dt, timedelta, timezone
from urllib.parse import urlparse, quote
from collections import defaultdict, namedtuple
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
from requests.cookies import RequestsCookieJar
import base64
import random
import string
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

class co:
    main = rgb(80, 5, 255)
    red = rgb(255, 69, 0)
    darkred = rgb(87, 2, 2)
    green = rgb(12, 250, 0)
    blue = rgb(30, 144, 255)
    yellow = rgb(255, 215, 0)
    orange = rgb(255, 140, 0)
    deeporange = rgb(201, 105, 6)
    pink = rgb(255, 105, 180)
    cyan = rgb(0, 255, 255)
    magenta = rgb(255, 0, 255)
    lime = rgb(12, 250, 0)
    indigo = rgb(138, 43, 226)
    grey = rgb(169, 169, 169)
    black = rgb(69, 69, 69)
    white = rgb(255, 255, 255)

    infolog = pink
    success = lime
    error = red
    locked = darkred
    debug = grey
    warning = yellow
    ratelimit = orange
    cloudflare = deeporange
    solver = indigo
    captcha = cyan
    
    reset = '\033[0m'

from src.utils.errorhandler import errorhandler
sys.excepthook = errorhandler
from src.utils.files import files
files.check()