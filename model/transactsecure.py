import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Sample data generation
np.random.seed(42)

# Generating 1000 records
num_records = 1000
names = ['John', 'Harry', 'Alice', 'Bob', 'Charlie', 'David']
transactions = []

# Generate timestamps
start_date = datetime.now() - timedelta(days=365)
timestamps = [start_date + timedelta(seconds=int(x)) for x in np.random.randint(0, 365*24*3600, num_records)]

# Initialize a dictionary to keep track of transaction frequency per user
transaction_count = {name: 0 for name in names}

for i in range(num_records):
    sender = np.random.choice(names)
    recipient = np.random.choice(names)
    while recipient == sender:
        recipient = np.random.choice(names)
    
    amount = np.random.randint(100, 10000)
    transaction_frequency = transaction_count[sender] + 1  # Increment transaction frequency for sender
    credit_rating = np.random.randint(0, 1001)  # Credit rating between 0 and 1000
    is_scam = 0

    # More realistic scam flagging based on credit rating
    if credit_rating < 300:
        is_scam = 1

    transactions.append([timestamps[i], sender, recipient, amount, transaction_frequency, credit_rating, is_scam])
    
    # Update transaction count
    transaction_count[sender] += 1

# Create a DataFrame
columns = ['Timestamp', 'Sender', 'Recipient', 'Amount', 'Transaction_Frequency', 'Credit_Rating', 'Is_Scam']
df = pd.DataFrame(transactions, columns=columns)

# Feature engineering on timestamp
df['Day'] = df['Timestamp'].dt.day
df['Month'] = df['Timestamp'].dt.month
df['Year'] = df['Timestamp'].dt.year
df['Hour'] = df['Timestamp'].dt.hour
df['Minute'] = df['Timestamp'].dt.minute
df['Second'] = df['Timestamp'].dt.second

# Drop the Timestamp column
df = df.drop(columns=['Timestamp'])

# Prepare features and target variable, excluding Sender and Recipient columns
X = df.drop(columns=['Is_Scam', 'Sender', 'Recipient'])
y = df['Is_Scam']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = rf_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Classification Report:\n{report}")

# Save the model using pickle
model_path = 'scam_detection_model.pkl'
with open(model_path, 'wb') as model_file:
    pickle.dump(rf_model, model_file)

print(f"Model saved to {model_path}")
