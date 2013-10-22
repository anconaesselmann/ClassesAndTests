import subprocess

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