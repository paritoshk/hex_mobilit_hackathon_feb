import streamlit as st
import pandas as pd
import speech_recognition as sr
import openai
import datetime
OPEN_AI_KEY = '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'
# Assuming 'audiorecorder' is a placeholder function, as Streamlit does not natively support this out of the box.
# This requires an external library or custom implementation for audio recording.
from audiorecorder import audiorecorder  # Assuming audiorecorder is a custom component or external library

# Function to convert speech to text
def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"

# Function to record audio and transcribe it, then send to LLM for processing
def record_and_transcribe():
    st.title("Safety Check 🎙️")
    audio = audiorecorder("Click to record", "Click to stop recording", key="recorder")
    
    if len(audio) > 0:
        audio_data = audio.export()  # Export as IO Bytes
        st.audio(audio_data.read(), format="audio/wav")
        audio_file_path = "audio.wav"
        audio.export(audio_file_path, format="wav")
        text = speech_to_text(audio_file_path)
        st.write("Transcribing... ", text)
        # Placeholder for sending the transcribed text to an LLM for processing
        if text:
            # This function should handle sending the text to your LLM and processing the response
            process_safety_query(text)

# Placeholder for processing the query with an LLM
# Placeholder function for processing the safety query


def process_safety_query(user_query:str, dataframe:pd.DataFrame):
    # Convert the current dataframe state to JSON
    dataframe_json = dataframe.to_json()
    
    # Get the current datetime
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Craft a message that includes the datetime, user query, and dataframe JSON
    system_message = f"You are a helpful assistant. Provide safety information based on the current crime data. Current datetime: {datetime_now}."
    user_message = f"{user_query} Data: {dataframe_json}"
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # Replace with the appropriate model name, e.g., "gpt-4" if available
            messages=[
                {"role": "system", "content": system_message},
                {"role": "assistant","content":"Yes, I am ready to help you! Please share the data about street and incidents to support you!"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=50  # Adjust as necessary to fit your output requirements
        )
        return completion.choices[0].message
    except Exception as e:
        return str(e)
    

def main():
    st.header("Welcome to the Safety Advisor App 🛡️")
    
    # User inputs for personalization
    age = st.selectbox("Select your age range:", ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or older"], key='age')
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"], key='gender')
    build = st.selectbox("Select your build:", ["Small", "Medium", "Large"], key='build')

    # Display user inputs for confirmation
    st.write(f"Your profile: Age range - {age}, Gender - {gender}, Build - {build}")

    # Map visualization placeholder
    st.header("Map 🗺️ - Select Your Location")
    # Dummy data for map demonstration
    data = pd.DataFrame({'lat': [40.7128, 34.0522], 'lon': [-74.0060, -118.2437]})
    st.map(data)

    # Voice query section
    st.header("Ask a Safety Question 🎤")

    record_and_transcribe()

if __name__ == "__main__":
    main()
