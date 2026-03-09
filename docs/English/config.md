# This article explains how to configure `command.json`

## Example
```json
{
"status": "-",
"scan": "- <mode> [timeout:10] @targets(^[a-z] $):3",
"upload": "- @files(.png$)"
}
```

## Parameter Concepts
`"script": "Here is the parameter format. Fill in parameters within the format, and separate parameters with spaces"`
| Symbol | Example | Definition |
| :---: | :--- | :--- |
| **`-`** | `-` | Represents the command itself |
| **`<Required Parameter>`** | `<file>` | Forces the user to input; error if missing |
| **`[Optional Parameter]`** | `[debug]` | User input is optional; defaults to `None` if missing |
| **`[Optional Parameter:Default]`** | `[port:8080]` | Uses the default value if user does not input |
| **`@Array Parameter`** | `@src` | Automatically collects all remaining parameters into a list |
| **`@Array Parameter(Regex)`** | `@log(.txt$)` | List items must match the regex, otherwise set to `None` |
| **`@Array Parameter:Length`** | `@vec:3` | Forces the list length to 3; fill with `None` if insufficient |

**Note**: Each parameter format must be prefixed with `-` or `- `. If there are additional parameters following, use `- `; otherwise, use `-`. 
If the parameter format only has `-`, it directly calls the `enter` function.
Regex for array parameters can also be combined with length: `- @args(d):5` means take the last 5 parameters that match the regex.

## Command ID
`"This is the command ID used to specify where the command is called": "format"`
It is important to note that the ID must be written in the file referenced by `commandConfig` in your `setting.json`.
Also, IDs must be separated by a `.`. For example, `file.add` indicates `commandDir/file/add.py`, where `file` represents `commandDir/file.py`.