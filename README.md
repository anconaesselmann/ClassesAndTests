#Classes and Tests (beta) 

####A smart-template-based file creator and test runner for PSR-0 name-spaced class and test files

###Features
####File Creation
* File creation is governed by "Smart Templates." Variables set in the settings file get read, 
  manipulated by a command defined in a `.variables` file, and inserted into a template. 
  Smart templates for projects using php in conjuction with phpUnit are provided.  

  *(Templates for other languages might be added in future versions but could be created by the user for now.)*

* Create new PSR-0 namespaced classes and their corresponding tests with the help of "smart templates".  
  Type `,`, `n` to open the file creation panel and enter the new file name. Folders are created automatically.
  ![alt text](/images/demo_01_create_class_and_test.gif "Demo of simultaneous Class and Test creation")
  If your test files live in a separate directory tree that mirrors your source code directory tree, 
  the test files are automatically placed in the correctdirectory-branch.

  Example:  
  if */MyProject/library/* is your code base and */MyProjec/library<b>Test</b>/* is the root of all your test files,
  the test file for  
  */MyProject/library/aae/mvc/Controller.php* 
  will be  
  */MyProject/library<b>Test</b>/aae/mvc/ControllerTest.php*



* Easyly create tests while editing a class or vice versa by pressing `,`, `t`.  
  If both the test and the class file already exist, `,`, `t` toggles back and forth between the two
  ![alt text](/images/demo_02_create_test.gif "Creating a Test file from a Class")
  
####Unit Testing
* Run tests for this class without leaving the editor
  ![alt text](/images/demo_03_run_tests.gif "Demo of simultaneous Class and Test creation")
* Run a test suite without leaving the editor
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
