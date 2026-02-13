import pandas as pd
import datetime as dt
import json

date = dt.datetime.now().date()

with open(f"{date}.json", "r") as file:
    data = json.load(file)

