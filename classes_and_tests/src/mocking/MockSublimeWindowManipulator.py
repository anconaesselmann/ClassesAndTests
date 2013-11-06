"""
@author Axel Ancona Esselmann
"""
class MockSublimeWindowManipulator:
    def __init__(self):
        self.fileOpened = None
        self.cursors = None
    def openFile(self, aPath, cursors):
        self.fileOpened = aPath
        self.cursors = cursors
        return True