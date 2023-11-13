import streamlit as st
import pandas as pd
import openai
import os


openai.api_key = os.environ.get('OPENAI_API_KEY')


def generate_lyrics(artist_name, genre, temperature=0.7):
    prompt = f"Imagine you are a famous singer/songwriter with numerous hit songs. Generate song lyrics for another successful song that will have just as much popularity in the style of {artist_name} and in the {genre} genre."

    # Generate lyrics using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can experiment with different engines
        prompt=prompt,
        max_tokens=200,  # Adjust max_tokens as needed
        temperature=temperature,
    )

    generated_lyric = response['choices'][0]['text']
    return generated_lyric

# Streamlit app
st.title("Lyric Generator Chatbot")

# Get user inputs
artist_name = st.text_input("Enter the artist's name:")
genre = st.text_input("Enter the genre:")
temperature = st.slider("Select temperature", 0.1, 1.0, 0.7, 0.1)

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, temperature)

        # Display the generated lyric
        st.success(f"Generated Lyric:\n{generated_lyric}")
    else:
        st.warning("Please fill in the artist's name and genre.")
