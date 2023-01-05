import decimal

import pyproj


class ProjectionUtils:
    def mapping(self,longitude: decimal, latitude: decimal):
        # 创建投影转换器
        projector = pyproj.Transformer.from_crs("epsg:3857", "epsg:4326")

        # 平面坐标
        # 进行投影转换
        x, y = projector.transform(longitude, latitude)
        return x, y

    def unmapping(slef,x: decimal, y: decimal):
        projector = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857")

        # 进行投影转换
        longitude, latitude = projector.transform(x, y)
        return (longitude, latitude)


if __name__ == '__main__':
    x: decimal = 105.27745692999337734
    y: decimal = 31.10850349014401672
    tuple = ProjectionUtils.mapping(1,x, y)
    print(tuple)
    point= ProjectionUtils.unmapping(1,"0.000279452", "0.000945723")
    print(point[0])
    print(point[1])
