import pandas as pd
import numpy as np
import gensim
import nltk
from nltk.tokenize import word_tokenize

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

# Combine all tokens into one list
all_tokens = df['message_tokens'].tolist() + df['recipient_name_tokens'].tolist() + df['sender_name_tokens'].tolist()

# Train a Word2Vec model on the tokens
word2vec_model = gensim.models.Word2Vec(all_tokens, vector_size=100, window=5, min_count=1, workers=4)

# Save the Word2Vec model
word2vec_model.save("word2vec_model.bin")

print("Word2Vec model saved as word2vec_model.bin")
