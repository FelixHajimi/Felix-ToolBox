import json
import os
import sys
import logging
import importlib.util as pathImport
import rich

logging.basicConfig(
    filename="./last.log",
    format="[%(levelname)s](%(asctime)s)<%(pathname)s>\n%(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)

commandConfig: dict = json.load(open("./command.json", encoding="utf-8"))
args = sys.argv[1:]
commands = {
    ".".join(path.split(".")[:-1]): f"./command/{path}"
    for path in os.listdir("./command/")
}
action = False


def runFunc(func, config: str, argsStart: int):
    if config == "-":
        func()
    else:
        config = config[2:].split(" ")
        data = {}
        for index, arg in enumerate(config):
            if arg[0] == "<" and arg[-1] == ">":
                data[arg[1:-1]] = args[index + argsStart]
            elif arg[0] == "[" and arg[-1] == "]":
                if len(args[argsStart:]) >= index + argsStart:
                    data[arg[1:-1].split(":")[0]] = args[index + argsStart]
                else:
                    data[arg[1:-1].split(":")[0]] = arg[1:-1].split(":")[1]
        func(**data)


commandConfig = {
    key: commandConfig[key]
    for key in sorted(commandConfig, key=lambda item: len(item), reverse=True)
}
for id, config in commandConfig.items():
    if id == ".".join(args[: len(id.split("."))]):
        spec = pathImport.spec_from_file_location("func", commands[id])
        func = pathImport.module_from_spec(spec)
        spec.loader.exec_module(func)
        runFunc(func.enterance, config, len(args[: len(id.split("."))]))
        action = True
        break
if not action:
    logging.error("未找到该命令")
    rich.print("[red bold]ERROR: 未找到该命令[/]")
