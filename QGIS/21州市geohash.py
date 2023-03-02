import os
import sys
from qgis.gui import *
from qgis.core import *
import qgis.utils
from qgis.core import QgsProject
import pandas as pd
from collections import OrderedDict
import re

def write_file(filepath: str, contents: str):
    """将内容写入文件"""
    with open(filepath, 'a') as f:
        f.write(contents)


def getSelection():
    # 获取当前活动图层
    layer = iface.activeLayer()

    # 获取当前活动图层的名称
    layer_name = layer.name()

    selection = layer.selectedFeatures()
    print(len(selection))
    cityname = "达州市"
    filepath = r"C:\Users\Talie\Documents\四川省21市\%s" % cityname + ".txt"
    # print("filepath->"+filepath)
    return selection


def createPolygonXY(areaName: str, lalolist: list[str]):
    # 创建QgsPointXYlist
    qgsPointXYlist = []
    for str in lalolist:
        value = str.split(",")
        point = QgsPointXY(float(value[0]), float(value[1]))
        qgsPointXYlist.append(point)

    # 创建一个多边形几何对象

    polygon_geom = QgsGeometry.fromPolygonXY([qgsPointXYlist])

    # 创建一个多边形要素对象
    polygon_feature = QgsFeature()
    polygon_feature.setGeometry(polygon_geom)

    # 创建一个图层，并添加多边形要素
    polygon_layer = QgsVectorLayer("Polygon", areaName, "memory")
    polygon_layer.dataProvider().addFeatures([polygon_feature])

    # 将图层添加到QGIS中
    QgsProject.instance().addMapLayer(polygon_layer)


# 判断是否有环
def checkPolygon_geom(areaName: str, lalolist: list[str]):
    # 创建QgsPointXYlist
    qgsPointXYlist = []
    for str in lalolist:
        value = str.split(",")
        point = QgsPointXY(float(value[0]), float(value[1]))
        qgsPointXYlist.append(point)

    # 创建一个多边形几何对象

    polygon_geom = QgsGeometry.fromPolygonXY([qgsPointXYlist])
    if (polygon_geom.isGeosValid()):
        print(areaName)


def createPointXY(areaName: str, lalolist: list[str]):
    # 创建一个点矢量图层
    points_layer = QgsVectorLayer("Point", areaName, "memory")
    for str in lalolist:
        value = str.split(",")
        point = QgsPointXY(float(value[0]), float(value[1]))
        # 创建一个点要素
        point_feature = QgsFeature()
        point_feature.setGeometry(QgsGeometry.fromPointXY(point))
        points_layer.dataProvider().addFeatures([point_feature])
    # 添加图层到 QGIS
    QgsProject.instance().addMapLayer(points_layer)


def getExcelList(func, file_path: str):
    # 读取excel
    df = pd.read_excel(file_path)
    for i, row in df.iterrows():
        row_str = ','.join(row.astype(str))
        # 正则表达式
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        # 匹配的是列表
        areaname = pattern.findall(row_str)[0]
        lalo = row_str.replace(areaname + ",", "").replace("[", "").replace("]", "")
        # 将经纬度字符串转成list
        laloList = lalo.split(";")

        # createPolygonXY(areaname+"test",set(laloList))
        func(areaname, laloList)


def createPolygonBySelection():
    selection = getSelection()
    lalo = list()
    layer = iface.activeLayer()
    # 获取当前活动图层的名称
    layer_name = layer.name()
    for feature in selection:
        geometry = feature.geometry()  # 获取要素几何属性
        if geometry.type() == QgsWkbTypes.PointGeometry:  # 如果要素是点要素
            point = geometry.asPoint()  # 获取点的坐标
            value = str(point.x()) + "," + str(point.y())
            lalo.append(value)

    #    createPolygonXY()
    sortlist = getSortList(lalo)

    createPolygonXY(layer_name + "test", lalo)


def getSortList2(lalo: list[str]):
    vertices = list()
    resultList = list()
    for string in lalo:
        var = string.split(",")
        vertices.append((float(var[0]), float(var[1])))
    sorted_vertices = sort_polygon_vertices(vertices)
    # Find a starting point that is not the start or end point of any edge
    edges = [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]
    start_vertex = None
    for v in vertices:
        is_start_vertex = True
        for e in edges:
            if e[0] == v or e[1] == v:
                is_start_vertex = False
                break
        if is_start_vertex:
            start_vertex = v
            break
    # Connect vertices in order
    polygon_vertices = [start_vertex]
    current_vertex = start_vertex
    while True:
        next_vertex = None
        for v in vertices:
            if v != current_vertex and v not in polygon_vertices:
                if next_vertex is None:
                    next_vertex = v
                else:
                    cross_product = (v[0] - current_vertex[0]) * (next_vertex[1] - current_vertex[1]) - (
                            v[1] - current_vertex[1]) * (next_vertex[0] - current_vertex[0])
                    if cross_product > 0:
                        next_vertex = v
        if next_vertex == start_vertex:
            break
        polygon_vertices.append(next_vertex)
        current_vertex = next_vertex
        return polygon_vertices


def getSortList(lalo: list[str]):
    vertices = list()
    resultList = list()
    for string in lalo:
        var = string.split(",")
        vertices.append((float(var[0]), float(var[1])))
    sorted_vertices = sort_convex_polygon_vertices(vertices)
    sorted_vertex_list = [(str(x), str(y)) for x, y in sorted_vertices]
    print(sorted_vertex_list)
    for x, y in sorted_vertex_list:
        resultList.append(str(x) + "," + str(y))
    return resultList


def sort_polygon_vertices2(vertices):
    # 找到最左边的顶点
    start_vertex = min(vertices, key=lambda v: (v[0], v[1]))
    # 从起点开始按顺序添加顶点到新的列表中
    sorted_vertices = [start_vertex]
    current_vertex = start_vertex
    vertices.remove(start_vertex)
    while vertices:
        next_vertex = min(vertices, key=lambda v: distance(current_vertex, v))
        sorted_vertices.append(next_vertex)
        current_vertex = next_vertex
        vertices.remove(next_vertex)

    return sorted_vertices


def sort_polygon_vertices(vertices):
    # 计算重心
    n = len(vertices)
    cx = sum(x for x, y in vertices) / n
    cy = sum(y for x, y in vertices) / n

    # 平移到重心
    vertices = [(x - cx, y - cy) for x, y in vertices]

    # 计算极角
    angles = [math.atan2(y, x) for x, y in vertices]

    # 按极角排序
    sorted_indices = sorted(range(n), key=lambda i: angles[i])
    sorted_vertices = [vertices[i] for i in sorted_indices]

    # 平移回原来的坐标系
    sorted_vertices = [(x + cx, y + cy) for x, y in sorted_vertices]

    return sorted_vertices
import math

def sort_convex_polygon_vertices(vertices):
    # 计算凸多边形重心
    centroid = [sum([v[0] for v in vertices])/len(vertices), sum([v[1] for v in vertices])/len(vertices)]
    # 将顶点按照极角从小到大排序
    vertices.sort(key=lambda v: math.atan2(v[1]-centroid[1], v[0]-centroid[0]))
    # 输出排序后的顶点
    return vertices


def distance(p1, p2):
    # 计算两个点之间的距离
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def main():
#    createPolygonBySelection()
    # 形成点或者图形
    excel_file = r"D:\develop\GeohashTest\QGIS\四川省21市.xlsx"
    getExcelList(createPointXY,excel_file)
    # 打印选中点


main()