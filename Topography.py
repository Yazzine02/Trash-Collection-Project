import math
import random


def degrees_to_radians(degrees):
    return degrees * math.pi / 180


def distance_in_km_between_earth_coordinates(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371

    d_lat = degrees_to_radians(lat2 - lat1)
    d_lon = degrees_to_radians(lon2 - lon1)

    lat1 = degrees_to_radians(lat1)
    lat2 = degrees_to_radians(lat2)

    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.sin(d_lon / 2) * math.sin(d_lon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c


def generate_points_at_distance(lat, lon, distance_km):
    earth_radius_km = 6371

    # Convert latitude and longitude from degrees to radians
    lat = degrees_to_radians(lat)
    lon = degrees_to_radians(lon)

    # Random bearing in radians
    bearing = random.uniform(0, 2 * math.pi)

    # Calculate new latitude
    new_lat = math.asin(math.sin(lat) * math.cos(distance_km / earth_radius_km) +
                        math.cos(lat) * math.sin(distance_km / earth_radius_km) * math.cos(bearing))

    # Calculate new longitude
    new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance_km / earth_radius_km) * math.cos(lat),
                               math.cos(distance_km / earth_radius_km) - math.sin(lat) * math.sin(new_lat))

    # Convert radians back to degrees
    new_lat = new_lat * 180 / math.pi
    new_lon = new_lon * 180 / math.pi

    return (new_lat, new_lon)