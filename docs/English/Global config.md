# This article will explain how to configure `setting.json`
> Why do we need `setting.json`?
> `setting.json` stores all global settings, and without it, the program will not run properly.
## Example
```json
{
  "language": "en-us",
  "commandConfig": "command.json",
  "commandDir": "command",
  "debug": false
}
```

- `language` is the global language, for example, en-us, which means all commands will output/log in English.
- `commandConfig` is the command configuration; `command.json` indicates that all command configurations are stored in this file.
- `commandDir` is the folder for command invocation; after reading `commandConfig`, the files will be called from this folder.
- `debug` is a global switch, which can be used by commands to modify some logic when enabled.