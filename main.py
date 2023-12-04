import streamlit as st
import openai
import os
from deep_translator import GoogleTranslator

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, temperature=0.7, use_slang=False):
    prompt = f"Imagine you are a songwriter. Write the lyrics to a song based on this {genre} in similarity to this artist: {artist_name}. Try your best to mimic the style of the artist"

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

# Function to translate lyrics to Hindi
def translate_to_hindi(text):
    translator = GoogleTranslator()
    translation = translator.translate(text, dest='hi')
    return translation.text

# Streamlit app
st.title("Lyric Generator Chatbot")

# Get user inputs
artist_name = st.text_input("Enter the artist's name:")
genre = st.text_input("Enter the genre:")
temperature = st.slider("Select temperature", 0.1, 1.0, 0.7, 0.1)
use_slang = st.checkbox("Allow Slang in Lyrics", value=False, key='slang_checkbox', help='Use slang and casual language in the lyrics.')
translate_to_hindi_checkbox = st.checkbox("Translate to Hindi", value=False, key='translate_checkbox', help='Translate the generated lyrics to Hindi.')

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, temperature, use_slang)

        # Translate to Hindi if the checkbox is selected
        if translate_to_hindi_checkbox:
            translated_lyric = translate_to_hindi(generated_lyric)
            st.success(f"Generated Lyric (Translated to Hindi):\n{translated_lyric}")
        else:
            st.success(f"Generated Lyric:\n{generated_lyric}")
    else:
        st.warning("Please fill in the artist's name and genre.")
