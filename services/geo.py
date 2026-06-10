from geopy.distance import geodesic

def distance_km(coord1, coord2):
    return geodesic(coord1, coord2).km


def score_by_distance(distance_km):
    if distance_km < 5:
        return 10
    elif distance_km < 15:
        return 7
    elif distance_km < 30:
        return 4
    return 1
