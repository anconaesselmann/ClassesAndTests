"""
@author Axel Ancona Esselmann
"""

def dataProvider(dataProviderFunction):
    def decorator(testFunction):
        def testRunner(self, *args):
            counter = 1
            allData = dataProviderFunction(self)
            allDataContainerType = allData.__class__.__name__
            if allDataContainerType != "list":
                raise Exception("Data Providers have to return lists. '" + allDataContainerType + "' passed instead.")
            for testCaseArguments in allData:
                containerType = testCaseArguments.__class__.__name__
                if containerType != "list":
                    raise Exception("Data Providers have to return lists of lists. Item " + str(counter) + " in the returned list is of type '" + containerType + "' instead.")
                try:
                    testFunction(self, *testCaseArguments)
                except Exception, e:
                    print("ERROR:\nTest failed with data set " + str(counter) + ":")
                    print(testCaseArguments)
                    raise
                counter += 1
        return testRunner
    return decorator