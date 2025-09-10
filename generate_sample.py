#!/usr/bin/env python3
"""
Generate a sample PDF to demonstrate the Client Agreement PDF Generator functionality.
This script creates a sample PDF without running the full Streamlit app.
"""

import os
import sys
import tempfile
import uuid
from datetime import datetime
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def generate_qr_code(text):
    """Generate QR code for verification"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_buffer = BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

def create_logo_placeholder():
    """Create a simple logo placeholder"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple geometric logo
    draw.ellipse([50, 50, 150, 150], fill='#1f4e79', outline='#2d5aa0', width=3)
    draw.text((100, 100), "CA", fill='white', anchor='mm')
    
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

def generate_sample_pdf():
    """Generate a sample PDF with demo data"""
    
    # Sample data
    client_name = "John Smith"
    client_address = "123 Main Street\nAnytown, ST 12345\nUnited States"
    agreement_amount = 5000.00
    notes_terms = """This agreement covers comprehensive consulting services for a period of 6 months. 
    Services include strategic planning, market analysis, competitive research, and implementation support. 
    
    Deliverables include:
    • Monthly strategic reports
    • Market analysis documentation
    • Implementation roadmap
    • Ongoing consultation sessions
    
    Payment terms: 50% upfront payment required, remaining 50% due upon project completion. 
    All work will be completed according to the agreed timeline and quality standards."""
    
    # Create output file
    output_dir = "sample_output"
    os.makedirs(output_dir, exist_ok=True)
    filename = "sample_agreement.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=100,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#1f4e79'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#1f4e79'),
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # Build PDF content
    story = []
    
    # Logo placeholder
    try:
        logo_buffer = create_logo_placeholder()
        logo_img = RLImage(logo_buffer, width=1*inch, height=1*inch)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
        story.append(Spacer(1, 20))
    except Exception as e:
        print(f"Warning: Could not add logo: {e}")
    
    # Title
    story.append(Paragraph("CLIENT SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 30))
    
    # Agreement details table
    agreement_id = f"AGR-{uuid.uuid4().hex[:8].upper()}"
    agreement_data = [
        ['Agreement Date:', datetime.now().strftime('%B %d, %Y')],
        ['Client Name:', client_name],
        ['Client Address:', client_address],
        ['Agreement Amount:', f"${agreement_amount:,.2f}"],
        ['Agreement ID:', agreement_id]
    ]
    
    agreement_table = Table(agreement_data, colWidths=[2*inch, 4*inch])
    agreement_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(agreement_table)
    story.append(Spacer(1, 30))
    
    # Terms and conditions
    story.append(Paragraph("TERMS AND CONDITIONS", heading_style))
    story.append(Paragraph(notes_terms, normal_style))
    story.append(Spacer(1, 30))
    
    # Standard clauses
    standard_terms = """
    This agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, 
    representations, or agreements relating to the subject matter herein. This agreement shall be governed by 
    the laws of the applicable jurisdiction. Any modifications to this agreement must be made in writing and 
    signed by both parties.
    """
    
    story.append(Paragraph("STANDARD PROVISIONS", heading_style))
    story.append(Paragraph(standard_terms, normal_style))
    story.append(Spacer(1, 40))
    
    # Signature section
    signature_data_content = [
        ['Client Signature:', ''],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Print Name:', client_name]
    ]
    
    signature_table = Table(signature_data_content, colWidths=[2*inch, 4*inch])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (1, 0), (1, 0), 1, black),  # Signature line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 30))
    
    # QR Code for verification
    try:
        qr_text = f"Agreement ID: {agreement_id}\nClient: {client_name}\nAmount: ${agreement_amount:,.2f}"
        qr_buffer = generate_qr_code(qr_text)
        qr_img = RLImage(qr_buffer, width=1*inch, height=1*inch)
        qr_img.hAlign = 'RIGHT'
        story.append(qr_img)
        
        story.append(Paragraph("Scan QR code for verification", ParagraphStyle(
            'QRCaption',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_RIGHT,
            textColor=HexColor('#666666')
        )))
    except Exception as e:
        print(f"Warning: Could not add QR code: {e}")
    
    # Build PDF
    doc.build(story)
    
    return filepath, filename

if __name__ == "__main__":
    try:
        filepath, filename = generate_sample_pdf()
        print("Sample PDF generated successfully!")
        print(f"File: {filename}")
        print(f"Location: {filepath}")
        
        # Get file size
        file_size = os.path.getsize(filepath)
        print(f"Size: {file_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"Error generating sample PDF: {e}")
        sys.exit(1)
