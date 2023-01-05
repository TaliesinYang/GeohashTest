import decimal
from typing import List
import pygeohash as pgh
from utils.FileUtils import FileUtil

from shapely.geometry import Polygon


def plus(self:decimal):
    # 小数点后11 位精确到10米 10位精确到100米 9位精确到几百米
    return self.quantize(decimal.Decimal("0.00000000001"), rounding=decimal.ROUND_HALF_UP) + decimal.Decimal('0.00000000001')


if __name__ == '__main__':
    # 1.使用工具类读取文件
    helper = FileUtil()
    contents: str = helper.read_file('../myfile.txt')
    strList: list[str] = contents.split("\n")
    result: str = ""
    coordinates = list()
    for x in strList:
        elem = x.split(" ")
        coordinates.append((float(elem[0]),float(elem[1])))
    print(str(coordinates))
    # 假设你有一个经纬度列表，例如 [(0, 0), (0, 1), (1, 1), (1, 0)]
    lng_lat_list = coordinates

    # 使用 Polygon 构造函数创建一个 Polygon 对象
    polygon = Polygon(lng_lat_list)

    # 使用 boundary 属性获取经纬度区域的边界
    boundary = polygon.boundary

    # 使用 boundary.coords 属性获取经纬度坐标列表
    lng_lat_coords = list(boundary.coords)

    # 输出经纬度坐标列表
    print(lng_lat_coords)


