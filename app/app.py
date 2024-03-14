from flask import Flask, request, send_file, render_template, redirect, url_for, Response
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
        
        transactions = []
        for t in transactions_raw:
            # Check if 'Amount' key exists, or use a default value/error handling
            amount = t.get('Amount')
            if amount is None:
                # Handle error, e.g., log it, use a default value, or skip the transaction
                continue  # For now, let's just skip this transaction
            
            transaction_type = 'DEBIT' if float(amount) < 0 else 'CREDIT'
            transactions.append({
                'Type': transaction_type,
                'Trans. Date': t.get('Trans. Date', 'N/A'),  # Provide a default if key doesn't exist
                'Post Date': t.get('Post Date', 'N/A'),
                'Amount': amount,
                'Description': t.get('Description', 'No description')  # Provide a default if key doesn't exist
            })
        
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
