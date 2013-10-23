import subprocess

class Command():
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument

    def run(self):
        process = subprocess.Popen([self.command, self.argument], shell=True, stdout = subprocess.PIPE,
                                                                              stderr=subprocess.STDOUT)
        returnCode = process.returncode
        return iter(process.stdout.readline, b'')

    def runAndPrintOutputLineByLine(self):
        for line in self.run():
            print(line.rstrip())

    def runAndGetOutputString(self):
        process = subprocess.Popen([self.command, self.argument], stdout=subprocess.PIPE,
                                                                  stderr=subprocess.PIPE)
        scriptResponse, scriptError = process.communicate()
        return scriptResponse + "\n" + scriptError

    def runAndPrintAllOutput(self):
        print(self.runAndGetOutputString())

"""
class Command():
    def __init__(self, commandString):
        self.commandString = commandString

    def run(self):
        process = subprocess.Popen(self.commandString, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
        returnCode = process.returncode
        return iter(process.stdout.readline, b'')

    def runAndPrintOutputLineByLine(self):
        for line in self.run():
            print(line.rstrip())

    def runAndGetOutputString(self):
        process = subprocess.Popen(self.commandString, shell=True, stdout = subprocess.PIPE)
        scriptResponse, scriptError = process.communicate()
        return scriptResponse

    def runAndPrintAllOutput(self):
        print(self.runAndGetOutputString())
"""