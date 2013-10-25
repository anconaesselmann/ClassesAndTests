import threading
import time

try:
    from Command import Command
except ImportError:
    from .Command import Command

DEBUG = True

class MultipleCommandExecutionThread(threading.Thread):
    def __init__(self, command=None, argument=None):
        self.reset()
        self._command = command
        self._argument = argument
        threading.Thread.__init__(self)

    def setCommand(self, command):
        self._command = command

    def setArgument(self, argument):
        self._argument = argument

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
        self._command = None
        self._argument = None

    def run(self):
        while not self._stop:
            #print "hasRun: " + str(self._hasRun) + ", command: " + str(self._command) + ", argument: " + str(self._argument)
            if not self._hasRun and self._command is not None and self._argument is not None:
                #print("executing command: " + self._command + " " + self._argument)
                command = Command(self._command, self._argument)
                self._scriptResponse = command.runAndGetOutputString()
                self._hasRun = True
                #print("result: " + str(self._scriptResponse))
            else:
                #print("not executing command")
                time.sleep(0.1)
        if DEBUG:
            print("ending MultipleCommandExecutionThread")