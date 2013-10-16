#Classes and Tests (beta) 

####A file creator and test runner for PSR-0 name-spaced class and test files
(For now Smart Templates supplied are for php and phpUnit)

###Features
Create new class files with their corresponding test files from "smart templates".  
Type `,`, `n` to open the file creation panel and enter the new file name. Folders are created automatically.
![alt text](/images/demo_01_create_class_and_test.gif "Demo of simultaneous Class and Test creation")
If your test files live in a separate directory tree that mirrors your source code directory tree, 
the test files are automatically placed in the correctdirectory-branch.

![alt text](/images/demo_02_create_test.gif "Demo of simultaneous Class and Test creation")

![alt text](/images/demo_03_run_tests.gif "Demo of simultaneous Class and Test creation")

![alt text](/images/demo_04_run_test_suite.gif "Demo of simultaneous Class and Test creation")


To enable vintage mode key bindings add these to your user-key-bindings:

```
{   "keys": [",", "n"],
    "command": "classes_and_tests",
    "context":[{"key": "setting.vintage_ctrl_keys"},{"key": "setting.command_mode"}]
},
{   "keys": [",", "t"],
    "command": "toggle_source_test",
    "context":[{"key": "setting.vintage_ctrl_keys"},{"key": "setting.command_mode"}]
},
{   "keys": [",", "r"],
    "command": "run_php_unit_tests",
    "context":[{"key": "setting.vintage_ctrl_keys"},{"key": "setting.command_mode"}]
},
{   "keys": [",", ",", "r"],
    "command": "run_php_unit_tests", "args": {"run_test_suite": true},
    "context":[{"key": "setting.vintage_ctrl_keys"},{"key": "setting.command_mode"}]
},
{   "keys": [",", "r"],
    "command": "hide_panel", "args": {"cancel": true},
    "context":[{"key": "setting.vintage_ctrl_keys"},{"key": "setting.command_mode"},{ "key": "panel_visible", "operator": "equal", "operand": true }]
}
```



Known issues:
Currently only key-bindings for Mac exist.

I am a freelance software engineer, if this plugin is useful to you, please considder supporting me with a donation!

<a href='https://pledgie.com/campaigns/22419'><img alt='Click here to lend your support to: Support the software you use! and make a donation at www.pledgie.com !' src='https://github.com/anconaesselmann/ClassesAndTests/raw/master/images/donate.png' border='0' ></a>
