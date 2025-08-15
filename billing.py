
def generate_invoice(user, packages, rate_per_package=1.0):
    total = len(packages) * rate_per_package
    invoice = f"INVOICE\nUser: {user}\nPackages: {len(packages)}\nTotal Due: ${total:.2f}"
    print(invoice)
    return invoice

# Example:
# generate_invoice("carrier1@example.com", [{'barcode': 'abc'}, {'barcode': 'xyz'}])
