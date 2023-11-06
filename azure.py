import streamlit as st
import pandas as pd
import openai
import os

# Load your dataset
file_path = "lyrics_dataset_all.csv"  # Update the path to your dataset
df = pd.read_csv(file_path)

# Filter the dataset to keep only the 'track_artist' and 'lyrics' columns
artist_lyrics = df[['artist', 'lyrics']]

# Set up your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Streamlit app title
st.title("Lyrics Generator")

# Dropdown to select the artist
selected_artist = st.selectbox('Select an artist:', artist_lyrics['artist'].unique())

# Function to generate lyrics based on selected artist
def generate_lyrics(artist):
    artist_lyrics = df[df['artist'] == artist]['lyrics'].dropna().tolist()
    combined_lyrics = '\n'.join(artist_lyrics[:5])
    combined_lyrics = combined_lyrics[:2048]
    prompt = f"Generate lyrics in the style of {artist}\n\n{combined_lyrics}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response['choices'][0]['text'].strip()

# Generate and display lyrics based on the selected artist
if selected_artist:
    generated_lyrics = generate_lyrics(selected_artist)
    st.write(generated_lyrics)
