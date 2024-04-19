import os
import csv
from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

transaction_folder = 'assignment/Transactions'
reference_data_folder = 'assignment/Reference Data'

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
    transaction_data = []
    for filename in os.listdir(transaction_folder):
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
    return transaction_data

# Load transaction and reference data into memory
reference_data_file = os.path.join(reference_data_folder, 'ProductReference.csv')
reference_data = load_reference_data(reference_data_file)

transaction_data_folder = transaction_folder  
transaction_data = load_transaction_data(transaction_data_folder)

# (a)
@app.route('/assignment/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    for transaction in transaction_data:
        if int(transaction['transactionId']) == transaction_id:
            product_info = reference_data.get(transaction['productId'], {})
            return jsonify({
                'transactionId': transaction['transactionId'],
                'productName': product_info.get('productName', ''),
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