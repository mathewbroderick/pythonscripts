import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

def create_nametag_page(pdf_file, nametags_data, template_path):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    positions = [
        (120, 700), (390, 700), (120, 475),
        (390, 475), (120, 250), (390, 250)
    ]
    for i, data in enumerate(nametags_data):
        x, y = positions[i % 6]
        draw_nametag(c, x, y, data)
    c.save()
    
    merge_with_template(pdf_file, template_path)

def draw_nametag(canvas, x, y, data):
    first_name, last_name, chapter, field_trips = data
    
    canvas.setFont("Helvetica-Bold", 40)
    canvas.drawString(x, y, first_name)
    
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawString(x, y - 30, last_name)
    
    canvas.setFont("Helvetica-BoldOblique", 26)
    canvas.setFillColorRGB(1, 0, 0)
    canvas.drawString(x, y - 60, chapter)
    canvas.setStrokeColorRGB(1, 0, 0)
    canvas.line(x, y - 62, x + canvas.stringWidth(chapter, "Helvetica-BoldOblique", 26), y - 62)
    canvas.setFillColorRGB(0, 0, 0) 
    
    canvas.setFont("Helvetica-Bold", 12)
    canvas.setFont("Helvetica", 12)
    canvas.drawString(x - 15, y - 110, field_trips.get('Friday', ''))
    canvas.drawString(x - 15, y - 130, field_trips.get('Saturday', ''))
    canvas.drawString(x - 15, y - 150, field_trips.get('Sunday', ''))

def merge_with_template(nametag_pdf_path, template_pdf_path):
    output = PdfWriter()
    nametag_pdf = PdfReader(nametag_pdf_path)
    template_pdf = PdfReader(template_pdf_path)
    
    for page_number in range(len(nametag_pdf.pages)):
        nametag_page = nametag_pdf.pages[page_number]
        template_page = template_pdf.pages[page_number]
        template_page.merge_page(nametag_page)
        output.add_page(template_page)
    
    with open(nametag_pdf_path, 'wb') as f:
        output.write(f)

def read_csv_and_create_nametags(csv_file, output_dir, template_path):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        nametags_data = []
        batch_count = 1
        for row in reader:
            name_parts = row['Name'].strip().split(maxsplit=1)
            if len(name_parts) < 2:
                continue
            first_name, last_name = name_parts
            chapter = row['NPSO Chapter'].strip()
            field_trips = {
                'Friday': row['finalized  friday'].strip(),
                'Saturday': row['Finalized Saturday'].strip(),
                'Sunday': row['Finalized Sunday'].strip()
            }
            nametags_data.append((first_name, last_name, chapter, field_trips))

            if len(nametags_data) == 6:
                output_file = f"{output_dir}/nametags_batch_{batch_count}.pdf"
                create_nametag_page(output_file, nametags_data, template_path)
                nametags_data = []
                batch_count += 1
        
        if nametags_data:
            output_file = f"{output_dir}/nametags_batch_{batch_count}.pdf"
            create_nametag_page(output_file, nametags_data, template_path)

read_csv_and_create_nametags('deathtoall.csv', './', 'newtemplate.pdf')
