import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Load the model
model_path = 'scam_detection_model.pkl'
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Function to make predictions
def predict_scam(transaction_details):
    df = pd.DataFrame([transaction_details])
    prediction = model.predict(df)
    return prediction[0]

# Streamlit UI
st.title("Scam Detection Model")

st.write("Enter transaction details:")

# Input fields
sender = st.selectbox("Sender", ['John', 'Harry', 'Alice', 'Bob', 'Charlie', 'David'])
recipient = st.selectbox("Recipient", ['John', 'Harry', 'Alice', 'Bob', 'Charlie', 'David'])
amount = st.number_input("Amount", min_value=0, max_value=10000, value=1000)
transaction_frequency = st.number_input("Transaction Frequency", min_value=1, max_value=100, value=1)
credit_rating = st.number_input("Credit Rating", min_value=0, max_value=1000, value=500)

# Feature engineering on current timestamp
now = datetime.now()
day = now.day
month = now.month
year = now.year
hour = now.hour
minute = now.minute
second = now.second

# Prepare the input data
transaction_details = {
    'Amount': amount,
    'Transaction_Frequency': transaction_frequency,
    'Credit_Rating': credit_rating,
    'Day': day,
    'Month': month,
    'Year': year,
    'Hour': hour,
    'Minute': minute,
    'Second': second
}

if st.button("Predict"):
    prediction = predict_scam(transaction_details)
    if prediction == 1:
        st.write("Warning: This transaction is predicted to be a scam.")
    else:
        st.write("This transaction is not predicted to be a scam.")
