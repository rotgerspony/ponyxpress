
def export_gpx(coords, filename="route.gpx"):
    with open(filename, "w") as f:
        f.write('<?xml version="1.0"?>\n<gpx version="1.1" creator="PonyXpress">\n<trk><trkseg>\n')
        for lat, lng in coords:
            f.write(f'<trkpt lat="{lat}" lon="{lng}"></trkpt>\n')
        f.write('</trkseg></trk></gpx>')
    print("GPX file saved.")
