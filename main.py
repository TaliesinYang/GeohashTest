import decimal
from typing import List
import pygeohash as pgh
from utils.FileUtils import FileUtil
from utils.ProjectionUtils import ProjectionUtils
from utils.ShapelyUtils import ShapelyUtils
import cv2
import numpy as np
import concurrent.futures
import time

def plus(self:decimal):
    # 小数点后11 位精确到10米 10位精确到100米 9位精确到几百米
    return self.quantize(decimal.Decimal("0.000000000001"), rounding=decimal.ROUND_HALF_UP) + decimal.Decimal('0.00000000005')

def printShape():
    helper = FileUtil()
    contents: str = helper.read_file('myfile.txt')
    strList: list[str] = contents.split("\n")
    result: str = ""
    projectList: list = list()
    projectionUtil = ProjectionUtils()
    possiblePoints: list = list()
    # 2.将文件按行读取并且进行切割
    for x in strList:
        tempList: list[str] = x.split(" ")
        # 将每一行的数据进行映射并且放到list中
        print(x)
        tuple = projectionUtil.mapping(tempList[1], tempList[0])
        projectList.append(tuple)
    img = np.ones((512, 512, 3))  # 白色背景
    color = (0, 255, 0)  # 绿色
    # 五角星
    pts = np.array(projectList)
    pts = pts.reshape((-1, 1, 2))  # reshape为10x1x2的numpy
    print(pts.shape)  # (10, 1, 2)
    cv2.polylines(img, [pts], True, color, 5)
    # 方形
    pts = np.array([[10, 50], [100, 50], [100, 100], [10, 100]])
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, color, 3)

    cv2.imshow('juzicode.com', img)
    cv2.waitKey()

def process_data(x,y,maxY,polygon,possiblePoints):
    while (y <= maxY):
        print(y)
        includedPoints: list = list()
        y = plus(y)

        # print(shapelyUtils.ifPolygon(polygon, float(x), float(y)))
        if shapelyUtils.ifPolygon(polygon, float(x), float(y)):
            possiblePoints.append((float(x), float(y)))
            # 反映射成经纬度列表
            includedPoints.append(projectionUtil.unmapping(float(x), float(y)))
        for point in includedPoints:
            geohash = pgh.encode(point[0], point[1], precision=7)
            result = str(geohash) + "->" + str(point[0]) + "," + str(point[1]) + ";\n"
            helper.write_file("output.txt", result)


def start():

    helper = FileUtil()
    contents: str = helper.read_file('myfile.txt')
    strList: list[str] = contents.split("\n")
    result: str = ""
    projectList: list = list()
    projectionUtil = ProjectionUtils()
    possiblePoints:list=list()
    # 2.将文件按行读取并且进行切割
    for x in strList:
        tempList: list[str] = x.split(" ")
        # 将每一行的数据进行映射并且放到list中
        tuple = projectionUtil.mapping(tempList[0], tempList[1])
        projectList.append(tuple)
    XList = list()
    Ylist = list()
    for x in projectList:
        XList.append(x[0])
        Ylist.append(x[1])
    XList.sort()
    # print(XList)
    # 3.计算list的最大值和最小值
    maxX:decimal = decimal.Decimal(max(XList))
    minX:decimal = decimal.Decimal(min(XList))
    maxY:decimal = decimal.Decimal(max(Ylist))
    minY:decimal = decimal.Decimal(min(Ylist))
    print(maxY - minY)
    print(maxX - minX)
    #
    print(maxX)
    print(minX)
    # print(maxY)
    # print(minY)
    #
    print(plus(maxX))
    print(plus(minX))
    # 4.计算出所有可能的点
    shapelyUtils=ShapelyUtils()
    polygon=shapelyUtils.getPolygon(projectList)
    x:decimal=decimal.Decimal(minX)
    y:decimal=decimal.Decimal(minY)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        while(x<=maxX):
            x=plus(x)
            y= decimal.Decimal(minY)
            future=executor.submit(process_data,x,y,maxY,polygon,possiblePoints)

    # helper.write_file("includedPoints.txt","".join(includedPoints))


if __name__ == '__main__':
    # 1.使用工具类读取文件
    # printShape()
    start()