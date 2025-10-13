DEBUG = False

import sys, os; sys.dont_write_bytecode = True; os.environ['PYTHONDONTWRITEBYTECODE'] = '1'; os.system('cls'); os.system('title G4Spreader - launching...')
try:
    import time
    import copy
    import uuid
    import json
    import subprocess
    from tkinter import Tk, filedialog, messagebox
    from curl_cffi import exceptions as cfex
    import re
    import multiprocessing
    import traceback
    import requests
    import threading as threadinglib
    import webbrowser
    import concurrent.futures
    import curl_cffi as curlcffi_
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
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Static, Log, ProgressBar
    from rich.text import Text
    import tkinter as tk
    from tkinter import scrolledtext
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    packages = [
        'curl-cffi',
        'requests',
        'textual',
        'datetime',
        'rich',
        'urllib3'
    ]

    print('Installing packages with python -m pip...')
    for pkg in packages:
        os.system(f'python -m pip install {pkg} --upgrade')

    print('\nInstalling packages with py -m pip...')
    for pkg in packages:
        os.system(f'py -m pip install {pkg} --upgrade')
    
    input('Run me againnnnn')