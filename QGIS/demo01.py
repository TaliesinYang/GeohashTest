import pandas as pd

import re
def createPolygonXY(areaName:str,lalolist: list[str]):
    # 创建QgsPointXYlist
    qgsPointXYlist = []
    for str in lalolist:
        value = str.split(",")
        if len(value) == 2:
            point = QgsPointXY(float(value[0]), float(value[1]))
            if isinstance(point, QgsPointXY):
                qgsPointXYlist.append(point)
            else:
                print(f"Invalid point: {point}")
        else:
            print(f"Invalid value: {value}")

    # 创建一个多边形几何对象
    polygon_geom = QgsGeometry.fromPolygonXY([qgsPointXYlist])
    print(polygon_geom)
    # 创建一个多边形要素对象
    polygon_feature = QgsFeature()
    polygon_feature.setGeometry(polygon_geom)

    # 创建一个图层，并添加多边形要素
    polygon_layer = QgsVectorLayer("Polygon", areaName, "memory")
    polygon_layer.dataProvider().addFeatures([polygon_feature])

    # 将图层添加到QGIS中
    QgsProject.instance().addMapLayer(polygon_layer)


def main():
    # 读取excel
    excel_file = r"C:\Users\Talie\Documents\四川省21市 (2)\四川省21市.xlsx"
    df = pd.read_excel(excel_file)
    for i, row in df.iterrows():
        row_str = ','.join(row.astype(str))
        # 正则表达式
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        # 匹配的是列表
        areaname = pattern.findall(row_str)[0]
        lalo = row_str.replace(areaname + ",", "").replace("[", "").replace("]", "")
        # 将经纬度字符串转成list
        laloList = lalo.split(";")
        createPolygonXY(areaname,laloList)
        break
main()