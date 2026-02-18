import os
import datetime
import requests
import json
from core.Profiler import Profiler

def init():
    global version
    global monip, monpays, codemonpays, pathDatabase
    # Note: keep settings lightweight; heavy tools are imported by `LittleBrother.py` when needed
    global Profiler

    version = '6.0.2'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pathDatabase = os.path.join(base_dir, "Watched")

    monip = requests.get("https://api.ipify.org/").text

    monpays = requests.get("http://ip-api.com/json/"+monip).text
    value = json.loads(monpays)
    monpays = value['country']
    codemonpays = value['countryCode']

    if not os.path.exists(pathDatabase):
        os.mkdir(pathDatabase)
