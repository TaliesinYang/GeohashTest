import geohash2
layer = iface.activeLayer()  # 获取活动图层
features = layer.selectedFeatures()  # 获取选中要素
for feature in features:
    point=feature.geometry().asPoint()
    print(str(point.x())+","+str(point.y()))
    gh = geohash2.encode(point.y(), point.x(), 6)
    print(gh)