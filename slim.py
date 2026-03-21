import importlib.util as pathImport
import json
import logging
import os
import pathlib
import re
import sys


def configParser(config: str):
    args = config.split(" ")[1:]
    res = []
    for arg in args:
        match1 = re.fullmatch(
            r"<([a-zA-Z_][a-zA-Z_\d]*)?(\(.*\))?(:\d+)?>(string|int|float|bool|json)?",
            arg,
        )
        match2 = re.fullmatch(
            r"\[([a-zA-Z_][a-zA-Z_\d]*)?(\(.*\))?(:\d+)?(=.*)?\](string|int|float|bool|json)?",
            arg,
        )
        if match1:
            if not match1.group(1):
                logging.error(tran.run("fillName", f"<?>{arg}"))
                print(
                    f"\033[48;2;255;0;0;38;2;255;255;255m{tran.run('fillName', f'<?>{arg}')}\033[0m"
                )
            res.append(
                {
                    "class": 1,
                    "name": match1.group(1),
                    "regex": match1.group(2)[1:-1] if match1.group(2) else None,
                    "length": int(match1.group(3)[1:]) if match1.group(3) else None,
                    "type": match1.group(4) if match1.group(4) else "string",
                }
            )
        elif match2:
            if not match2.group(1):
                logging.error(tran.run("fillName", f"<?>{arg}"))
                print(
                    f"\033[48;2;255;0;0;38;2;255;255;255m{tran.run('fillName', f'<?>{arg}')}\033[0m"
                )
            res.append(
                {
                    "class": 2,
                    "name": match2.group(1),
                    "regex": match2.group(2)[1:-1] if match2.group(2) else None,
                    "length": int(match2.group(3)[1:]) if match2.group(3) else None,
                    "default": match2.group(4)[1:] if match2.group(4) else None,
                    "type": match2.group(5) if match2.group(5) else "string",
                }
            )
        else:
            logging.error(tran.run("notMatchFormat", f"<?>{arg}"))
            print(
                f"\033[48;2;255;0;0;38;2;255;255;255m{tran.run('notMatchFormat', f'<?>{arg}')}\033[0m"
            )
    return res


def toType(text: str | None, type_: str | None):
    if text is None or type_ is None:
        return None
    mapping = {
        "string": str,
        "int": int,
        "float": float,
        "bool": bool,
        "json": json.loads,
    }
    for t, f in mapping.items():
        if type_ == t:
            if type_ == "json":
                text = text.replace("'", '"')
            try:
                return f(text)
            except Exception as error:
                logging.error(f"转换错误:{error}")
                return None


def runFunc(enter, config: str, argStartIndex: int):
    if config == "-":
        enter()
    else:
        data = {}
        parser = configParser(config)
        for index, arg in enumerate(parser):
            argIndex = argStartIndex + index + 1
            argList: list
            try:
                if arg["class"] == 1:
                    if arg["length"] or arg["length"] == 0:
                        argList = (
                            args[argIndex:]
                            if arg["length"] == 0
                            else args[argIndex : 1 + arg["length"]]
                        )
                        for _ in range(arg["length"] - len(argList)):
                            argList.append(None)
                        for index, text in enumerate(argList):
                            value = None
                            if arg["regex"]:
                                value = toType(
                                    text if re.fullmatch(arg["regex"], text) else None,
                                    arg["type"],
                                )
                            else:
                                value = toType(text, arg["type"])
                            argList[index] = value
                        data[arg["name"]] = argList
                    else:
                        value = None
                        if arg["regex"]:
                            value = toType(
                                args[argIndex]
                                if re.fullmatch(arg["regex"], args[argIndex])
                                else None,
                                arg["type"],
                            )
                        else:
                            value = toType(args[argIndex], arg["type"])
                        data[arg["name"]] = value
                elif arg["class"] == 2:
                    if arg["length"] or arg["length"] == 0:
                        argList = (
                            args[argIndex:]
                            if arg["length"] == 0
                            else args[argIndex : 1 + arg["length"]]
                        )
                        for _ in range(arg["length"] - len(argList)):
                            argList.append(arg["default"])
                        for index, text in enumerate(argList):
                            value = None
                            if len(args) - 1 >= argIndex:
                                if arg["regex"]:
                                    value = toType(
                                        text
                                        if re.fullmatch(arg["regex"], text)
                                        else arg["default"],
                                        arg["type"],
                                    )
                                else:
                                    value = toType(text, arg["type"])
                            else:
                                value = toType(arg["default"], arg["type"])
                            argList[index] = value
                        data[arg["name"]] = argList
                    else:
                        value = None
                        if len(args) - 1 >= argIndex:
                            if arg["regex"]:
                                value = toType(
                                    args[argIndex]
                                    if re.fullmatch(arg["regex"], args[argIndex])
                                    else arg["default"],
                                    arg["type"],
                                )
                            else:
                                value = toType(args[argIndex], arg["type"])
                        else:
                            value = toType(arg["default"], arg["type"])
                        data[arg["name"]] = value
                else:
                    logging.error(f"{tran.run('notFoundFormat')}{arg['class']}")
                    print(f"{tran.run('notFoundFormat')}{arg['class']}")
            except Exception:
                logging.error(eval(tran.run("requiredError")))
                print(
                    f"\033[48;2;255;0;0;38;2;255;255;255m{eval(tran.run('requiredError'))}\033[0m"
                )
                return
        enter(**data)


