# Import necessary libraries
import streamlit as st
import openai
import pandas as pd
import os

# Load your dataset
queen_lyrics = pd.read_csv('path_to_queen_lyrics.csv')  # Load your dataset here

# Set up your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize Streamlit
st.title("Lyrics Generator")

# Create a text input field for user queries
user_input = st.text_input("Ask a question:")

# Function to generate lyrics based on user input and dataset
def generate_lyrics(user_input):
    combined_lyrics = '\n'.join(queen_lyrics['lyrics'].dropna().tolist())
    prompt = f"Generate lyrics inspired by: {user_input}\n\n{combined_lyrics}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response['choices'][0]['text'].strip()

# Generate and display lyrics based on user input
if user_input:
    generated_lyrics = generate_lyrics(user_input)
    st.write(generated_lyrics)
