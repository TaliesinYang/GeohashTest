import decimal
from typing import List
import pygeohash as pgh
from utils.FileUtils import FileUtil

from shapely.geometry import Polygon


def plus(self:decimal):
    # 小数点后11 位精确到10米 10位精确到100米 9位精确到几百米
    return self.quantize(decimal.Decimal("0.00000000001"), rounding=decimal.ROUND_HALF_UP) + decimal.Decimal('0.00000000001')


if __name__ == '__main__':
    cityname = "达州市"
    filepath = r"C:\Users\Talie\Documents\四川省21市\%s" % cityname
    print(filepath)