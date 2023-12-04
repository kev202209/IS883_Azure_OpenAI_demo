import streamlit as st
import pandas as pd
import openai
import os

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, subject=None, rhyme=None, temperature=0.7, use_slang=False):
    prompt = f"Imagine you are a songwriter. Write the lyrics to a song based on this {genre} that the author wants: {subject}, in similarity to this artist: {artist_name}, and if available create rhymes with this phrase {rhyme}. Try your best to match the style of the artist. Unless specified, do not use slang or casual langauge in the lyrics generated."

    # Modify the prompt based on the use_slang parameter
    if use_slang:
        prompt += " You are allowed to use slang and casual language in the lyrics in this case."

    # Generate lyrics using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=temperature,
    )

    generated_lyric = response['choices'][0]['text']
    return generated_lyric

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

        # Display the generated lyric
        st.success(f"Generated Lyric:\n{generated_lyric}")

        # Ask for user feedback
        user_feedback = st.selectbox("How satisfied are you with the generated lyric?", ["Satisfied", "Neutral", "Dissatisfied"])

        # Use user feedback to refine the model if dissatisfied
        if user_feedback == "Dissatisfied":
            st.info("Thank you for your feedback! We will use this to improve our lyric generation.")
            # You can include logic here
