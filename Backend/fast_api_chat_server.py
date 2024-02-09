from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from bot_agent_with_no_memory_api_ready import *
import json
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server startup .....")
    global vector 
    vector = buildIndex()
    print("vector", vector)


    yield

    print("Server shutdown .......")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    msg: str


@app.post("/chat")
def update_item( message: Message):    
    print("Inside /chat")
    print("vector = ", vector)

    bot_response = chat(vector, message.msg)            
    return {"bot_response": bot_response['output']}


def buildIndex():
    print("Building index on server startup ... ")
    loader = CSVLoader(file_path='./data/support-bot.csv')
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(docs)
    vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    return vector    