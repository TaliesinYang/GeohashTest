from shapely.geometry import Polygon, Point


class ShapelyUtils:
    def getPolygon(self,list:list) -> Polygon:
        """

        :rtype: object
        """
        polygon = Polygon(list)

        # 定义多边形的边界

        # 创建多边形
        polygon = Polygon(list)
        return polygon

    def ifPolygon(self,polygon:Polygon,x,y):
        envelope = polygon.envelope
        # 定义要检查的经纬度
        point = Point(x,y)
        return envelope.intersects(point)

if __name__ == '__main__':
    polygon_coords = [(1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (2.0, 1.0)]
    polygon = ShapelyUtils.getPolygon(polygon_coords)
    flag=ShapelyUtils.ifPolygon(1,polygon,1.5,300)
    print(flag)