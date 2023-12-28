from bardapi import BardCookies
import streamlit as st
from streamlit_chat import message
import speech_recognition as sr  # Added for speech recognition
import base64
#import easyocr

#arrancalo en terminal con: streamlit run main.py

cookie_dict = {
    "__Secure-1PSID": "dQgaNyfctb5HwYvtbpqdxHG4ONF-BfabpLjh-TPlFMGvIc3FqflPDNY3NUTrmf-YqXv73Q.",
    "__Secure-1PSIDTS": "sidts-CjEBPVxjSqxAWlTgCpqO9_X9w2vjkuM55qJAO_2HcTJbdJgOSGzYytogI3myaCBXPzJUEAA",
    "__Secure-1PSIDCC": "ABTWhQHFpBFPlI_A322e8P4xmRo9oYqPuCgl5QjoP78-k9saxRX28c4pyoK0Wc4ILnhYlkFPrKM"
}

bard = BardCookies(cookie_dict=cookie_dict)

# message = input("Introduce lo que necesites saber: ")

# print(bard.get_answer(str(message))['content'])

st.title("CalculoIA tutor")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results from speech recognition service; {0}".format(e))
        return ""


def response_api(promot):
    message = bard.get_answer(str(promot))['content']
    return message

def user_input():
    text_input = st.text_input("Introduce lo que necesitas saber: ")
    speech_input = st.button("Hablar")  # Button for speech input

    if speech_input:
        text_input = recognize_speech()

    return text_input

def audio_input():
    uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["mp3", "wav"])
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return audio_base64
    return None

if 'generate' not in st.session_state:
    st.session_state['generate']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]

user_text = user_input()
user_audio = audio_input()

if user_text: # or user_audio:
    if user_audio:
        # Process audio, convert it to text or any other necessary step
        # For simplicity, let's assume the audio processing step is handled
        processed_audio_text = recognize_speech()
        output = response_api(processed_audio_text)
    else:
        output = response_api(user_text)
    
    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)

if st.session_state['generate']:
    for i in range(len(st.session_state['generate']) - 1, -1, -1):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generate"][i], key=str(i))