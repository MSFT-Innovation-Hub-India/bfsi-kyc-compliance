# bfsi-kyc-compliance

A KYC (Know Your Customer) Compliance application for the Banking, Financial Services and Insurance (BFSI) sector.

## Features

- Modern web-based UI for KYC document submission
- Aadhar and PAN number validation
- Document upload functionality (PDF, JPG, JPEG, PNG)
- RESTful API for KYC validation and compliance checks
- Microsoft design principles and branding

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Flask

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MSFT-Innovation-Hub-India/bfsi-kyc-compliance.git
cd bfsi-kyc-compliance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask server:
```bash
python compliance_api.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Using the KYC Portal

1. **Enter Aadhar Number**: Provide your 12-digit Aadhar number
2. **Upload Aadhar Document**: Upload a clear copy of your Aadhar card (PDF, JPG, JPEG, or PNG format, max 5MB)
3. **Enter PAN Number**: Provide your 10-character PAN number (format: XXXXX0000X)
4. **Upload PAN Document**: Upload a clear copy of your PAN card (PDF, JPG, JPEG, or PNG format, max 5MB)
5. **Submit**: Click the "Submit KYC Documents" button to submit your information

## API Endpoints

- `GET /` - KYC Compliance Portal UI
- `POST /submit-kyc` - Submit KYC documents and information
- `GET /kyc?customerID={id}` - Validate KYC for a customer
- `GET /compliance?customerID={id}` - Check compliance status
- `GET /swagger` - API specification

## Project Structure

```
bfsi-kyc-compliance/
├── compliance_api.py      # Flask application and API endpoints
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── swagger.json          # API specification
├── templates/            # HTML templates
│   └── index.html       # KYC portal UI
└── uploads/             # Uploaded documents (not tracked in git)
```

## Security

- File upload validation (type and size restrictions)
- Secure filename handling
- Input validation for Aadhar and PAN numbers
- HTTPS recommended for production deployment

## License

MIT License