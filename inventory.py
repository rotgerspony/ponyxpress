
inventory = {}

def add_item(barcode, location):
    inventory[barcode] = location
    print(f"Added: {barcode} at {location}")

def print_inventory():
    for code, loc in inventory.items():
        print(f"{code} -> {loc}")

if __name__ == "__main__":
    add_item("PKG123", "Mailbox A")
    add_item("PKG456", "Porch B")
    print_inventory()
