import slim


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        self.map: dict
        self.lang: str

    def run(self, key: str) -> str: ...


class Test:
    def __init__(self) -> None:
        self.tran: Tran
        self.TRAN = {
            "zh-cn": {
                "hello": "你好,",
                "input_name": "所以,你的名字是什么?\n输入你的名字:",
                "meet": "很高兴见到你",
                "help": """[name] 可选选项，如果填入则输出"Hello {name}"，否则询问用户的名字再输出""",
            },
            "en-us": {
                "hello": "Hello ",
                "input_name": "So,what are you name?\nInput your name:",
                "meet": "Nice to meet you.",
                "help": """[name] is an optional parameter. If provided, it outputs "Hello {name}"; otherwise, it asks the user for their name and then outputs it.""",
            },
        }

    def enter(self, name: str | None):
        if name:
            print(f"{self.tran.run('hello')}{name}")
        else:
            name = input(self.tran.run("input_name"))
            print(f"{self.tran.run('hello')}{name}!{self.tran.run('meet')}")

    def help(self):
        return self.tran.run("help")

    def config(self, tools, lang: str, **args):
        self.tran = tools["Tran"](self.TRAN, lang)


slim.register("hello", "[name]", Test())
slim.run()
