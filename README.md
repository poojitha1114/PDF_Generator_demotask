# Client Agreement PDF Generator

A Streamlit web application for generating professional client agreement PDFs with digital signatures, QR codes, and modern UI.

🚀 Features

PDF Generation: Well-formatted agreements with headers, footers, and tables

Digital Signatures: Draw or upload signature images

QR Code Verification: Automatic QR code for document verification

Responsive Design: Modern, professional UI

Temporary Storage: Secure handling of generated files

💻 Live Demo

Streamlit App Link:https://pdfgeneratordemotask-2vvt7ayg3gdym79sihgaek.streamlit.app/

📋 Requirements

Python 3.11+

Streamlit, FPDF2, ReportLab

Dependencies listed in requirements.txt

⚡ Run Locally
git clone https://github.com/poojitha1114/PDF_Generator_demotask.git
cd PDF_Generator_demotask
pip install -r requirements.txt
streamlit run app.py

🐳 Docker
docker build -t client-agreement-generator .
docker run -p 8501:8501 client-agreement-generator

☁️ Deployment

Optimized for Streamlit Cloud or Google Cloud Run

Live demo URL can be shared with stakeholders or interviewers

📄 Usage

Fill client information (Name, Address, Amount, Terms)

Add signature (draw/upload) or skip

Click Generate PDF → download the file

🏗️ Project Structure
PDF_generator/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
└── sample_output/  # Sample generated PDFs
