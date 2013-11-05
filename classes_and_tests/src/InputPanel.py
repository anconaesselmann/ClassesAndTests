DEBUG = True
UNIT_TEST_DEBUG = False

try:
    import sublime
except ImportError:
    from mocking.sublime import sublime
    if UNIT_TEST_DEBUG: 
        DEBUG = True
        print("InputPanel: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

class InputPanel():
    def __init__(self, sublimeViewInstance ,sublimeEditInstance):
        self.view = sublimeViewInstance
        self.region = None
        self.edit = sublimeEditInstance

    def selectAll(self):
        result = False
        for region in self.view.sel():
            if region.empty():
                self.region = self.view.line(region)
                result = True
        return result

    def getTextFromSelection(self):
        result = None
        if self.region is not None:
            result = self.view.substr(self.region)
        return result

    def getAllText(self):
        self.selectAll()
        lineText = self.getTextFromSelection()
        return lineText

    def replaceAllText(self, newText):
        self.selectAll()
        self.replaceSelectedText(newText)

    def replaceSelectedText(self, newLine):
        result = False
        if self.region is not None:
            self.view.replace(self.edit, self.region, newLine)
            self.newLine = newLine
            result = True
        return result

    # returns the new new line
    def deleteUntil(self, needle):
        lineText = self.getAllText()
        result = lineText
        if lineText is not None:
            index = lineText.rfind(needle);
            newLine = lineText[0:index + len(needle)]
            self.replaceSelectedText(newLine)
            result = newLine
        return result