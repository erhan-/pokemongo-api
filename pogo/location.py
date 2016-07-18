import logging
from geopy.geocoders import GoogleV3

import util
import s2sphere
from geopy.distance import VincentyDistance

geolocator = GoogleV3()

def getLocation(search):
    loc = geolocator.geocode(search)
    return loc

def encodeLocation(loc):
    return (util.f2i(loc.latitude), util.f2i(loc.longitude), util.f2i(loc.altitude))


def getNeighbors(loc, level=15, spread=700):
    distance = VincentyDistance(meters=spread)
    center = (loc.latitude, loc.longitude, 0)
    p1 = distance.destination(point=center, bearing=45)
    p2 = distance.destination(point=center, bearing=225)
    p1 = s2sphere.LatLng.from_degrees(p1[0], p1[1])
    p2 = s2sphere.LatLng.from_degrees(p2[0], p2[1])
    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    region = s2sphere.RegionCoverer()
    region.min_level = level
    region.max_level = level
    cells = region.get_covering(rect)
    return sorted([c.id() for c in cells])
