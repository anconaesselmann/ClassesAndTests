import threading

from Command import Command

class CommandExecutionThread(threading.Thread):
    def __init__(self, commandString):
        self.commandString = commandString
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        self.result = Command(self.commandString).runAndGetOutputString()