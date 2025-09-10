# Client Agreement PDF Generator

A production-ready Streamlit web application for generating professional client agreement PDFs with digital signatures, QR codes, and modern UI/UX design.

![App Screenshot](https://via.placeholder.com/800x400/1f4e79/ffffff?text=Client+Agreement+PDF+Generator)

## 🚀 Features

- **Professional PDF Generation**: Creates well-formatted agreements with headers, footers, and structured layouts
- **Digital Signatures**: Support for both canvas drawing and image upload signatures
- **QR Code Verification**: Automatic QR code generation for document verification
- **Modern UI/UX**: Responsive design with branding colors and professional styling
- **Real-time Validation**: Form validation with helpful error messages
- **Cloud-Ready**: Optimized for deployment on Google Cloud Run
- **Temporary Storage**: Secure temporary file handling with unique filenames

## 📋 Requirements

- Python 3.11+
- Streamlit 1.28.1+
- ReportLab 4.0.4+
- Additional dependencies listed in `requirements.txt`

## 🛠️ Local Setup & Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd PDF_generator
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t client-agreement-generator .
```

### Run Docker Container

```bash
docker run -p 8501:8501 client-agreement-generator
```

## ☁️ Google Cloud Run Deployment

### Prerequisites

1. Install Google Cloud CLI
2. Authenticate with Google Cloud
3. Enable Cloud Run API
4. Enable Container Registry API

### Deployment Steps

#### 1. Set Project Variables

```bash
export PROJECT_ID="your-project-id"
export SERVICE_NAME="client-agreement-generator"
export REGION="us-central1"
```

#### 2. Configure Docker for Google Cloud

```bash
gcloud auth configure-docker
```

#### 3. Build and Tag Image

```bash
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .
```

#### 4. Push to Container Registry

```bash
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME
```

#### 5. Deploy to Cloud Run

```bash
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --port 8501
```

#### 6. Get Service URL

```bash
gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'
```

### Alternative: One-Command Deployment

```bash
gcloud run deploy client-agreement-generator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi
```

## 📱 Usage Guide

### 1. Fill Client Information
- **Client Name**: Enter the full legal name
- **Client Address**: Complete mailing address
- **Agreement Amount**: Total contract value in USD
- **Notes/Terms**: Specific terms and conditions

### 2. Add Signature (Optional)
- **Draw Signature**: Use the canvas to draw directly
- **Upload Image**: Upload a signature image file (PNG, JPG, JPEG)
- **Skip**: Generate PDF without signature

### 3. Generate PDF
- Click "Generate PDF Agreement"
- Download the generated PDF
- PDF includes QR code for verification

### 4. Sample Data
- Use "Load Sample Data" to test the application
- Modify sample data as needed

## 🏗️ Project Structure

```
PDF_generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── README.md            # Project documentation
└── sample_output/       # Sample generated PDFs
    └── sample_agreement.pdf
```

## 🎨 Customization

### Branding Colors
The app uses a professional blue color scheme:
- Primary: `#1f4e79`
- Secondary: `#2d5aa0`
- Background: `#f8f9fa`

### Logo Customization
Replace the logo placeholder in the `create_logo_placeholder()` function with your company logo.

### PDF Template
Modify the `generate_pdf()` function to customize:
- Header/footer content
- Table layouts
- Color schemes
- Additional sections

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application port | `8501` |
| `STREAMLIT_SERVER_HEADLESS` | Run in headless mode | `true` |
| `STREAMLIT_SERVER_ENABLE_CORS` | Enable CORS | `false` |

### Streamlit Configuration

Create `.streamlit/config.toml` for additional customization:

```toml
[server]
port = 8501
headless = true
enableCORS = false

[theme]
primaryColor = "#1f4e79"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#262730"
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Form validation works correctly
- [ ] PDF generation completes successfully
- [ ] Download functionality works
- [ ] Signature canvas responds properly
- [ ] Image upload accepts valid formats
- [ ] QR code generates correctly
- [ ] Responsive design on mobile devices

### Sample Test Data

```
Client Name: John Smith
Client Address: 123 Main Street, Anytown, ST 12345, United States
Agreement Amount: $5,000.00
Notes/Terms: Consulting services for 6 months including strategic planning and implementation support.
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt
```

#### 2. PDF Generation Fails
- Check file permissions in temp directory
- Verify ReportLab installation
- Ensure sufficient disk space

#### 3. Canvas Signature Not Working
- Clear browser cache
- Check JavaScript is enabled
- Try different browser

#### 4. Docker Build Fails
- Ensure Docker is running
- Check Dockerfile syntax
- Verify base image availability

### Performance Optimization

1. **Memory Usage**: Adjust container memory limits based on usage
2. **Startup Time**: Use multi-stage Docker builds for smaller images
3. **Concurrent Users**: Configure Cloud Run instances based on traffic

## 📊 Monitoring & Logging

### Cloud Run Monitoring

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" --limit 50

# Monitor metrics
gcloud run services describe $SERVICE_NAME --region $REGION
```

### Application Metrics

The app tracks:
- Number of PDFs generated (session-based)
- Form completion rates
- Error occurrences

## 🔒 Security Considerations

- Temporary files are automatically cleaned up
- No persistent storage of sensitive data
- Input validation prevents injection attacks
- HTTPS enforced in production (Cloud Run)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Cloud Run documentation

## 🎯 Roadmap

- [ ] Email integration for automatic PDF delivery
- [ ] Multiple signature support
- [ ] Template customization UI
- [ ] Database integration for agreement tracking
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ using Streamlit and ReportLab**
