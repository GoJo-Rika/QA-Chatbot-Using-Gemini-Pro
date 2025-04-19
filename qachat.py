import streamlit as st
import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv() ## Loading all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-2.0-flash-lite")
chat = model.start_chat(history=[])
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

## Initialize our streamlit app
st.set_page_config(page_title="Gemini Q&A Chatbot Demo")

st.header("Gemini Q&A Chatbot Demo")

## Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

## if submit is clicked
if submit and input:
    response = get_gemini_response(input)
    ## Add user query and response to session state chat history
    st.session_state["chat_history"].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("Bot", chunk.text))

st.subheader("The Chat History is")

for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")