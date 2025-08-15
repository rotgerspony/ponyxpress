
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_packages_to_pdf(packages, filename="packages.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    text = c.beginText(50, 750)
    text.setFont("Helvetica", 12)
    text.textLine("PonyXpress Delivery Report")
    for pkg in packages:
        text.textLine(f"{pkg['barcode']} - {pkg['destination']}")
    c.drawText(text)
    c.save()
    print("PDF export complete.")
