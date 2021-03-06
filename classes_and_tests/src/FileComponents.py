import os

##
# A class that breaks a file or folder path into it's components
#
class FileComponents():
    def __init__(self, path):
        self._defaultExtension = None
        self.set(path)

    # TODO: implement this
    def setDefaultExtension(self, extension):
        self._defaultExtension = extension
        self._applyDefaultExtension()

    def _applyDefaultExtension(self):
        if self._defaultExtension is not None :
            extension = self.getExtension()
            if extension is None or extension == "":
                oldPath = self._path
                basePath = self._basePath
                #print("<< path: " + str(path) + ", basePath: " + str(basePath))
                self.set(oldPath + "." + self._defaultExtension)
                #print("<<<< path: " + str(path) + ", basePath: " + str(basePath))
                try:
                    self.setBasePath(basePath)
                except Exception as e:
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
                    pass


    def set(self, path):
        if path is None:
            path = ""

        if path != "":
            path = os.path.normpath(path)
            path, extension = os.path.splitext(path)
            #print("path: " + path + ", ext: " + extension)
        else:
            extension = ""
        if extension != "":
            self._extension = extension[1:]
            self._isFile = True
            self._path, self._file = os.path.split(path)
            #print self._path + self._file
        else:
            """if path[0:1] == ".":
                self._extension = None
                self._isFile = True
                self._path = ""
                self._file = path
            else:"""
            self._extension = None
            self._isFile = False
            self._path = path
            self._file = None

            if path == ".":
                #print(path)
                pass
        if self._path[:len(os.sep)] == os.sep:
            self._pathIsAbsolute = True
        else:
            self._pathIsAbsolute = False
        self._basePath = None
        self._applyDefaultExtension()

    def pathIsAbsolute(self):
        if self._pathIsAbsolute:
            return True
        else:

            if self._basePath is not None:
                return True
            else:
                return False

    ## (unitTested)
    # If the path is relative, or if an absolute path was given, but
    # one would like to specify a base path within that absolute path,
    # this function sets the base path.
    #
    # @throws Exception: Thrown when providing a base path for an absolute path,
    #                    and the base path is not the beginning of the
    #                    absolute path
    #
    def setBasePath(self, basePath=None):
        if basePath is None or basePath == "":
            return
        basePath = os.path.normpath(basePath)
        if self._pathIsAbsolute == False:
            self._basePath = basePath
        else:
            error = True
            lenBasePath = len(basePath)
            lenPath = len(self._path)
            #print("<<<<<<<<<<<< path: " + str(self._path) + ", basePath: " + str(basePath))


            if lenPath >= lenBasePath:
                suspect = self._path[:lenBasePath]
                if suspect == basePath:
                    relativePath = self._path[lenBasePath:]
                    error = False
                    self._basePath = basePath
            if error:
                raise Exception("Setting a base path for an absolute path where the base path is not the beginning of the absolute path:\nBase path: " + basePath + "\nPath: " + self._path)

    ## (unitTested)
    def getBasePath(self):
        return self._basePath

    ## (unitTested)
    def isFile(self):
        return self._isFile

    ## (unitTested)
    # Returns the file extension without the period
    #
    def getExtension(self):
        return self._extension

    ## (unitTested)
    # Returns the file name without it's path or file extension
    #
    def getFile(self):
        return self._file

    ## (unitTested)
    # Returns the relative path without a file name, provided either a
    # base path was given, or the path given when set() was called was
    # not an absolute path, otherwise returns None.
    #
    def getRelativePath(self):
        if self.pathIsAbsolute() == True and self._basePath is None:
            return None
        if self._basePath != None and self._pathIsAbsolute:
            lenBasePath = len(self._basePath)
            lenPath = len(self._path)
            if lenPath >= lenBasePath:
                suspect = self._path[:lenBasePath]
                if suspect == self._basePath:
                    if self._path[lenBasePath:lenBasePath + len(os.sep)] == os.sep:
                        lenBasePath += len(os.sep)
                    relativePath = self._path[lenBasePath:]
                    return relativePath
        relativePath = self._path
        if relativePath == "":
            relativePath = None
        return relativePath

    ## (unitTested)
    # Returns the file name with extension and relative path, provided
    # either a base path was given, or the path given when set() was called
    # was not an absolute path, otherwise returns None.
    #
    def getRelativeFileName(self):
        if self.pathIsAbsolute() == True and self._basePath is None:
            return None
        if self._isFile:
            if self.getRelativePath() is not None:
                return os.path.join(self.getRelativePath(), self.getFile() + "." + self.getExtension())
        else:
            return None

    ##
    # Returns the absolute path without file name, if the file path provided
    # when set() was called was absolute, or a base path was provided with
    # setBasePath(), otherwise returns None.
    #
    def getAbsolutePath(self):
        if self.pathIsAbsolute() == False:
            return None
        if self._pathIsAbsolute == False and self._basePath != None:
            absolutePath = os.path.join(self._basePath, self._path)
        else:
            absolutePath = self._path
        return absolutePath

    ## (unitTested)
    # Returns the file name with extension and absolute path, if the file path
    # provided when set() was called was absolute, or a base path was provided
    # with setBasePath(), otherwise returns None.
    #
    def getAbsoluteFileName(self):
        if self.pathIsAbsolute() == False:
            return None
        if self._isFile:
            return os.path.join(self.getAbsolutePath(), self.getFile() + "." + self.getExtension())
        else:
            return None

    ##
    # Returns the absolute path without file name, or the relative path without
    # file name, if no absolute path was provided.
    #
    def getDir(self):
        directory = self.getAbsolutePath()
        if directory is None:
            directory = self.getRelativePath()
        return directory

    ##
    # Returns the file name with extension and absolute path, or the relative
    # the file name with extension and relative path, if no absolute path was
    # provided, or None when no file name was provided
    #
    def getFileName(self):
        fileName = self.getAbsoluteFileName()
        if fileName is None:
            fileName = self.getRelativeFileName()
        return fileName