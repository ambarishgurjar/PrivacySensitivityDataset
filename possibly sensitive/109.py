
    if (py > by or py < ay) or (
        px > max(ax, bx)):
        return False

    if px < min(ax, bx):
        intersect = True
    else:
        if abs(ax - bx) > _tiny:
            m_red = (by - ay) / float(bx - ax)
        else:
            m_red = _huge
        if abs(ax - px) > _tiny:
            m_blue = (py - ay) / float(px - ax)
        else:
            m_blue = _huge
        intersect = m_blue >= m_red
    return intersect

def _odd(x): return x%2 == 1

def is_point_inside(p, poly, ln):
    s = 0

    for i in range(ln):
        j = (i + 1) % ln

        s += ray_intersect_segment(p[1], p[0], poly[i][1], poly[i][0], poly[j][1], poly[j][0])

    return _odd(s)


_earthRadius = 6378137
_minLatitude = -85.05112878
_maxLatitude = 85.05112878
_minLongitude = -180
_maxLongitude = 180


_level = 11


def _clip(num, minValue, maxValue):
    return min(max(num, minValue), maxValue)


def _latlngToPixelXY(lat, lng):
    latitude = _clip(lat, _minLatitude, _maxLatitude)
    longitude = _clip(lng, _minLongitude, _maxLongitude)

    x = (longitude + 180) / 360.0
    sinLatitude = math.sin(latitude * math.pi / 180.0)
    y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)

    mapSize = 256 << _level
    pixelX = int(_clip(x * mapSize + 0.5, 0, mapSize - 1))
    pixelY = int(_clip(y * mapSize + 0.5, 0, mapSize - 1))

    return pixelX, pixelY


def _pixelXYToTileXY(pixelX, pixelY):
    return int(math.floor(pixelX / 256.0)), int(math.floor(pixelY / 256.0))


with open('tzids.json', 'r') as data:
    tzids = json.load(data)


with open('polygons-1.json', 'r') as data:
    global polygons
    polygons = json.load(data)

with open('polygons-2.json', 'r') as data:
    json_data = json.load(data)
    polygons.extend(json_data)

