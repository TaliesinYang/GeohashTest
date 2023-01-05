import decimal
from typing import List
import pygeohash as pgh
from utils.FileUtils import FileUtil
from utils.ProjectionUtils import ProjectionUtils
from utils.ShapelyUtils import ShapelyUtils
import concurrent.futures


def plus(self: decimal):
    # 小数点后11 位精确到10米 10位精确到100米 9位精确到几百米
    return self.quantize(decimal.Decimal("0.0000001"), rounding=decimal.ROUND_HALF_UP) + decimal.Decimal('0.0000001')


def thread_func(x, y, polygon, reslutSet: set, projectionUtil: ProjectionUtils, shapelyUtils: ShapelyUtils):
    Y = decimal.Decimal(y)
    x = decimal.Decimal(x)
    while (y <= maxY):
        y = plus(y)
        projectTuple = projectionUtil.mapping(float(x), float(y))
        # print(shapelyUtils.ifPolygon(polygon, float(x), float(y)))
        if shapelyUtils.ifPolygon(polygon, projectTuple[0], projectTuple[1]):
            result=projectionUtil.unmapping(float(projectTuple[0]),float(projectTuple[1]))
            # print(result)
            #  反映射成经纬度列表
            reslutSet.add(result)


if __name__ == '__main__':
    # 1.使用工具类读取文件
    helper = FileUtil()
    contents: str = helper.read_file('../myfile.txt')
    strList: list[str] = contents.split("\n")
    result: str = ""
    tupleList: list = list()
    projectionUtil = ProjectionUtils()
    possiblePoints: list = list()
    projectList: list = list()
    # 2.将文件按行读取并且进行切割
    for x in strList:
        tempList: list[str] = x.split(" ")
        # 将每一行的数据进行映射并且放到list中
        tuple = (tempList[0], tempList[1])
        tupleList.append(tuple)
        projectTuple = projectionUtil.mapping(tempList[0], tempList[1])
        projectList.append(projectTuple)
    XList = list()
    Ylist = list()
    for x in tupleList:
        XList.append(x[0])
        Ylist.append(x[1])
    XList.sort()
    print(XList)
    # 3.计算list的最大值和最小值
    maxX: decimal = decimal.Decimal(max(XList))
    minX: decimal = decimal.Decimal(min(XList))
    maxY: decimal = decimal.Decimal(max(Ylist))
    minY: decimal = decimal.Decimal(min(Ylist))
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
    shapelyUtils = ShapelyUtils()
    x: decimal = decimal.Decimal(minX)
    y: decimal = decimal.Decimal(minY)
    polygon = shapelyUtils.getPolygon(projectList)
    resultSet = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        while (x <= maxX):
            x = plus(x)
            future = executor.submit(thread_func,x, y, polygon, resultSet, projectionUtil, shapelyUtils)
    # helper.write_file("includedPoints.txt","".join(includedPoints))
    geohashSet = set()
    for point in resultSet:
        # print(point)
        geohash = pgh.encode(point[0], point[1], precision=7)
        geohashSet.add(geohash)
    print(geohashSet.__sizeof__())

    for x in geohashSet:
        print(x)
        result = str(x) + "\n" + result
    helper.write_file("output.txt", result)
