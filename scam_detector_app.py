import streamlit as st
import pandas as pd

# Load the database
df = pd.read_csv('credit_scores.csv')

# Function to get the credit rating based on the credit score
def get_credit_rating(score):
    if score > 750:
        return 'A'
    elif score > 500:
        return 'B'
    else:
        return 'C'

# Streamlit app
st.title("Credit Rating Checker")

st.header("Enter the person's name below:")

# User input
name = st.text_input("Name")

# Check the credit score and rating
if st.button("Check Rating"):
    if name in df['name'].values:
        credit_score = df.loc[df['name'] == name, 'credit_score'].values[0]
        rating = get_credit_rating(credit_score)
        st.write(f"The credit score for {name} is {credit_score}, which corresponds to a rating of {rating}.")
    else:
        st.write("Name not found in the database.")
