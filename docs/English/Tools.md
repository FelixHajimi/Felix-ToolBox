# This article will explain the usage of all tools in the config function API

## tran-Tran
This is a translation tool, see line 137 of the program.  
It has a built-in `run` method, which returns a string as the translated text.

### Example
```py
tran = None
TRAN = {
    "zh-cn": {
        "hello": "你好!"
    },
    "en-us": {
        "hello": "Hello!"
    },
}
def config(tools: dict[str, any], lang: str, **args):
    global tran
    tran = tools["tran"](TRAN, lang)

def enter(name: str, **args):
    print(tran.run("hello") name)
```
Running `slim hello Felix` with the language set to `en-us` will output "Hello!Felix".  

The `run` function has a priority:  
- First, try using `lang` in `TRAN`  
- => If it does not exist, try `en-us`  
- => If it still does not exist, use the first language  
- => Otherwise, an error is raised  

The `run` function also has a parameter: `content`, which indicates how to output the string. This parameter defaults to "<?>".  
When passing `content`, the "<?>" flag represents the translated output text.  

In the above example, you can use this method:  
```py
# enter/
print(tran.run("hello", f"<?>{name}")) 
```

For more complex scenarios, you can use `eval` to output, using the same example:  
```py
# TRAN/en-us/
{"hello": "f"Hello!{name}""}

# enter/
print(eval(tran.run("hello")))
```