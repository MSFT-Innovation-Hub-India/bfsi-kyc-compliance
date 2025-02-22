import os
import sys
from flask import Flask, request, jsonify
import pyodbc
import json

from config import DefaultConfig
configParams = DefaultConfig()

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect(f'DRIVER={configParams.driver};SERVER={configParams.server};PORT=1433;DATABASE={configParams.database};UID={configParams.username};PWD={configParams.password}')
    return conn

@app.route('/kyc', methods=['GET'])
def kyc_validation():
    print("ComplianceAPI: KYC validation")
    customer_id = request.args.get('customerID')
    conn = get_db_connection()
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
@app.route('/swagger.json', methods=['GET'])
def swagger_spec():
    spec_path = "swagger.json"
    with open(spec_path, "r") as f:
        spec = json.load(f)
    return jsonify(spec)

if __name__ == '__main__':
    app.run(debug=True)