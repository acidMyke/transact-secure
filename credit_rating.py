import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Load your data
data = pd.read_csv('your_data.csv')

# Feature engineering
# Assume 'amount', 'frequency', 'recipient_name', 'sender_name' are columns in your data
data['transaction_frequency'] = data.groupby('sender_name')['amount'].transform('count')
data['recipient_frequency'] = data.groupby('recipient_name')['amount'].transform('count')

# Define features and target for fraud detection
X_fraud = data[['amount', 'transaction_frequency', 'recipient_frequency']]
y_fraud = data['is_fraud']

# Train-test split for fraud detection
X_train_fraud, X_test_fraud, y_train_fraud, y_test_fraud = train_test_split(X_fraud, y_fraud, test_size=0.3, random_state=42)

# Train Isolation Forest for fraud detection
iso_forest = IsolationForest(contamination=0.01, random_state=42)
iso_forest.fit(X_train_fraud)

# Predict fraud on test set
y_pred_fraud = iso_forest.predict(X_test_fraud)
y_pred_fraud = [1 if pred == -1 else 0 for pred in y_pred_fraud]

# Evaluate fraud detection model
print("Fraud Detection Model")
print(classification_report(y_test_fraud, y_pred_fraud))

# Define features and target for credit rating prediction
X_credit = data[['amount', 'transaction_frequency', 'recipient_frequency']]
y_credit = data['credit_rating']  # Assume credit_rating is encoded as 0, 1, 2 for C, B, A

# Train-test split for credit rating prediction
X_train_credit, X_test_credit, y_train_credit, y_test_credit = train_test_split(X_credit, y_credit, test_size=0.3, random_state=42)

# Train Random Forest for credit rating prediction
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train_credit, y_train_credit)

# Predict credit rating on test set
y_pred_credit = rf_classifier.predict(X_test_credit)

# Evaluate credit rating model
print("Credit Rating Prediction Model")
print(classification_report(y_test_credit, y_pred_credit))

# Output example
def get_credit_rating(amount, recipient_name):
    recipient_data = data[data['recipient_name'] == recipient_name]
    if recipient_data.empty:
        return "Recipient not found"
    
    recipient_data['transaction_frequency'] = len(recipient_data)
    recipient_data['recipient_frequency'] = len(recipient_data[recipient_data['recipient_name'] == recipient_name])
    
    rating_pred = rf_classifier.predict(recipient_data[['amount', 'transaction_frequency', 'recipient_frequency']])
    return rating_pred[0]

# Example usage
amount = 5000
recipient_name = 'Harry'
credit_rating = get_credit_rating(amount, recipient_name)
print(f"Credit rating for {recipient_name}: {credit_rating}")
