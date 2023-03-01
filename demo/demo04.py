# QgsWkbTypes.PointGeometry点类型
# QgsWkbTypes.PolygonGeometry 面类型
def getLayerByNameAndType(layer_name, layer_type):
    layers = QgsProject.instance().mapLayersByName(layer_name)
    for layerVar in layers:
        layerType = layerVar.geometryType()
        if layerType == layer_type:
            return layerVar
def getExcelList():
    excel_file = r"C:\Users\Talie\Documents\四川省21市 (2)\四川省21市.xlsx"
    # 读取excel
    df = pd.read_excel(excel_file)
    excelDict=dict()
    for i, row in df.iterrows():
        row_str = ','.join(row.astype(str))
        # 正则表达式
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        # 匹配的是列表
        areaname = pattern.findall(row_str)[0]
        lalo = row_str.replace(areaname + ",", "").replace("[", "").replace("]", "")
        # 将经纬度字符串转成list
        laloList = lalo.split(";")
        xyList=list()
        for string in laloList:
            var = string.split(",")
            xyList.append((float(var[0]),float(var[1])))
        # createPolygonXY(areaname+"test",set(laloList))
        # func(areaname, laloList)
        excelDict[areaname]=xyList
    return excelDict
def checkPolygonContains(polygon_layer, point_layer):
    # 循环遍历点图层中的每个点
    for point_feature in point_layer.getFeatures():
        print(point_feature)
        point_geom = point_feature.geometry()
        point = point_geom.asPoint()

        # 选择第一个多边形要素来判断该点是否在多边形内部
        for polygon_feature in polygon_layer.getFeatures():
            polygon_geom = polygon_feature.geometry()

            if polygon_geom.contains(point_geom):
                print("Point is inside polygon->"+str(point.x())+","+str(point.y()))
                break
        else:
            print("Point is outside polygon->"+str(point.x())+","+str(point.y()))

def getPointList(areaname:str,laloList:list,polygon_layer):
    points_layer = QgsVectorLayer("Point", areaname, "memory")
    QgsProject.instance().addMapLayer(points_layer)
    min_x = min([p[0] for p in laloList])
    max_x = max([p[0] for p in laloList])
    min_y = min([p[1] for p in laloList])
    max_y = max([p[1] for p in laloList])
    step = 0.001
    for x in range(int((max_x - min_x) / step) + 5):
        current_x = min_x + x * step
        for y in range(int((max_y - min_y) / step) + 5):
            current_y = min_y + y * step
            for polygon_feature in polygon_layer.getFeatures():
                polygon_geom = polygon_feature.geometry()
                point = QgsPointXY(current_x, current_y)
                if polygon_geom.contains(point):
                    # 创建一个点要素
                    point_feature = QgsFeature()
                    point_feature.setGeometry(QgsGeometry.fromPointXY(point))
                    points_layer.dataProvider().addFeatures([point_feature])
                    # print("Point is inside polygon->" + str(point.x()) + "," + str(point.y()))
                    break
                else:
                    # print("Point is outside polygon->" + str(point.x()) + "," + str(point.y()))
            break
        break
def main():
    polygon_layer = getLayerByNameAndType("boundary_administrative_成都市", QgsWkbTypes.PolygonGeometry)
    point_layer = getLayerByNameAndType("test01", QgsWkbTypes.PointGeometry)
    # checkPolygonContains(polygon_layer, point_layer)
    areaname="成都市"
    excelDict=getExcelList()
    getPointList(areaname,excelDict[areaname],polygon_layer)


main()