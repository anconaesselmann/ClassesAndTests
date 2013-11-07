import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from classes_and_tests.src.FileComponents import FileComponents

data = [
    {"basePath": None                  ,"inputValue": "/A/path/To/a/file.txt"                                  , "extension": "txt"    , "className": "file"       , "fileName": "file"           , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": "/A/path/To/a/file.txt"                         },
    {"basePath": None                  ,"inputValue": "A/path/To/a/File.py"                                    , "extension": "py"     , "className": "File"       , "fileName": "File"           , "isFile": True , "basePathExeption": False, "isAbsolute": False, "relativePath": "A/path/To/a"                  , "relativeFileName": "A/path/To/a/File.py"                          , "absoluteFileName": None                                            },
    {"basePath": None                  ,"inputValue": "/A/path/To/a/file"                                      , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": True , "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": None                  ,"inputValue": "A/path/To/a/file"                                       , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": False, "relativePath": "A/path/To/a/file"             , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": None                  ,"inputValue": "/AClass.php"                                            , "extension": "php"    , "className": "AClass"     , "fileName": "AClass"         , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": "/AClass.php"                                   },
    {"basePath": ""                    ,"inputValue": "Main.html"                                              , "extension": "html"   , "className": "Main"       , "fileName": "Main"           , "isFile": True , "basePathExeption": False, "isAbsolute": False, "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": None                  ,"inputValue": ""                                                       , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": False, "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": ""                    ,"inputValue": ""                                                       , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": False, "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": ""                    ,"inputValue": None                                                     , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": False, "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": None                  ,"inputValue": None                                                     , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": False, "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": "/"                   ,"inputValue": "/"                                                      , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": True , "relativePath": ""                             , "relativeFileName": None                                           , "absoluteFileName": None                                            },
    {"basePath": "/"                   ,"inputValue": "/MyProject/library/scrTest/aae/MyClassTest.php"         , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": "MyProject/library/scrTest/aae", "relativeFileName": "MyProject/library/scrTest/aae/MyClassTest.php", "absoluteFileName": "/MyProject/library/scrTest/aae/MyClassTest.php"},
    {"basePath": "/MyProject/library/" ,"inputValue": "/MyProject/library/scrTest/aae/MyClassTest.php"         , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": "scrTest/aae"                  , "relativeFileName": "scrTest/aae/MyClassTest.php"                  , "absoluteFileName": "/MyProject/library/scrTest/aae/MyClassTest.php"},
    {"basePath": "/MyProject/library"  ,"inputValue": "/MyProject/library/scrTest/aae/MyClassTest.php"         , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": "scrTest/aae"                  , "relativeFileName": "scrTest/aae/MyClassTest.php"                  , "absoluteFileName": "/MyProject/library/scrTest/aae/MyClassTest.php"},
    {"basePath": "/MyProject/library/" ,"inputValue": "scrTest/aae/MyClassTest.php"                            , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": "scrTest/aae"                  , "relativeFileName": "scrTest/aae/MyClassTest.php"                  , "absoluteFileName": "/MyProject/library/scrTest/aae/MyClassTest.php"},
    {"basePath": "/MyProject/library"  ,"inputValue": "scrTest/aae/MyClassTest.php"                            , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": False, "isAbsolute": True , "relativePath": "scrTest/aae"                  , "relativeFileName": "scrTest/aae/MyClassTest.php"                  , "absoluteFileName": "/MyProject/library/scrTest/aae/MyClassTest.php"},
    {"basePath": "/MyProject/library"  ,"inputValue": "/scrTest/aae/MyClassTest.php"                           , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": True , "isAbsolute": True , "relativePath": None                           , "relativeFileName": None                                           , "absoluteFileName": "/scrTest/aae/MyClassTest.php"                  },
    {"basePath": "/MyProject/library"  ,"inputValue": "/MyProject/library/"                                    , "extension": None     , "className": None         , "fileName": None             , "isFile": False, "basePathExeption": False, "isAbsolute": True , "relativePath": ""                             , "relativeFileName": None                                           , "absoluteFileName": None                                            }

    #{"basePath": None                  ,"inputValue": ".DS_Store"                                              , "extension": None     , "className": None         , "fileName": ".DS_Store"      , "isFile": True, "basePathExeption": False,  "isAbsolute": False, "relativePath": None                             },
    #{"basePath": None                  ,"inputValue": "/MyProject/.DS_Store"                                   , "extension": None     , "className": None         , "fileName": ".DS_Store"      , "isFile": True, "basePathExeption": False,  "isAbsolute": False, "relativePath": None                             },

    #{"basePath": "MyProject/library"   ,"inputValue": "/scrTest/aae/MyClassTest.php"                           , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": True ,"isAbsolute": True,  "relativePath": "/scrTest/aae/MyClassTest.php"    },
    #{"basePath": "MyProject/library/"  ,"inputValue": "scrTest/aae/MyClassTest.php"                            , "extension": "php"    , "className": "MyClass"    , "fileName": "MyClassTest"    , "isFile": True , "basePathExeption": False,"isAbsolute": True,  "relativePath": "scrTest/aae/MyClassTest.php"     }
]

class FileComponentsTest(unittest.TestCase):
    def test___init__(self):
        aPath = "/file.txt"
        obj = FileComponents(aPath)

    def test_getExtension(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            result = fc.getExtension()
            self.assertEqual(record["extension"], result)

    def test_isFile(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            result = fc.isFile()
            self.assertEqual(record["isFile"], result)

    def test_getFile(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            result = fc.getFile()
            self.assertEqual(record["fileName"], result)

    def test_set_and_getBasePath(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            basePath = record["basePath"]
            try:
                fc.setBasePath(basePath)
                result = fc.getBasePath()
            except Exception, e:
                self.assertEqual(True, record["basePathExeption"])
                pass
            else:
                self.assertEqual(False, record["basePathExeption"])
                if basePath == "":
                    basePath = None
                if basePath is not None:
                    basePath = os.path.normpath(basePath)
                self.assertEqual(basePath, result)

    def test_pathIsAbsolute(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            if not record["basePathExeption"]:
                fc.setBasePath(record["basePath"])
            result = fc.pathIsAbsolute()
            self.assertEqual(record["isAbsolute"], result)

    def test_getRelativePath(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            if not record["basePathExeption"]:
                fc.setBasePath(record["basePath"])
            result = fc.getRelativePath()
            self.assertEqual(record["relativePath"], result)

    def test_getRelativeFileName(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            if not record["basePathExeption"]:
                fc.setBasePath(record["basePath"])
            result = fc.getRelativeFileName()
            self.assertEqual(record["relativeFileName"], result)

    def test_getAbsoluteFileName(self):
        global data
        for record in data:
            fc = FileComponents(record["inputValue"])
            if not record["basePathExeption"]:
                fc.setBasePath(record["basePath"])
            result = fc.getAbsoluteFileName()
            self.assertEqual(record["absoluteFileName"], result)

    def test_setDefaultExtension(self):
        aPath = "/MyProject/library/aae/mvc/Controller"
        defaultFileExtension = "php"
        expected = "/MyProject/library/aae/mvc/Controller.php"
        fc = FileComponents(aPath)
        fc.setDefaultExtension(defaultFileExtension)

        result = fc.getFileName()

        self.assertEqual(expected, result)

    def test_setDefaultExtension_call_set_after_setting_default_file_extension(self):
        aPath = "/Some/Thing/Completely/different.php"
        anotherPath = "/MyProject/library/aae/mvc/Controller"
        defaultFileExtension = "php"
        expected = "/MyProject/library/aae/mvc/Controller.php"
        fc = FileComponents(aPath)
        fc.setDefaultExtension(defaultFileExtension)
        fc.set(anotherPath)

        result = fc.getFileName()

        self.assertEqual(expected, result)

    def test_setDefaultExtension_get_base_path(self):
        aPath = "/MyProject/library/aae/mvc/Controller"
        basePath = "/MyProject/library/"
        defaultFileExtension = "php"
        expected = "/MyProject/library"
        fc = FileComponents(aPath)
        fc.setBasePath(basePath)

        fc.setDefaultExtension(defaultFileExtension)

        result = fc.getBasePath()

        self.assertEqual(expected, result)

    def test_setDefaultExtension_explicit_extension_provided(self):
        aPath = "/MyProject/library/aae/mvc/Controller.py"
        defaultFileExtension = "php"
        expected = "/MyProject/library/aae/mvc/Controller.py"
        fc = FileComponents(aPath)
        fc.setDefaultExtension(defaultFileExtension)

        result = fc.getFileName()

        self.assertEqual(expected, result)

    def test_setDefaultExtension_bugfix(self):
        # Applies in the following scenario:
        # a base path was set before a default file extension has been applied.
        # the former base path is not valid any more when old path is equal to
        # the base path:
        #       old path: /MyProject/library
        #       base path: /MyProject/library
        #       default extension is set to .php
        #       the new path is /MyProject/library.php
        #       rendering the old base path is invalid
        # the moral of the story: default file extensions should be 
        # applied before setting a base path!
        aPath = "/MyProject/library"
        basePath = "/MyProject/library/"
        defaultFileExtension = "php"
        expected = "/MyProject/library.php"
        fc = FileComponents(aPath)
        fc.setBasePath(basePath)
        fc.setDefaultExtension(defaultFileExtension)

        result = fc.getFileName()

        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()