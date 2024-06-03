from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
# from langchain.chat_models import ChatOpenAI
from langserve import add_routes
from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
import uvicorn
import os

app=FastAPI(
    title="Kashmeen Server",
    version="1.0",
    decsription="A simple API Server"
)


llm = Ollama(model="llama3")
prompt = ChatPromptTemplate.from_template("help on user query on {topic}")

add_routes(
    app,
    prompt|llm,
    path="/ks"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
