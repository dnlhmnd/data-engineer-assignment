import os
import csv
import time
import threading
from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

transaction_folder = 'assignment/Transactions'
reference_data_folder = 'assignment/Reference Data'

# Shared data structures
reference_data = {}
transaction_data = []

def load_reference_data(reference_data_file):
    reference_data = {}
    with open(reference_data_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reference_data[row['productId']] = {
                'productName': row['productName'],
                'productManufacturingCity': row['productManufacturingCity']
            }
    return reference_data

def load_transaction_data(transaction_folder):
    global transaction_data
    
    processed_files = set()
    
    while True:

        files = os.listdir(transaction_folder)
        
        # Check for new files
        new_files = [file for file in files if file not in processed_files]
        
        # Process new files
        for filename in new_files:
            if filename.endswith('.csv'):
                file_path = os.path.join(transaction_folder, filename)
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        transaction_data.append({
                            'transactionId': row['transactionId'],
                            'productId': row['productId'],
                            'transactionAmount': row['transactionAmount'],
                            'transactionDatetime': row['transactionDatetime']
                        })

                processed_files.add(filename)

        time.sleep(3)  

# Load reference data
reference_data_file = os.path.join(reference_data_folder, 'ProductReference.csv')
reference_data = load_reference_data(reference_data_file)

# Start the transaction data loader thread
transaction_loader_thread = threading.Thread(target=load_transaction_data, args=(transaction_folder,))
transaction_loader_thread.daemon = True
transaction_loader_thread.start()

# (a)
@app.route('/assignment/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    for transaction in transaction_data:
        if int(transaction['transactionId']) == transaction_id:
            product_info = reference_data.get(transaction['productId'], {})
            return jsonify({
                'transactionId': transaction['transactionId'],
                'productName': product_info.get('productName', 'Unknown Product'),
                'transactionAmount': float(transaction['transactionAmount']),
                'transactionDatetime': transaction['transactionDatetime']
            })
    return jsonify({'error': 'Transaction not found'}), 404

# (b)
@app.route('/assignment/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
def get_transaction_summary_by_products(last_n_days):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=last_n_days)
    summary = {}

    for transaction in transaction_data:
        transaction_date = datetime.strptime(transaction['transactionDatetime'], '%Y-%m-%d %H:%M:%S')
        if start_date <= transaction_date <= end_date:
            product_id = transaction['productId']
            product_name = reference_data.get(product_id, {}).get('productName', 'Unknown Product')
            transaction_amount = float(transaction['transactionAmount'])
            summary[product_name] = summary.get(product_name, 0) + transaction_amount

    formatted_summary = [{'productName': product_name, 'totalAmount': total_amount} for product_name, total_amount in summary.items()]

    return jsonify({'summary': formatted_summary})

# (c)
@app.route('/assignment/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
def get_transaction_summary_by_manufacturing_city(last_n_days):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=last_n_days)
    summary = {}

    for transaction in transaction_data:
        transaction_date = datetime.strptime(transaction['transactionDatetime'], '%Y-%m-%d %H:%M:%S')
        if start_date <= transaction_date <= end_date:
            product_id = transaction['productId']
            product_info = reference_data.get(product_id, {})
            manufacturing_city = product_info.get('productManufacturingCity', 'Unknown City')
            transaction_amount = float(transaction['transactionAmount'])
            summary[manufacturing_city] = summary.get(manufacturing_city, 0) + transaction_amount

    formatted_summary = [{'cityName': city_name, 'totalAmount': total_amount} for city_name, total_amount in summary.items()]

    return jsonify({'summary': formatted_summary})

if __name__ == '__main__':
    app.run(debug=True)#, port=8080)