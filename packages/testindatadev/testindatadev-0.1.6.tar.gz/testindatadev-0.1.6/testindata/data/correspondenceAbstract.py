from abc import abstractmethod, ABCMeta
from testindata.dataset.file import File

class CorrespondenceAbstract(metaclass=ABCMeta):
    def __init__(self):
        self.filePathList = []
        self.fileAnnDict = {}

    @abstractmethod
    def AddFiles(self) -> File:pass

