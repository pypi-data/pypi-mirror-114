from abc import abstractmethod, ABCMeta
import yaml
import os

class CorrespondAbstract(metaclass=ABCMeta):
    def __init__(self, cfPath):
        if os.path.exists(cfPath):
            with open(cfPath, "r", encoding="utf-8") as cf:
                self.conf = yaml.load(cf.read(), Loader=yaml.FullLoader)
        else:
            raise Exception(f"no such config file: {cfPath}")

    @abstractmethod
    def getFiles(self, pathDir) -> []:
        return []


    @abstractmethod
    def getAnnByFilePath(self, filePath) -> str:
        return ""
