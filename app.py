import streamlit as st
import pandas as pd
import speech_recognition as sr
from openai import OpenAI
from datetime import datetime
from audiorecorder import audiorecorder

# Assuming 'audiorecorder' is a placeholder function, as Streamlit does not natively support this out of the box.
# This requires an external library or custom implementation for audio recording.
  # Assuming audiorecorder is a custom component or external library
def load_data():
    # Load the dataset
    df = pd.read_csv('Streamlit_input.csv')
    
    # List of dangerous crime subcategories to filter
    dangerous_crimes = [
        'Theft From Vehicle', 'Weapons Offense', 'Larceny Theft - Bicycle',
        'Larceny - From Vehicle', 'Larceny Theft - Shoplifting'
    ]
    
    # Filter the DataFrame for rows where 'Incident Subcategory' is in the list of dangerous crimes
    filtered_df = df[df['Incident Subcategory'].isin(dangerous_crimes)]
    
    return filtered_df.reset_index().head(20)
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
def record_and_transcribe(user_query,dataframe,):
    st.title("Safety Check 🎙️")
    audio = audiorecorder("Click to record", "Click to stop recording", key="recorder")
    
    if len(audio) > 0:
        audio_data = audio.export()  # Export as IO Bytes
        st.audio(audio_data.read(), format="audio/wav")
        audio_file_path = "audio.wav"
        audio.export(audio_file_path, format="wav")
        text = speech_to_text(audio_file_path)
        st.write("Transcribing... ", text)
        if text:
            return st.write(process_safety_query(user_query,text,dataframe))
        # Placeholder for sending the transcribed text to an LLM for processing

# Placeholder for processing the query with an LLM
# Placeholder function for processing the safety query


client = OpenAI(api_key=st.secrets["OPEN_AI_KEY"])

def process_safety_query(user_query:str,user_input:str, dataframe:pd.DataFrame):
    # Convert the current dataframe state to JSON
    dataframe_json = dataframe.to_json()
    
    # Get the current datetime
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Craft a message that includes the datetime, user query, and dataframe JSON
    system_message = f"You are a helpful assistant. Tell if current street is safe or not, dont summarize the data information based on the current crime data. Current datetime: {datetime_now}."
    user_message = f"{user_query+user_input} Data: {dataframe_json}"
    
    completion = client.chat.completions.create(
            model="gpt-4-1106-preview",  # Replace with the appropriate model name, e.g., "gpt-4" if available
            messages=[
                {"role": "system", "content": system_message},
                {"role": "assistant","content":"Yes, I am ready to help you! Please share the data about street and incidents to support you!"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=75,
            temperature = 0.15# Adjust as necessary to fit your output requirements
        )
    return completion.choices[0].message

def main():
    st.header("Welcome to the Safety Advisor App 🛡️")
    
    # User inputs for personalization
    age = st.sidebar.selectbox("Select your age range:", ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or older"], key='age')
    gender = st.sidebar.selectbox("Select your gender:", ["Male", "Female", "Other"], key='gender')
    build = st.sidebar.selectbox("Select your build:", ["Small", "Medium", "Large"], key='build')
    user_info = ''.join([age,gender,build])

    # Display user inputs for confirmation
    st.write(f"Your profile: Age range - {age}, Gender - {gender}, Build - {build}")

    # Map visualization placeholder
    st.header("Map 🗺️ - Select Your Location")
    # Dummy data for map demonstration
    data = load_data()
    st.map(data,latitude='Latitude',longitude='Longitude',color="#ffffff",size=2,zoom=19)

    # Voice query section
    st.header("Ask a Safety Question 🎤")

    record_and_transcribe(user_info,data)
if __name__ == "__main__":
    main()
