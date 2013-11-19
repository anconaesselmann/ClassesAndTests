# Adapted from @skuroda,s PersistentRegexHighlight and @wbond's resource loader.

import sys
import sublime

#VERSION = int(sublime.version())

mod_prefix = "classes_and_tests"
reload_mods = []

"""
if VERSION > 3000:
    mod_prefix = "PersistentRegexHighlight." + mod_prefix
    from imp import reload
    for mod in sys.modules:
        if mod[0:24] == 'PersistentRegexHighlight' and sys.modules[mod] is not None:
            reload_mods.append(mod)
else:"""

for mod in sorted(sys.modules):
    testString = 'classes_and_tests'
    if mod[0:len(testString)] == testString and sys.modules[mod] is not None:
        reload_mods.append(mod)

mods_load_order = [
    '.src.Std',
    '.src.UnitTestFunctions',
    '.src.SublimeFunctions',
    '.src.SublimeWindowFunctions',
    '.src.SublimeWindowManipulator'
    '.src.UserSettings',
    '.src.FileComponents',
    '.src.MirroredDirectory',
    '.src.Command',
    #'.src.FileManipulation',
    '.src.FileSystem',
    #'.src.FileCreator',
    '.src.TemplateFileCreator',
    '.src.CommandExecutionThread',
    '.src.MultipleCommandExecutionThread',
    '.src.InputPanel',
    '.src.OutputPanel',
    '.src.LiveUnitTesting',
    '.TextInsert',
    '.ToggleSourcesTests',
    '.RunUnitTests',
    '.CreateMissingFunctions',
    '.ContinuousUnitTesting',
    '.ClassesAndTests'
    '.SyncronizeClassAndTestTabs',
    '.OutputPanelInsert',
    '.OutputPanelClear'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])