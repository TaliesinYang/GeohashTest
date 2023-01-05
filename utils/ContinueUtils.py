import FileUtils
class ContinueUtils:
    # 记录已经执行到的最大经度

    # record文件说明，每一个记录使用|分割其中记录有
    # |longitude|longitudeUpdateTime|
    longitude:str
    def writeLongitudeRecord(self):
        FileUtils.FileUtil.write_file(None,"continueRecord.txt",)

    def splitChange(self,index,contents):
        # index start at 0
        str = FileUtils.FileUtil.read_file(None, "continueRecord.txt")
        recordList = str.split("|")
        recordList[index+1]=contents


