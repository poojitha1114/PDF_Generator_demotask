import streamlit as st
import os
import tempfile
import uuid
from datetime import datetime
from io import BytesIO
import base64
import qrcode
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from streamlit_drawable_canvas import st_canvas
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Client Agreement PDF Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding and styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .logo-placeholder {
        width: 80px;
        height: 80px;
        background: white;
        border-radius: 50%;
        margin: 0 auto 1rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #1f4e79;
        font-weight: bold;
    }
    
    .form-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f4e79;
    }
    
    .form-section h3 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def create_temp_folder():
    """Create temporary folder for PDF storage"""
    temp_dir = os.path.join(tempfile.gettempdir(), "client_agreements")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

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

def generate_pdf(client_name, client_address, agreement_amount, notes_terms, signature_data=None):
    """Generate professional PDF agreement"""
    
    # Create temporary file
    temp_dir = create_temp_folder()
    filename = f"agreement_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(temp_dir, filename)
    
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
        st.error(f"Error adding logo: {e}")
    
    # Title
    story.append(Paragraph("CLIENT SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 30))
    
    # Agreement details table
    agreement_data = [
        ['Agreement Date:', datetime.now().strftime('%B %d, %Y')],
        ['Client Name:', client_name],
        ['Client Address:', client_address],
        ['Agreement Amount:', f"${agreement_amount:,.2f}"],
        ['Agreement ID:', f"AGR-{uuid.uuid4().hex[:8].upper()}"]
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
        qr_text = f"Agreement ID: AGR-{uuid.uuid4().hex[:8].upper()}\nClient: {client_name}\nAmount: ${agreement_amount:,.2f}"
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
        st.error(f"Error adding QR code: {e}")
    
    # Build PDF
    doc.build(story)
    
    return filepath, filename

def main():
    # Header with logo
    st.markdown("""
    <div class="main-header">
        <div class="logo-placeholder">CA</div>
        <h1>Client Agreement PDF Generator</h1>
        <p>Generate professional client agreements with digital signatures</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for additional options
    with st.sidebar:
        st.header("📋 Quick Actions")
        st.info("Fill out the form to generate a professional PDF agreement")
        
        st.header("🎨 Customization")
        include_qr = st.checkbox("Include QR Code", value=True, help="Add QR code for verification")
        include_logo = st.checkbox("Include Logo", value=True, help="Add company logo placeholder")
        
        st.header("📊 Statistics")
        if 'pdf_count' not in st.session_state:
            st.session_state.pdf_count = 0
        st.metric("PDFs Generated", st.session_state.pdf_count)
    
    # Main form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("📝 Agreement Details")
        
        # Client information
        client_name = st.text_input(
            "Client Name *",
            value=st.session_state.get('sample_client_name', ''),
            placeholder="Enter client's full name",
            help="Full legal name of the client"
        )
        
        client_address = st.text_area(
            "Client Address *",
            value=st.session_state.get('sample_client_address', ''),
            placeholder="Enter complete address including city, state, and zip code",
            height=100,
            help="Complete mailing address"
        )
        
        # Financial details
        agreement_amount = st.number_input(
            "Agreement Amount ($) *",
            value=st.session_state.get('sample_agreement_amount', 0.0),
            min_value=0.0,
            step=100.0,
            format="%.2f",
            help="Total amount for the agreement"
        )
        
        # Terms and notes
        notes_terms = st.text_area(
            "Notes / Terms *",
            value=st.session_state.get('sample_notes_terms', ''),
            placeholder="Enter specific terms, conditions, and notes for this agreement...",
            height=150,
            help="Detailed terms and conditions specific to this agreement"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Signature section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("✍️ Client Signature (Optional)")
        
        signature_option = st.radio(
            "Signature Method:",
            ["None", "Draw Signature", "Upload Image"],
            horizontal=True
        )
        
        signature_data = None
        
        if signature_option == "Draw Signature":
            st.write("Draw your signature below:")
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0.0)",
                stroke_width=2,
                stroke_color="#000000",
                background_color="#ffffff",
                height=150,
                width=400,
                drawing_mode="freedraw",
                key="signature_canvas",
            )
            
            if canvas_result.image_data is not None:
                signature_data = canvas_result.image_data
        
        elif signature_option == "Upload Image":
            uploaded_signature = st.file_uploader(
                "Upload signature image",
                type=['png', 'jpg', 'jpeg'],
                help="Upload a clear image of the signature"
            )
            
            if uploaded_signature is not None:
                signature_data = uploaded_signature
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📄 PDF Preview")
        
        # Validation
        is_valid = all([client_name, client_address, agreement_amount > 0, notes_terms])
        
        if not is_valid:
            st.warning("⚠️ Please fill in all required fields marked with *")
        else:
            st.success("✅ All required fields completed")
        
        # Generate PDF button
        if st.button("🚀 Generate PDF Agreement", disabled=not is_valid, use_container_width=True):
            try:
                with st.spinner("Generating PDF..."):
                    filepath, filename = generate_pdf(
                        client_name, 
                        client_address, 
                        agreement_amount, 
                        notes_terms, 
                        signature_data
                    )
                    
                    st.session_state.pdf_count += 1
                    
                    # Success message
                    st.markdown(f"""
                    <div class="success-message">
                        <strong>✅ PDF Generated Successfully!</strong><br>
                        File: {filename}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download button
                    with open(filepath, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                        
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # Display PDF info
                    st.info(f"📊 File size: {len(pdf_data) / 1024:.1f} KB")
                    
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    <strong>❌ Error generating PDF:</strong><br>
                    {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        # Sample data button
        if st.button("📋 Load Sample Data", use_container_width=True):
            st.session_state.update({
                'sample_client_name': 'John Smith',
                'sample_client_address': '123 Main Street\nAnytown, ST 12345\nUnited States',
                'sample_agreement_amount': 5000.00,
                'sample_notes_terms': 'This agreement covers consulting services for a period of 6 months. Services include strategic planning, market analysis, and implementation support. Payment terms: 50% upfront, 50% upon completion.'
            })
            st.rerun()

if __name__ == "__main__":
    main()
