import requests
import streamlit as st

def get_ollamma_req(text):
    print(text)
    response = requests.post(
        "http://localhost:8000/ks/invoke",
        json={"input":{"topic":text}}
    )
    print(response)
    return response.json()['output']

st.title("Langchain with Ollama2")
text_input = st.text_input("Enter your query")

if text_input:
    st.write(get_ollamma_req(text_input))