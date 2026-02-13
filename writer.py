import json
import datetime

date = datetime.datetime.now().date()
print(date)

data = {
    "111": "spelare_x",
    "222": "spelare_y",
    "333": "spelare_z"
}

players = {
    "111": {
        "fys": {
            "": ""
        },
        "phy": {
            "": ""
        }
    },
    "222": {
        "phy": "abcd",
        "fys": 300
    }
}
with open("codes.json", "r", encoding="utf-8") as file:
    codes_D = json.load(data, file)