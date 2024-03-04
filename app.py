import streamlit as st
import nltk
import requests
import speech_recognition as sr
from rake_nltk import Rake

nltk.download('stopwords')
nltk.download('punkt')

# Replace with your actual API key and search engine ID
API_KEY = 'AIzaSyAjwvDJmEdbWhrzWR-17OctIS0ib4zfneU'
# Replace with your actual Custom Search Engine ID
SEARCH_ENGINE_KEY = '7564b8c73e277468a'


# Function to transcribe speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak into the microphone")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Speech not recognized")
        except sr.RequestError as e:
            st.error(f"Could not request results: {e}")

# Function to extract keywords using RAKE
def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords_with_scores = r.get_ranked_phrases_with_scores()
    return [keyword for score, keyword in keywords_with_scores if score > 5]

# Streamlit app
st.set_page_config(layout="wide")

def main():
    st.title("Speech to Text Image Search")

    # Button to start speech to text conversion
    if st.button("Start Speech to Text"):
        transcribed_text = speech_to_text()
        if transcribed_text:
            st.info("Transcription complete:")
            st.write(transcribed_text)

            # Extract keywords from the transcribed text
            st.subheader("Extracted Keywords")
            keywords = extract_keywords(transcribed_text)
            st.write(keywords)

            # Use the transcribed text as the search query for image search
            search_query = ' '.join(keywords)
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'q': search_query,
                'key': API_KEY,
                'cx': SEARCH_ENGINE_KEY,
                'searchType': 'image'
            }

            response = requests.get(url, params=params)
            results = response.json().get('items', [])

            # Display the first two images side by side
            st.subheader("Image Search Results")
            if len(results) >= 2:
                col1, col2 = st.columns(2)
                col1.image(results[0]['link'], caption="Image 1", use_column_width=True)
                col2.image(results[1]['link'], caption="Image 2", use_column_width=True)
            else:
                st.warning("Not enough images found for display.")

if __name__ == "__main__":
    main()