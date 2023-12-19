from bardapi import BardCookies
import streamlit as st
from streamlit_chat import message

#arrancalo en terminal con: streamlit run main.py

cookie_dict = {
    "__Secure-1PSID": "xxxxxxxxxx.",
    "__Secure-1PSIDTS": "xxxxxxxxxxxxxxxxx",
    "__Secure-1PSIDCC": "xxxxxxxxxxxxxxxxxxxxx"
}

bard = BardCookies(cookie_dict=cookie_dict)

# message = input("Introduce lo que necesites saber: ")

# print(bard.get_answer(str(message))['content'])

st.title("CalculoIA tutor")

def response_api(promot):
    message = bard.get_answer(str(promot))['content']
    return message

def user_input():
    input_text = st.text_input("Introduce lo que necesitas saber: ")
    return input_text

if 'generate' not in st.session_state:
    st.session_state['generate']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]

user_text =user_input()

if user_text:
    output = response_api(user_text)
    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)

if st.session_state['generate']:
    for i in range(len(st.session_state['generate']) -1, -1, -1):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generate"][i], key=str(i))