import streamlit as st
import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader

groq_api_key = "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"

st.title("ChatBot")

# llm = Ollama(model="llama3")
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")


prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

def vector_embedding():
    if 'vectors' not in st.session_state:
        st.session_state.embeddings=OllamaEmbeddings()
        st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

prompt=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}

    """
    )

if st.button("Documents Embedding"):
    vector_embedding()

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = st.session_state.vectors.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

prompt = st.text_input("Enter your query here")

if prompt:
    response = retrieval_chain.invoke({"input":prompt})
    st.write(response['answer'])
