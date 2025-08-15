
def export_kml(coords, filename="route.kml"):
    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n')
        for lat, lng in coords:
            f.write(f'<Placemark><Point><coordinates>{lng},{lat},0</coordinates></Point></Placemark>\n')
        f.write('</Document></kml>')
    print("KML file saved.")
