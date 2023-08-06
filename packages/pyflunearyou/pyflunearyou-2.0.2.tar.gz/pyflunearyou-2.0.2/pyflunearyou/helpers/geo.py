"""Define various geo utility functions."""
from math import asin, cos, radians, sin, sqrt
from typing import Any, Dict, List


def get_nearest_by_coordinates(
    data: List[Dict[str, Any]],
    latitude_key: str,
    longitude_key: str,
    target_latitude: float,
    target_longitude: float,
) -> Any:
    """Get the closest dict entry based on latitude/longitude."""
    return min(
        data,
        key=lambda p: haversine(
            target_latitude,
            target_longitude,
            float(p[latitude_key]),
            float(p[longitude_key]),
        ),
    )


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Determine the distance between two latitude/longitude pairs."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    calc_a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    calc_c = 2 * asin(sqrt(calc_a))
    return 6371 * calc_c
