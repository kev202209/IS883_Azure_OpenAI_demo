import streamlit as st
import pandas as pd
import openai
import os
from nltk.translate.bleu_score import sentence_bleu

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, subject=None, rhyme=None, temperature=0.7, use_slang=False):
    prompt = f"Write the lyrics to a song based on this {genre} that the author wants: {subject}, in similarity to this artist: {artist_name}, and if available create rhymes with this phrase {rhyme}"

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

# Function to calculate BLEU score
def calculate_bleu(reference, candidate):
    reference_tokens = [word.lower() for word in reference.split()]
    candidate_tokens = [word.lower() for word in candidate.split()]
    return sentence_bleu([reference_tokens], candidate_tokens)

# Streamlit app
st.title("Lyric Generator Chatbot")

# Get user inputs
artist_name = st.text_input("Enter the artist's name:")
genre = st.text_input("Enter the genre:")
subject = st.text_input("Subject (Optional):", "Enter the subject for this particular song")
rhyme = st.text_input("Rhyme (Optional):", "Enter a particular word or phrase that you would like used")
temperature = st.slider("Select temperature", 0.1, 1.0, 0.7, 0.1)
use_slang = st.checkbox("Allow Slang in Lyrics", value=False, key='slang_checkbox', help='Use slang and casual language in the lyrics.')

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, subject, rhyme, temperature, use_slang)

        # Get the reference text (replace this with your actual reference text)
        reference_text = "Hello, it's me \n I was wondering if after all these years you'd like to meet \n To go over everything \n They say that time's supposed to heal ya, but I ain't done much healing \n Hello, can you hear me? \n I'm in California dreaming about who we used to be \n When we were younger and free \n I've forgotten how it felt before the world fell at our feet \n There's such a difference between us \n And a million miles"

        # Calculate BLEU score
        bleu_score = calculate_bleu(reference_text, generated_lyric)

        # Display the generated lyric and BLEU score
        st.success(f"Generated Lyric:\n{generated_lyric}")
        st.info(f"BLEU Score: {bleu_score:.2f} (The higher, the better quality)")
    else:
        st.warning("Please fill in the artist's name and genre.")
