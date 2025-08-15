
import csv

def export_packages_to_csv(packages, filename="packages.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Barcode", "Size", "Destination"])
        for pkg in packages:
            writer.writerow([pkg["barcode"], pkg["size"], pkg["destination"]])
    print("CSV export complete.")
