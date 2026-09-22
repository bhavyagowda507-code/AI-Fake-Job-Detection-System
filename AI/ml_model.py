# ml_model.py
import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("⚡ Starting machine learning training sequence...")

# Balanced training text matrix
data = {
    'text': [
        "We are looking for a Software Engineer with experience in Python, Flask, and SQL. Full benefits and competitive salary offered.",
        "Seeking a full-time Data Analyst to manage database queries, generate weekly financial reports, and collaborate with product teams.",
        "Join our team as an Administrative Assistant. Duties include scheduling meetings, managing emails, and greeting clients in the office.",
        "Looking for a Remote Package Processing Agent. Receive shipped boxes at your house, repackage them, and mail them out immediately.",
        "Earn easy cash online daily! Deposit company funds into your personal bank account and send cryptocurrency tokens back to us.",
        "Immediate opening for Data Entry Clerk. To begin the immediate onboarding setup, please text our hiring manager on Telegram right now."
    ],
    'label': [0, 0, 0, 1, 1, 1]  # 0 = SAFE, 1 = SCAM
}

df = pd.DataFrame(data)

# Extract Features
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Train Model
model = LogisticRegression()
model.fit(X, y)

print("💾 Writing .pkl files directly into the backend directory...")
# Save files right here where app.py can see them
with open('job_vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

with open('job_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("✨ SUCCESS: 'job_vectorizer.pkl' and 'job_model.pkl' created cleanly!")