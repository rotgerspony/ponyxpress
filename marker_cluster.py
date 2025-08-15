
def cluster_markers(markers):
    return [{"lat": m["lat"], "lng": m["lng"], "count": 1} for m in markers]