class AdminCommands:
    def __init__(self, debug: bool = False):
        self.debug = debug

    def help(self, id: str | None):
        commands = json.load(open(f"{PATH}/command.json", encoding="utf-8"))
        if id is None:
            for id, config in commands.items():
                print(f"{id} : {config}")
        else:
            try:
                print(f"{id} : {commands[id]}")
            except KeyError:
                logging.error(f"{tran.run('notFoundCommand')}{id}")
                print(
                    f"\033[48;2;255;0;0;38;2;255;255;255m{tran.run('notFoundCommand')}{id}\033[0m"
                )

    def create(self, id: str | None, config: str | None):
        commandConfig = json.load(
            open(f"{PATH}/{SETTING['commandConfig']}", encoding="utf-8")
        )
        if id is None and config is None:
            for id, config in commandConfig.items():
                if id is None or config is None:
                    return
                path = f"{PATH}/{SETTING['commandDir']}/{'/'.join(id.split('.'))}.py"
                p = pathlib.Path(path)
                if not p.exists():
                    p.touch()
                    argsText = ""
                    for arg in configParser(config):
                        argsText = (
                            f"{argsText}, {arg['name']}: {'list[str | None]' if arg['array'] else 'str'}"
                            if arg["type"] == 1
                            else (
                                f"{argsText}, {arg['name']}: {'list[str | None]' if arg['array'] else 'str | None'}"
                                if arg["type"] == 2
                                else f"{argsText}, ERROR"
                            )
                        )
                    open(path, "w", encoding="utf-8").write(
                        f"def config(**args):\n    pass\n\ndef enter({argsText[2:]}):\n    pass"
                    )
                    logging.info(tran.run("createdFile", f"<?>{path}"))
                    print(tran.run("createdFile", f"<?>{path}"))
        else:
            commandConfig[id] = "-" if config is None else config
            open(SETTING["commandConfig"], "w", encoding="utf-8").write(
                json.dumps(commandConfig, indent=2, ensure_ascii=False)
            )
            print(tran.run("createdFile", f"<?>{SETTING['commandConfig']}"))
            self.create(None, None)


