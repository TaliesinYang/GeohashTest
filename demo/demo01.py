import decimal
from typing import List
import pygeohash as pgh
from utils.FileUtils import FileUtil
from utils.ProjectionUtils import ProjectionUtils
from utils.ShapelyUtils import ShapelyUtils

def plus(self:decimal):
    # 小数点后11 位精确到10米 10位精确到100米 9位精确到几百米
    return self.quantize(decimal.Decimal("0.000001"), rounding=decimal.ROUND_HALF_UP) + decimal.Decimal('0.000005')


if __name__ == '__main__':
    # 1.使用工具类读取文件
    helper = FileUtil()
    contents: str = helper.read_file('../myfile.txt')
    strList: list[str] = contents.split("\n")
    result: str = ""
    projectList: list = list()
    projectionUtil = ProjectionUtils()
    possiblePoints:list[(int,int)]=list()
    # 2.将文件按行读取并且进行切割
    for x in strList:
        tempList: list[str] = x.split(" ")

        # 将每一行的数据进行映射并且放到list中
        # tuple = projectionUtil.mapping(tempList[0], tempList[1])
        # long(2.22)
        projectList.append((float(tempList[0]) , float(tempList[1])))
    print(projectList)

    XList = list()
    Ylist = list()
    for x in projectList:
        XList.append(x[0])
        Ylist.append(x[1])
    XList.sort()
    print(XList)
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
    # ShapelyUtils = ShapelyUtils()
    # # polygon_coords = [(1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (2.0, 1.0)]
    # polygon_coords = [(105.38027244991371845, 31.1478304403225934), (105.37929596963334689, 31.14655777012507087),
    #                   (105.378177040338187, 31.14669371973940315)]
    # polygon = ShapelyUtils.getPolygon(polygon_coords)
    shapelyUtils=ShapelyUtils()
    polygon=shapelyUtils.getPolygon(projectList)
    print(polygon)
    x:decimal=decimal.Decimal(minX)
    y:decimal=decimal.Decimal(minY)
    includedPoints:list=list()
    while(x<=maxX):
        x=plus(x)
        Y= decimal.Decimal(minY)
        while(y<=maxY):
            y=plus(y)
            print(shapelyUtils.ifPolygon(polygon, float(x), float(y)))
            if shapelyUtils.ifPolygon(polygon, float(x), float(y)):
                possiblePoints.append((float(x),float(y)))
                # 反映射成经纬度列表
                includedPoints.append((float(x),float(y)))
    # helper.write_file("includedPoints.txt","".join(includedPoints))
    geohashSet = set()
    for point in includedPoints:
        # print(point)
        geohash = pgh.encode(point[0], point[1], precision=7)
        geohashSet.add(geohash)
    print(geohashSet.__sizeof__())

    for x in geohashSet:
        print(x)
        result=str(x)+"\n"+result
    helper.write_file("output.txt",result)



