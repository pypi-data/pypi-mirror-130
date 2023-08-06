import enum
import math
from typing import Tuple, Union

# Earth radius in kilometers
# (mean radius, see https://en.wikipedia.org/wiki/Earth_radius#Published_values)
EARTH_RADIUS_KM = 6371.0087714


class Bearing(enum.Enum):
    """
    Enumeration of basic bearings.
    """

    NORTH = 0.0
    NORTH_EAST = 45.0
    EAST = 90.0
    SOUTH_EAST = 135.0
    SOUTH = 180.0
    SOUTH_WEST = 225.0
    WEST = 270.0
    NORTH_WEST = 315.0


def move(
    point: Tuple[float, float],
    bearing: Union[Bearing, float],
    distance: float,
    earth_radius: float = EARTH_RADIUS_KM,
) -> Tuple[float, float]:
    """
    Moves a point on the surface of the earth (given as (lat, lon) tuple) towards the
    given bearing by the given distance (in km) and returns the resulting point.
    """

    # Handle enumerated bearing
    if isinstance(bearing, Bearing):
        bearing = bearing.value

    # Convert to radians
    lat, lon = math.radians(point[0]), math.radians(point[1])
    bearing = math.radians(bearing)

    # Calculate moved lat and lon
    lat_prime = math.asin(
        math.sin(lat) * math.cos(distance / earth_radius)
        + math.cos(lat) * math.sin(distance / earth_radius) * math.cos(bearing)
    )

    lon_prime = lon + math.atan2(
        math.sin(bearing) * math.sin(distance / earth_radius) * math.cos(lat),
        math.cos(distance / earth_radius) - math.sin(lat) * math.sin(lat_prime),
    )

    # Convert back to degrees
    lat_prime = math.degrees(lat_prime)
    lon_prime = math.degrees(lon_prime)

    # Normalize latitude
    lat_prime += 90.0
    lat_prime %= 180.0
    lat_prime -= 90.0

    # Normalize longitude
    lon_prime += 180.0
    lon_prime %= 360.0
    lon_prime -= 180.0

    return lat_prime, lon_prime


def haversine(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    earth_radius: float = EARTH_RADIUS_KM,
) -> float:
    """
    Calculate the great circle distance between two points on the earth (in km).
    """

    # Convert to radians
    p1_lat, p1_lon, p2_lat, p2_lon = map(math.radians, [p1[0], p1[1], p2[0], p2[1]])

    # Calculate haversine
    d_lon = p2_lon - p1_lon
    d_lat = p2_lat - p1_lat
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(p1_lat) * math.cos(p2_lat) * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return c * earth_radius