def runAdminFunc(adminArgs: list[str]):
    admin = AdminCommands(SETTING["debug"])
    adminCommands = {
        "help": ("- [id]", admin.help),
        "create": ("- [id] [config]", admin.create),
    }
    adminCommands = {
        key: adminCommands[key]
        for key in sorted(adminCommands, key=lambda item: len(item), reverse=True)
    }
    for command, config in adminCommands.items():
        if command == ".".join(adminArgs[: len(command.split("."))]):
            logging.info(tran.run("runningAdminCommand", f"<?>:{args}"))
            runFunc(config[1], config[0], len(command.split(".")))
            exit()
    logging.error(tran.run("notFoundCommand", f"<?>{args}"))
    print(
        f"\033[48;2;255;0;0;38;2;255;255;255m{tran.run('notFoundCommand', f'<?>{args}')}\033[0m"
    )


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        self.map = translateMap
        self.lang = lang

    def run(self, key: str, content: str = "<?>"):
        if self.lang not in self.map:
            if "en-us" in self.map:
                language = "en-us"
            else:
                language = next(iter(self.map))
        else:
            language = self.lang
        return content.replace("<?>", self.map[language][key])


logging.basicConfig(
    filename="./last.log",
    format="[%(levelname)s](%(asctime)s)<%(pathname)s>\n%(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)


PATH = os.path.dirname(os.path.abspath(__file__))
TRAN = {
    "zh-cn": {
        "requiredError": 'f"你有一个必填项未填写: 应该在第 {index} 个参数填写,参数名为 {arg["name"]}"',
        "notFoundCommand": "未找到该命令: ",
        "createdFile": "已创建文件至: ",
        "fillName": "请填写参数名: ",
        "notMatchFormat": "没有匹配此格式的参数: ",
        "notFoundCommandFile": "检测到命令文件不存在,程序已退出",
        "runningCommand": "正在运行命令",
        "runningAdminCommand": "正在运行管理员命令",
        "notFoundFormat": "没有此格式: ",
    },
    "en-us": {
        "requiredError": 'f"You have a required parameter not filled: should be filled at position {index}, parameter name is {arg["name"]}"',
        "notFoundCommand": "Command not found: ",
        "createdFile": "File created at: ",
        "fillName": "Please fill in parameter name: ",
        "notMatchFormat": "No parameter matching this format: ",
        "notFoundCommandFile": "Command file not detected, the program has exited",
        "runningCommand": "Running command",
        "runningAdminCommand": "Running admin command",
        "notFoundFormat": "This format does not exist: ",
    },
}
SETTING = json.load(open(f"{PATH}/setting.json", encoding="utf-8"))


commandConfig: dict = json.load(
    open(f"{PATH}/{SETTING['commandConfig']}", encoding="utf-8")
)
commandConfig = {
    key: commandConfig[key]
    for key in sorted(commandConfig, key=lambda id: len(id), reverse=True)
}
commands = {
    key: f"{PATH}/{SETTING['commandDir']}/{'/'.join(key.split('.'))}.py"
    for key in commandConfig
}
tran = Tran(TRAN, SETTING["language"])
args = sys.argv[1:]
if len(args) != 0 and args[0] == "--admin":
    runAdminFunc(args[1:])
    exit()


configArgs = {
    "path": PATH,
    "lang": SETTING["language"],
    "debug": SETTING["debug"],
    "other": SETTING["other"],
    "tools": {
        "tran": Tran,
        "configParser": configParser,
        "runFunc": runFunc,
    },
}


for id, config in commandConfig.items():
    if id == ".".join(args[: len(id.split("."))]):
        try:
            spec = pathImport.spec_from_file_location("func", commands[id])
            if not spec or not spec.loader:
                raise
            func = pathImport.module_from_spec(spec)
            spec.loader.exec_module(func)
        except Exception:
            logging.warning(tran.run("notFoundCommandFile"))
            print(
                f"\033[48;2;255;255;0;38;2;255;255;255m{tran.run('notFoundCommandFile')}\033[0m"
            )
            exit()
        if hasattr(func, "config"):
            getattr(func, "config")(**configArgs)
        logging.info(tran.run("runningCommand", f"<?>:{args}"))
        runFunc(func.enter, config, len(args[: len(id.split("."))]) - 1)
        exit()
logging.error(tran.run("notFoundCommand", f"<?>{args}"))
print(
    f"\033[48;2;255;0;0;38;2;255;255;255m{tran.run('notFoundCommand', f'<?>{args}')}\033[0m"
)
