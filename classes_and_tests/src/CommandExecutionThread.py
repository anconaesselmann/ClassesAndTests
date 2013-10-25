import threading

try:
    from Command import Command
except ImportError:
    from .Command import Command

class CommandExecutionThread(threading.Thread):
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        self.result = Command(self.command, self.argument).runAndGetOutputString()

"""
class CommandExecutionThread(threading.Thread):
    def __init__(self, commandString):
        self.commandString = commandString
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        self.result = Command(self.commandString).runAndGetOutputString()
"""