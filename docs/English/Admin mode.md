# This article will cover all the commands in Operator Mode and how to use them

## How to Run Operator Mode
```bash
# This is how you usually use SLIM
slim script subscript args...
# But to use operator mode, you need to prefix it with the --admin logo
slim --admin adminscript args...
```

## help
### Example
```bash
slim --admin help
slim --admin help fex
```
### Parameter format
```bash
slim --admin help [id]
```
## Parsing
If there is no id parameter, the ID of all commands and its parameter format are directly output
For example, 'slim --admin help'
```txt
file : -
file.add : - <path>
file.del : - <path>
file.load : - <path> [encoding:utf-8]
file.move : - <path> <newPath>
file.rename : - <path> <newName>
query : -
query.tree : - <mode> [data] [configs]
query.path : - [path]
query.cmd : - [id]
fex : - <path> [encoding:utf-8] [plugin]
```
If it contains an id parameter, output the ID and parameter format of the command
For example, 'slim --admin help fex'
```txt
fex : - <path> [encoding:utf-8] [plugin]
```

## create
### Example
```bash
slim --admin create
slim --admin create test
slim --admin create test "- <name>"
```
### Parameter format
```bash
slim --admin create [id] [format]
```
### Parsing
If neither the id parameter nor the format parameter is written, it scans the commandConfig and determines if the command ID is in the commandDir  
If not, create and write the parameters in 'commandDir'

If the 'id parameter' is written, the 'id' will be added to 'commandConfig' and 'commadnDir', but the parameter format is '-'

If you write the 'format parameter' and 'id parameter', this 'id' and the corresponding 'format' will be added to 'commandConfig' and 'commadnDir'