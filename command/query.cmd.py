import os
import json


def enterance(id: str):
    data = json.load(
            open(
                os.path.dirname(os.path.dirname(__file__)) + "/command.json",
                encoding="utf-8",
            )
        )
    if id == "":
        print("所有命令:")
        for id, format in data.items():
            print(f"  {id} > {format}")
    elif id in data:
        print(f"{id} > {data[id]}")
