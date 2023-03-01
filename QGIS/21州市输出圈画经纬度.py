import os
import sys
from qgis.gui import *
from qgis.core import *
import qgis.utils
from qgis.core import QgsProject


def write_file( filepath: str, contents: str):
    """将内容写入文件"""
    with open(filepath, 'a') as f:
        f.write(contents)


# 获取当前活动图层
layer = iface.activeLayer()

# 获取当前活动图层的名称
layer_name = layer.name()

selection = layer.selectedFeatures()
print(len(selection))
cityname = "test"
filepath = r"C:\Users\Talie\Documents\四川省21市\%s" % cityname+".txt"
print("filepath->"+filepath)
resultstr=""
flag=0
firstValue=""
for feature in selection:
    if flag == 0:
        firstValue=str(feature.attribute(1))+","+str(feature.attribute(2))+";\n"
    resultstr+=str(feature.attribute(1))+","+str(feature.attribute(2))+";\n"
    flag=1
write_file(filepath,cityname+"@@@")
write_file(filepath,resultstr)
write_file(filepath,firstValue)