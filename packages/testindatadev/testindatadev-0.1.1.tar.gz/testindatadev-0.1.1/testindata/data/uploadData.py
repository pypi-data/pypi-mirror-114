import yaml
import os

class UploadData():
    def __init__(self, format="voc", path="path/to/your/files", fe="jpg", apath="path/to/your/annotations", at="xml", afe="xml", ds_id="ds_*************"):
        if format not in ["voc", "coco", "customize"]:
            raise Exception("wrong data format type! ['voc', 'coco', 'customize'] are supported")

        self.format = format
        self.path = path
        self.fe = fe
        self.apath = apath
        self.at = at
        self.afe = afe
        self.dsId = ds_id

        self.configFilePath = os.path.join(os.path.abspath(os.curdir), self.format + "_upload_conf.yaml")
        self.scriptPath = os.path.join(os.path.abspath(os.curdir), self.format + "Correspondence.py")

        self.conf = None

        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, "r", encoding="utf-8") as cf:
                self.conf = yaml.load(cf.read(), Loader=yaml.FullLoader)



    def init(self):
        yamlText = f'''#请编辑此文件以进行后续操作
files:
  path: {self.path}          #需要上传的文件的路径
  extension: {self.fe}       #所有需要上传文件的扩展名，用于匹配文件用,可填用数组入多个
annotations:
  path: {self.apath}    #所有标注(识别)结果数据的路径
  format: {self.at}                       #所有标注数据的文件类型，此项设置用于指定数据解析
  extension: {self.afe}                #所有标注数据的文件扩展名，用于匹配文件用,可填用数组入多个，文件扩展名与文件内容的真实格式有时是不一样的
format: {self.format}                         #此项设置用于指定解析数据的数据格式，支持["voc", "coco", "customize"]之一，目前仅支持voc, coco格式，customize为用户自定义格式
dataset: {self.afe}         #用于指定需要上传至哪一个数据集
        '''

        # yamlExtraText = '''
        #     correspondence:
        #       scriptPath: path/to/your/correspondence.py #此项设置解决数据转换的问题，format设置为customize时此项必填，如果此项被设置，则format自动转为customize
        # '''

        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, "w", encoding="utf-8") as cf:
                cf.write("")

        with open(self.configFilePath, "a", encoding="utf-8") as cf:
            cf.write(yamlText)
            # if self.format not in ["voc", "coco"]:
            #     cf.write(yamlExtraText)

        print("successfully in TDA uploading-initialization，files bellow ware generated，please check and edit them for keep going：")
        print(self.configFilePath)
        if self.format not in ["voc", "coco"]:
            print(self.scriptPath)

    def appliy(self, cfPath, corrPath=""):
        self.configFilePath = cfPath
        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, "r", encoding="utf-8") as cf:
                self.conf = yaml.load(cf.read(), Loader=yaml.FullLoader)
        else:
            raise Exception(f"no such config file: {cfPath}")

        try:
            self.format = self.conf["format"]
            self.path = self.conf["files"]["path"]
            self.fe = self.conf["files"]["extension"]
            self.apath = self.conf["annotations"]["path"]
            self.at = self.conf["annotations"]["format"]
            self.afe = self.conf["annotations"]["extension"]
            self.dsId = self.conf["dataset"]
        except Exception as e:
            print(e)
            raise Exception(f"bad configuration: {cfPath}, please check or execute init again")



