import os
import sys
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import json

from config import DefaultConfig
configParams = DefaultConfig()

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    try:
        import pyodbc
        conn = pyodbc.connect(f'DRIVER={configParams.driver};SERVER={configParams.server};PORT=1433;DATABASE={configParams.database};UID={configParams.username};PWD={configParams.password}')
        return conn
    except ImportError:
        print("Warning: pyodbc not installed. Database features will be disabled.")
        return None
    except Exception as e:
        print(f"Warning: Could not connect to database: {str(e)}")
        return None

@app.route('/kyc', methods=['GET'])
def kyc_validation():
    print("ComplianceAPI: KYC validation")
    customer_id = request.args.get('customerID')
    conn = get_db_connection()
    
    if conn is None:
        return jsonify({
            "status": "failure",
            "message": "Database connection not available"
        }), 503
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CustomerDetails WHERE customerId = ?", customer_id)
    customer_details = cursor.fetchone()
    conn.close()
    
    if customer_details:
        response = {
            "status": "success",
            "message": "KYC validation successful",
            "data": {
                "customerId": customer_details.customerId,
                "name": customer_details.name,
                "dob": customer_details.dob,
                "address": customer_details.address
            }
        }
    else:
        response = {
            "status": "failure",
            "message": "Customer not found"
        }
    return jsonify(response)

@app.route('/compliance', methods=['GET'])
def compliance_check():
    print("ComplianceAPI: Compliance check")
    customer_id = request.args.get('customerID')
    conn = get_db_connection()
    
    if conn is None:
        return jsonify({
            "status": "failure",
            "message": "Database connection not available"
        }), 503
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ComplianceDetails WHERE customerId = ?", customer_id)
    compliance_details = cursor.fetchone()
    conn.close()
    
    if compliance_details:
        response = {
            "status": "success",
            "message": "Compliance check successful",
            "data": {
                "customerId": compliance_details.customerId,
                "complianceType": compliance_details.complianceType
            }
        }
    else:
        response = {
            "status": "failure",
            "message": "Compliance details not found"
        }
    return jsonify(response)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/swagger', methods=['GET'])
def swagger_spec():
    spec_path = "swagger.json"
    with open(spec_path, "r") as f:
        spec = json.load(f)
    return jsonify(spec)

@app.route('/submit-kyc', methods=['POST'])
def submit_kyc():
    print("ComplianceAPI: KYC submission")
    
    try:
        # Get form data
        aadhar_number = request.form.get('aadharNumber')
        pan_number = request.form.get('panNumber')
        
        # Validate form data
        if not aadhar_number or not pan_number:
            return jsonify({
                "status": "failure",
                "message": "Aadhar number and PAN number are required"
            }), 400
        
        # Validate Aadhar format (12 digits)
        if len(aadhar_number) != 12 or not aadhar_number.isdigit():
            return jsonify({
                "status": "failure",
                "message": "Invalid Aadhar number format"
            }), 400
        
        # Validate PAN format (5 letters, 4 digits, 1 letter)
        if len(pan_number) != 10:
            return jsonify({
                "status": "failure",
                "message": "Invalid PAN number format"
            }), 400
        
        # Handle file uploads
        aadhar_file = request.files.get('aadharFile')
        pan_file = request.files.get('panFile')
        
        if not aadhar_file or not pan_file:
            return jsonify({
                "status": "failure",
                "message": "Both Aadhar and PAN documents are required"
            }), 400
        
        # Validate file types
        if not allowed_file(aadhar_file.filename):
            return jsonify({
                "status": "failure",
                "message": "Invalid Aadhar file type. Allowed types: PDF, JPG, JPEG, PNG"
            }), 400
        
        if not allowed_file(pan_file.filename):
            return jsonify({
                "status": "failure",
                "message": "Invalid PAN file type. Allowed types: PDF, JPG, JPEG, PNG"
            }), 400
        
        # Save files
        aadhar_filename = secure_filename(f"aadhar_{aadhar_number}_{aadhar_file.filename}")
        pan_filename = secure_filename(f"pan_{pan_number}_{pan_file.filename}")
        
        aadhar_path = os.path.join(app.config['UPLOAD_FOLDER'], aadhar_filename)
        pan_path = os.path.join(app.config['UPLOAD_FOLDER'], pan_filename)
        
        aadhar_file.save(aadhar_path)
        pan_file.save(pan_path)
        
        # Here you would typically:
        # 1. Store the file paths and user data in the database
        # 2. Trigger document verification process
        # 3. Send confirmation email/SMS
        
        return jsonify({
            "status": "success",
            "message": "KYC documents submitted successfully!",
            "data": {
                "aadharNumber": aadhar_number,
                "panNumber": pan_number,
                "aadharFile": aadhar_filename,
                "panFile": pan_filename
            }
        }), 200
        
    except Exception as e:
        print(f"Error in submit_kyc: {str(e)}")
        return jsonify({
            "status": "failure",
            "message": "An error occurred while processing your request"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Azure's PORT environment variable
    app.run(host="0.0.0.0", port=port)