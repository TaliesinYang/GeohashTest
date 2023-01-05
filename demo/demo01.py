from utils.FileUtils import FileUtil
import pygeohash as pgh

if __name__ == '__main__':
    helper = FileUtil()
    contents: str = helper.read_file('myfile.txt')
    strList: list[str] = contents.split("\n")
    coordinates = list()
    for x in strList:
        elem = x.split(" ")
        coordinates.append((elem[0], elem[1]))


    geohashes = [pgh.encode(float(coordinate[0]), float(coordinate[1]),7) for coordinate in coordinates]
    result=""
    geohashes=set(geohashes)
    for x in geohashes:
        result+=str(x)+"\n"

    helper.write_file("demo01.txt",result)