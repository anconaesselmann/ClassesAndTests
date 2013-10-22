import threading
import time

from Command import Command

class MultipleCommandExecutionThread(threading.Thread):
    def __init__(self):
        self.reset()
        threading.Thread.__init__(self)

    def setCommandString(self, commandString):
        self._commandString = commandString

    def getResult(self):
        return self._scriptResponse

    def stop(self):
        self._stop = True

    def hasRun(self):
        return self._hasRun

    def reset(self):
        self._stop = False
        self._hasRun = False
        self._scriptResponse = None
        self._commandString = None

    def run(self):
        while not self._stop:
            if not self._hasRun and self._commandString is not None:
                command = Command(self._commandString)
                self._scriptResponse = command.runAndGetOutputString()
                self._hasRun = True
            else:
                time.sleep(0.1)
        print "exiting loop"