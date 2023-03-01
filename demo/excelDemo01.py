# QgsWkbTypes.PointGeometry点类型
# QgsWkbTypes.PolygonGeometry 面类型
def getLayerByNameAndType(layer_name, layer_type):
    layers = QgsProject.instance().mapLayersByName(layer_name)
    for layerVar in layers:
        layerType = layerVar.geometryType()
        if layerType == layer_type:
            return layerVar


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
                print("!!!!Point is inside polygon->"+str(point.x())+","+str(point.y()))
                break
        else:
            print("Point is outside polygon->"+str(point.x())+","+str(point.y()))

def getContainPoint(areaName:str):


def main():
    polygon_layer = getLayerByNameAndType("boundary_administrative_成都市", QgsWkbTypes.PolygonGeometry)
    point_layer = getLayerByNameAndType("test01", QgsWkbTypes.PointGeometry)
    print(point_layer)
    print(polygon_layer)
    checkPolygonContains(polygon_layer, point_layer)


main()