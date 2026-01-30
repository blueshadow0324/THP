import json

data = {
    "111": "spelare_x",
    "222": "spelare_y",
    "333": "spelare_z"
}

with open("codes.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
