
def summarize_packages(packages):
    total = len(packages)
    by_size = {}
    for pkg in packages:
        size = pkg.get("size", "unknown")
        by_size[size] = by_size.get(size, 0) + 1
    print(f"Total: {total}")
    for k, v in by_size.items():
        print(f"{k}: {v}")
