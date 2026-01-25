# utils/routing.py
import math
from ..models import Driver


def find_nearest_driver(order_lat, order_lng, max_radius_km=15):
    """
    Finds the closest available driver within a specific radius.
    """
    available_drivers = Driver.objects.filter(is_available=True)
    best_driver = None
    shortest_distance = max_radius_km

    for driver in available_drivers:
        # Distance formula (Haversine)
        R = 6371  # Earth radius in km
        d_lat = math.radians(driver.current_lat - order_lat)
        d_lng = math.radians(driver.current_lng - order_lng)

        a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(order_lat)) * \
            math.cos(math.radians(driver.current_lat)) * math.sin(d_lng / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        if distance < shortest_distance:
            shortest_distance = distance
            best_driver = driver

    return best_driver