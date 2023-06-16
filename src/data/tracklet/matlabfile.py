import os

import scipy.io

from src.utils.analysis import buildShortName


class MatlabFile:
    def __init__(self, path):
        self.path = path
        self.data = self.__loadMatFile(path=self.path)
        self.dataSetName = os.path.basename((self.data["export"]["baseDir"]))

        self.dataSetShortName = buildShortName(self.dataSetName)

    def __loadMatFile(self, path):
        """
        this function should be called instead of direct scipy.io.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects
        """
        data = scipy.io.loadmat(path, struct_as_record=False, squeeze_me=True)
        return self.__checkKeys(data)

    def __checkKeys(self, dictionary):
        """
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        """
        for key in dictionary:
            if isinstance(dictionary[key], scipy.io.matlab.mat_struct):
                dictionary[key] = self.__todict(dictionary[key])
        return dictionary

    def __todict(self, matlabObject):
        """
        A recursive function which constructs from matObjects nested dictionaries
        """
        dictionary = dict()
        for strg in matlabObject._fieldnames:
            elem = matlabObject.__dict__[strg]
            if isinstance(elem, scipy.io.matlab.mat_struct):
                dictionary[strg] = self.__todict(elem)
            else:
                dictionary[strg] = elem
        return dictionary
