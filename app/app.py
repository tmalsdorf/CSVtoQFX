from flask import Flask, request, send_file, render_template, redirect, url_for, Response, send_from_directory
import csv
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename
import os
import io

app = Flask(__name__)

def csv_to_ofx(csv_data):
    """
    Converts CSV data of transactions to OFX format.
    Adjust this function based on your specific CSV format and requirements.
    """
    transactions = list(csv.DictReader(csv_data.splitlines()))

    ofx = ET.Element('OFX')
    banktranlist = ET.SubElement(ofx, 'BANKTRANLIST')

    for t in transactions:
        stmttrn = ET.SubElement(banktranlist, 'STMTTRN')
        ET.SubElement(stmttrn, 'TRNTYPE').text = 'DEBIT' if float(t['Amount']) < 0 else 'CREDIT'
        trans_date = format_date(t['Trans. Date'])
        post_date = format_date(t['Post Date'])
        ET.SubElement(stmttrn, 'DTPOSTED').text = post_date
        ET.SubElement(stmttrn, 'DTUSER').text = trans_date
        ET.SubElement(stmttrn, 'TRNAMT').text = t['Amount']
        ET.SubElement(stmttrn, 'MEMO').text = t['Description']

    return ET.tostring(ofx, encoding='unicode')

def format_date(date_str):
    """
    Converts a date from MM/DD/YYYY format to YYYYMMDD.
    """
    month, day, year = date_str.split('/')
    return f"{year}{month.zfill(2)}{day.zfill(2)}"

def convert_transaction(transaction):
    amount = transaction.get('Amount')
    if amount is None:
        return None

    transaction_type = 'DEBIT' if float(amount) < 0 else 'CREDIT'
    return {
        'Type': transaction_type,
        'Trans. Date': transaction.get('Trans. Date', 'N/A'),
        'Post Date': transaction.get('Post Date', 'N/A'),
        'Amount': amount,
        'Description': transaction.get('Description', 'No description')
    }

@app.route('/export-json', methods=['POST'])
def export_json():
    transactions_data = request.json
    return Response(
        json.dumps(transactions_data, indent=2), 
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=transactions.json'}
    )

@app.route('/export-xml', methods=['POST'])
def export_xml():
    transactions_data = request.json
    
    # Create XML root
    root = ET.Element('transactions')
    
    # Add each transaction
    for transaction in transactions_data:
        transaction_elem = ET.SubElement(root, 'transaction')
        for key, value in transaction.items():
            ET.SubElement(transaction_elem, key.replace(' ', '')).text = str(value)
    
    # Convert to pretty-printed XML
    rough_string = ET.tostring(root, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    return Response(
        pretty_xml, 
        mimetype='application/xml',
        headers={'Content-Disposition': 'attachment;filename=transactions.xml'}
    )

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/convert-csv-to-ofx', methods=['POST'])
def convert_csv_to_ofx():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        csv_data = file.read().decode('utf-8')
        transactions_raw = list(csv.DictReader(csv_data.splitlines()))
        
        transactions = [t for t in (convert_transaction(t) for t in transactions_raw) if t is not None]
        
        return render_template('transactions.html', transactions=transactions)
    else:
        return redirect(url_for('index'))

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns a simple JSON response indicating the status of the application.
    """
    return {"status": "healthy", "message": "Service is up and running"}, 200

if __name__ == '__main__':
    app.run(debug=False)
