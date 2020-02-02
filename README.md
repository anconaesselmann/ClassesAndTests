# LiveUnit (beta) 

#### A smart-template-based file creator and test runner for PSR-0 name-spaced class and test files

### Features
#### File Creation
* File creation is governed by "Smart Templates." Variables set in the settings file get read, 
  manipulated by a command defined in a `.variables` file, and inserted into a template. 
  Smart templates for projects using php in conjuction with phpUnit are provided.  

  *(Templates for other languages might be added in future versions but could be created by the user for now.)*

* Create new PSR-0 namespaced classes and their corresponding tests with the help of "smart templates".  
  Type `option` + `command` + `n` to open the file creation panel and enter the new file name. Folders are created automatically.
  ![alt text](/images/demo_01_create_class_and_test.gif "Demo of simultaneous Class and Test creation")
  If your test files live in a separate directory tree that mirrors your source code directory tree, 
  the test files are automatically placed in the correctdirectory-branch.

  Example:  
  if */MyProject/library/* is your code base and */MyProjec/library<b>Test</b>/* is the root of all your test files,
  the test file for  
  */MyProject/library/aae/mvc/Controller.php* 
  will be  
  */MyProject/library<b>Test</b>/aae/mvc/ControllerTest.php*



* Easyly create tests while editing a class or vice versa by pressing `option` + `command` + `tab`.  
  If both the test and the class file already exist, `option` + `command` + `tab` toggles back and forth between the two
  ![alt text](/images/demo_02_create_test.gif "Creating a Test file from a Class")
  
#### Unit Testing
* Run tests for this class without leaving the editor by pressing `option` + `command` + `u`.
  ![alt text](/images/demo_03_run_tests.gif "Demo of simultaneous Class and Test creation")


* Run a test suite without leaving the editor by pressing `option` + `command` + `shift` + `u`.
  ![alt text](/images/demo_04_run_test_suite.gif "Demo of simultaneous Class and Test creation")




Known issues:
Currently only key-bindings for Mac exist.

