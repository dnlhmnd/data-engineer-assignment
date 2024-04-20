import streamlit as st
import pandas as pd

st.title('Data Engineer Role Application Assignment at OneByZero')
st.write('This is a breakdown and demo of the application I created for the Data Engineer - Coding Assignment.')
st.write("")
st.write("**Assignment Objective:** As part of your evaluation, we will need you to complete a coding assignment that will help us understand your fit with the opening at OnebyZero.")
st.write("")
st.write('**Description of assignment:**')
st.write('Assignment Environment:\n1.	This application populates and provides retrieval features for transactions of a company.\n\n2.	Transaction information is coming as files (let’s say every 5 minutes) in a folder.')
st.write('3.	Another folder contains a file, which contains reference data for products, against which the transactions are happening.\n4.	This application is an in-memory application so no persistent storage is required. i.e. You can reload the already available data in the transaction folder upon start-up of the application.')
st.write('5.	A transaction record contains following attributes in a comma separated format\n')

tran_data = {
    'transactionId': [1, 2, 3, 4, 5, 6],
    'productId': [10, 10, 20, 10, 30, 20],
    'transactionAmount': [1000.0, 1000.0, 2000.0, 1000.0, 3000.0, 2000.0],
    'transactionDatetime': ['2018-10-01 10:10:10', '2018-10-01 10:15:10', '2018-10-01 10:15:20',
                             '2018-10-01 10:10:10', '2018-10-01 10:20:10', '2018-10-01 10:15:30']
}
tran_df = pd.DataFrame(tran_data)
st.dataframe(tran_df)

st.write('6.	The product reference data have following attributes in a CSV.')

product_data = {
    'productId': [10, 20, 30],
    'productName': ['P1', 'P2', 'P3'],
    'productManufacturingCity': ['C1', 'C1', 'C2']
}
product_df = pd.DataFrame(product_data)
st.dataframe(product_df)

st.write('7.	Reference data is static and transaction data keeps coming in real-time in their respective folders.')
st.write("")
st.write('**Implementation Language: Python**')
st.write('Following REST APIs should be implemented.')
st.write("**a.	GET request http://localhost:8080/assignment/transaction/{transaction_id}** \n\n i.	Type: GET \n\n ii.	Output data JSON: { “transactionId”: 1, “productName”: “P1”, “transactionAmount”: 1000.0, “transactionDatetime”: “2018-01-01 10:10:10”}")
with st.expander("See code snippet"):
    code = '''@app.route('/assignment/transaction/<int:transaction_id>', methods=['GET'])
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
    return jsonify({'error': 'Transaction not found'}), 404'''
    st.code(code, language='python')

image_url = 'images/SS1.png'
st.image(image_url, use_column_width=True)
st.caption("I used the default port of Streamlit because I already have an existing connection for port 8080 in my local machine")

st.write("")
st.write("**b.	GET request http://localhost:8080/assignment/transactionSummaryByProducts/{last_n_days}**\n\ni.	Type: GET\n\nii.	Output data JSON: { “summary”:  [ {“productName”: “P1”, {“totalAmount”: 3000.0}]}")
with st.expander("See code snippet"):
    code = '''@app.route('/assignment/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
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

    return jsonify({'summary': formatted_summary})'''
    st.code(code, language='python')

image_url = 'images/SS2.png'
st.image(image_url, use_column_width=True)
st.caption("I had to use high value on {last_n_days} because the latest date on Transaction_20180101101010.csv is 2018 only, according to the assignment 'summary of transactions during the last 10 days from current date' which is 2024")

st.write("")
st.write("**c.	GET request http://localhost:8080/assignment/transactionSummaryByManufacturingCity/{last_n_days}**\n\ni.	Type: GET\n\nii.	Output data JSON: { “summary”:  [ {“cityName”: “C1”, {“totalAmount”: 3000.0}]}")
with st.expander("See code snippet"):
    code = '''@app.route('/assignment/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
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

    return jsonify({'summary': formatted_summary})'''
    st.code(code, language='python')

image_url = 'images/SS3.png'
st.image(image_url, use_column_width=True)
st.caption("I had to use high value on {last_n_days} for the same reason as task (b)")

st.write("")
st.write("To check if the application updates the transaction information when new files are uploaded in the folder I utilized Python's threading to continously check the 'Transaction' folder every 3 seconds when the application starts")
dummy_data = {
    "transactionId": [7, 8, 9, 10],
    "productId": [30, 40, 50, 60],
    "transactionAmount": [3000.0, 4000.0, 5000.0, 6000.0],
    "transactionDatetime": [
        "2018-10-01 10:25:10", "2018-10-01 10:30:10", "2018-10-01 10:35:10",
        "2018-10-01 10:40:10"
    ]
}

df = pd.DataFrame(dummy_data)
st.write("Dummy data (data-engineer-assignment/Transaction_test.csv) ")
st.write(df)

st.write("As you can see, the transaction information got updated after I copied the dummy data to the 'Transaction' folder")