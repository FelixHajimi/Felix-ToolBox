# This article will describe all the API interfaces of the commands

## Example
```py
# script.py
"""
See line 190 of the program
configArgs = {
"path": PATH,
"lang": SETTING["language"],
"debug": SETTING["debug"],
"tools": {"tran": Tran},
}
"""
def config(path: str, lang: str, debug: bool, tools: dict[str, any]):
    pass

def enter(**args): # Here are all the parameter configurations you wrote in the config
    # Specific business logic
    pass
```

### Function of the config function
It represents the global settings of the program. The program will pass the global settings into this function as parameters.
Parameters explained:
- path: the path of the main program, see line 161 of the program
- lang: global language, can be used with `tools["tran"]`
- debug: global debug mode, can output detailed information in debug mode
- tools: tools that may be used, currently contains a tool called Tran, see line 137 of the program or refer to the "Tools" documentation