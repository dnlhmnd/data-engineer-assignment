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
st.write('2.	Following REST APIs should be implemented.')
st.write("a.	GET request http://localhost:8080/assignment/transaction/{transaction_id} \n\n i.	Type: GET \n\n ii.	Output data JSON: { “transactionId”: 1, “productName”: “P1”, “transactionAmount”: 1000.0, “transactionDatetime”: “2018-01-01 10:10:10”}")
with st.expander("See Code"):
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
st.image(image_url, caption='Image from GitHub', use_column_width=True)