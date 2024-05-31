import pandas as pd
import numpy as np
import gensim
import nltk
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Initialize NLTK and download necessary data
nltk.download('punkt')

# Load the dataset
file_path = 'toy_dataset_with_probabilities.csv'
df = pd.read_csv(file_path)

# Preprocess the text
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize
    tokens = [word for word in tokens if word.isalpha()]  # Remove non-alphabetic tokens
    return tokens

# Apply preprocessing to the text columns
df['message_tokens'] = df['message'].apply(preprocess_text)
df['recipient_name_tokens'] = df['recipient_name'].apply(preprocess_text)
df['sender_name_tokens'] = df['sender_name'].apply(preprocess_text)

# Train a Word2Vec model on the tokens
all_tokens = df['message_tokens'].tolist() + df['recipient_name_tokens'].tolist() + df['sender_name_tokens'].tolist()
word2vec_model = gensim.models.Word2Vec(all_tokens, vector_size=100, window=5, min_count=1, workers=4)

# Function to get the embedding for a text
def get_text_embedding(tokens, model):
    embedding = np.mean([model.wv[word] for word in tokens if word in model.wv], axis=0)
    if isinstance(embedding, np.ndarray):
        return embedding
    else:
        return np.zeros(model.vector_size)

# Get embeddings for the text columns
df['message_embedding'] = df['message_tokens'].apply(lambda x: get_text_embedding(x, word2vec_model).tolist())
df['recipient_name_embedding'] = df['recipient_name_tokens'].apply(lambda x: get_text_embedding(x, word2vec_model).tolist())
df['sender_name_embedding'] = df['sender_name_tokens'].apply(lambda x: get_text_embedding(x, word2vec_model).tolist())

# Drop the token columns
df = df.drop(columns=['message_tokens', 'recipient_name_tokens', 'sender_name_tokens'])

# Convert embedding columns from lists to arrays of floats
df['message_embedding'] = df['message_embedding'].apply(lambda x: np.array(x, dtype=np.float32))
df['recipient_name_embedding'] = df['recipient_name_embedding'].apply(lambda x: np.array(x, dtype=np.float32))
df['sender_name_embedding'] = df['sender_name_embedding'].apply(lambda x: np.array(x, dtype=np.float32))

# Expand arrays into separate columns
message_embedding_df = pd.DataFrame(df['message_embedding'].tolist(), index=df.index).add_prefix('message_embedding_')
recipient_name_embedding_df = pd.DataFrame(df['recipient_name_embedding'].tolist(), index=df.index).add_prefix('recipient_name_embedding_')
sender_name_embedding_df = pd.DataFrame(df['sender_name_embedding'].tolist(), index=df.index).add_prefix('sender_name_embedding_')

# Concatenate embeddings into the original dataframe
df = pd.concat([df, message_embedding_df, recipient_name_embedding_df, sender_name_embedding_df], axis=1)

# Drop the original embedding columns
df = df.drop(columns=['message_embedding', 'recipient_name_embedding', 'sender_name_embedding'])

# Identify columns with object and datetime64[ns] data types
columns_to_drop = df.select_dtypes(include=['object', 'datetime64[ns]']).columns

# Drop the identified columns
df = df.drop(columns=columns_to_drop, errors='ignore')

# Prepare features and target variable
X = df.drop(columns=['is_scam_prob'])
y = df['is_scam_prob'].apply(lambda x: 1 if x > 0.5 else 0)  # Binarize the scam probability for classification

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
model_path = 'random_forest_scam_model.pkl'
with open(model_path, 'wb') as model_file:
    pickle.dump(rf_model, model_file)

print(f"Model saved to {model_path}")
