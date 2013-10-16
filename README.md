Classes and Tests (beta) 

A file creator and test runner for PSR-0 name-spaced class and test files (Templates supplied are for php and phpUnit)

![alt text](/images/demo1.gif "Demo of simultaneous Class and Test creation")



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

<a href='https://pledgie.com/campaigns/22419'><img alt='Click here to lend your support to: Support the software you use! and make a donation at www.pledgie.com !' src='/images/donate.png?skin_name=chrome' border='0' ></a>
