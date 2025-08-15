
def generate_demo_script():
    scenes = [
        "📱 User scans package barcode",
        "🗺️ Map auto-fills destination",
        "📷 Photo attached to log",
        "🔒 Admin views route replay",
        "📦 Packages auto-sync when online"
    ]
    print("=== PonyXpress Demo ===")
    for i, scene in enumerate(scenes):
        print(f"Scene {i+1}: {scene}")

if __name__ == "__main__":
    generate_demo_script()
