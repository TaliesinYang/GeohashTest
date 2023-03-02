import os
import re

def clear_parentheses(content):
    return re.sub(r'[\(\)]', '', content)

def clear_folder(folder_path):
    results = []
    # 搜索文件夹下的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 读取文件内容
            with open(file_path, 'r') as f:
                content = f.read()
            # 清除(和)字符
            new_content = clear_parentheses(content)
            results.append((file, new_content))
    return results


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

def main():
    laloList=clear_folder(r"C:\Users\Administrator\Desktop\lalo\lola2")
    for var in laloList:
        createPolygonXY(var[0],var[1].split(","))
if __name__ == '__main__':
    main()
main()