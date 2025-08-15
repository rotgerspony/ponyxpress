
from geopy.distance import geodesic

def optimize_route(points):
    # Naive TSP: start to nearest until done
    path = []
    current = points[0]
    points = points[1:]
    path.append(current)
    while points:
        next_pt = min(points, key=lambda p: geodesic((current[0], current[1]), (p[0], p[1])).meters)
        points.remove(next_pt)
        path.append(next_pt)
        current = next_pt
    return path
