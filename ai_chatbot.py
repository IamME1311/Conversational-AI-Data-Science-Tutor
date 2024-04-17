import google.generativeai as gemini
import streamlit as st


f = open("Keys/.gemini_api_key.txt")

api_key = f.read()

gemini.configure(api_key=api_key)
model = gemini.GenerativeModel(model_name="gemini-1.5-pro-latest",
                               system_instruction="""You are tasked to resolve only data science
                               doubts of the user.""")


st.title("💬AI Data Science Tutor")

if "memory" not in st.session_state:
    st.session_state["memory"] = []

chat = model.start_chat(history=st.session_state["memory"])

st.chat_message("ai").write("Hi, How may I help you with Data Science today?")

    
for msg in chat.history:
    name=msg.role
    if name=="model":
        name="ai"
        st.chat_message(name).write(msg.parts[0].text)
    else:
        st.chat_message(msg.role).write(msg.parts[0].text)

user_input = st.chat_input()

if user_input:
    st.chat_message("user").write(user_input)
    response = chat.send_message(user_input, stream=True)
    st.chat_message("ai").write(chunk.text for chunk in response)
    st.session_state["memory"] = chat.history