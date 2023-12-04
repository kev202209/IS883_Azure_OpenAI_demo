
import streamlit as st
import pandas as pd
import openai
import os
from googletrans import Translator

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, temperature=0.7, use_slang=False):
    prompt = f"Imagine you are a famous singer/songwriter with numerous hit songs. Generate song lyrics for another successful song that will have just as much popularity in the style of {artist_name} and in the {genre} genre."

    # Modify the prompt based on the use_slang parameter
    if use_slang:
        prompt += " Use slang and casual language in the lyrics."

    # Generate lyrics using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=temperature,
    )

    generated_lyric = response['choices'][0]['text']
    return generated_lyric

# Function to translate text from English to German
def translate_to_german(text):
    translator = Translator()
    translation = translator.translate(text, dest='de')
    return translation.text

# Streamlit app
st.title("Lyric Generator Chatbot")

# Get user inputs
artist_name = st.text_input("Enter the artist's name:")
genre = st.text_input("Enter the genre:")
temperature = st.slider("Select temperature", 0.1, 1.0, 0.7, 0.1)
use_slang = st.checkbox("Allow Slang in Lyrics", value=False, key='slang_checkbox', help='Use slang and casual language in the lyrics.', use_container_width=True)

# Toggle button for translation
translate_toggle = st.checkbox("Translate to German", value=False, key='translate_toggle', help='Toggle to translate the generated lyric to German.')

# Logging statements to check the values of use_slang and translate_toggle
st.write(f"use_slang value: {use_slang}")
st.write(f"translate_toggle value: {translate_toggle}")

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, temperature, use_slang)

        # Translate the generated lyric to German if the toggle is on
        translated_lyric = translate_to_german(generated_lyric) if translate_toggle else generated_lyric

        # Display the generated or translated lyric
        st.success(f"Generated Lyric (English):\n{generated_lyric}")
        st.success(f"Translated Lyric (German):\n{translated_lyric}")
    else:
        st.warning("Please fill in the artist's name and genre.")
