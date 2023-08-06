from testindata.data.correspondenceAbstract import CorrespondenceAbstract
from testindata.TDA import TDA
from pascal_voc_tools import PascalXml

class VocCorrespondence(CorrespondenceAbstract):
    def __init__(self, upData, tda:TDA):
        self.upData = upData
        self.tda = tda

        print(self.upData.conf)
        print(self.upData.filePathList[0:10])
        print(self.upData.annPathList[0:10])

        # print(self.upData.format)
        # print(self.upData.path)
        # print(self.upData.fe)
        # print(self.upData.apath)
        # print(self.upData.at)
        # print(self.upData.afe)
        # print(self.upData.dsId)



        if self.upData.format != "voc":
            raise Exception("VocCorrespondence support voc format dataset only")

        if self.upData.at != "xml":
            raise Exception("voc format data accepts xml contents")

    def GetCorrespondence(self):
        """
        get files and annotation correspondence
        """
        # print(self.upData.filePathList[0:10])
        # print(self.upData.annPathList[0:10])

        ret = {}

        kList = {}
        for fpath in self.upData.filePathList:
            k = "".join(fpath.replace(self.upData.path, "").split(".")[:-1]).lstrip("/").lstrip("\\")
            kList[k] = fpath

        vList = {}
        for annPath in self.upData.annPathList:
            v = "".join(annPath.replace(self.upData.apath, "").split(".")[:-1]).lstrip("/").lstrip("\\")
            vList[v] = annPath

        for name, path in kList.items():
            ret[kList[name]] = vList[name]

        return ret


    def AddFiles(self):
        fileAndAnn = self.GetCorrespondence()
        for filePath, annPath in fileAndAnn.items():
            fileMetaData = {
                "format":self.upData.format,
                "extension":filePath.split(".")[-1]
            }

            objectName = filePath.replace(self.upData.path, "").strip("/")
            f = self.tda.AddFile(filePath, objectName=objectName, metaData=fileMetaData)

            x = PascalXml()
            x.load(annPath)
            for obj in x.object:
                box = {
                    "x":obj.bndbox.xmin,
                    "y":obj.bndbox.ymin,
                    "width":obj.bndbox.xmax - obj.bndbox.xmin,
                    "height":obj.bndbox.ymax - obj.bndbox.ymin
                }

                attrs = {
                    "pose":obj.pose,
                    "truncated":obj.truncated,
                    "difficult":obj.difficult,
                }

                f.AddBox2D(box, label=obj.name, attrs=attrs)

            annMetaData = {
                "format":self.upData.format,
                "extension":annPath.split(".")[-1]
            }

            annObjectName = annPath.replace(self.upData.path, "").strip("/")
            self.tda.AddFile(annPath, objectName=annObjectName, metaData=annMetaData)



