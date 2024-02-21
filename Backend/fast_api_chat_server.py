from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from bot_agent_with_memory_api_ready import *
import json
import time

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever
from constants import *
from bot_agent_with_memory_api_ready import *

vector = None
sparseIndex = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server startup .....")
    global vector
    global sparseIndex

    sparseIndex = None
    print("sparseIndex", sparseIndex)

    vector = buildVectorIndex()
    print("vector", vector)

    if(ENABLE_HYBRID_SEARCH):
        sparseIndex = buildSparseIndex()
    
    print("sparseIndex ", sparseIndex)

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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Request took {process_time} secs to complete")
    return response

class Message(BaseModel):
    msg: str


@app.post("/chat")
def update_item( request:Request, message: Message):    
    print("Inside /chat")
    print("vector = ", vector)

    userId = request.headers.get('userId')
    print('User Id - ' , userId)
    
    
    bot_response = chat(userId, message.msg)            
    return {"bot_response": bot_response['output']}


def buildVectorIndex():
    global documents
    print("Building index on server startup ... ")
    loader = CSVLoader(file_path='./data/support-bot.csv')
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(docs)
    # vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    # vector = FAISS.from_documents(documents, OpenAIEmbeddings()).as_retriever(search_kwargs={"k": 3})
    vector = FAISS.from_documents(documents, OpenAIEmbeddings()).as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5, "k": 3} )
    
    return vector    


# BM25 aims to find the best matching documents for a given search query by considering the frequency of terms, their rarity across documents, and adjusting for document length. It strikes a balance between precision and recall in information retrieval systems.
def buildSparseIndex():
    print("Building sparse index on server startup ... ", documents)
    bm25_retriever = BM25Retriever.from_documents(documents) 
    bm25_retriever.k = 2

    return bm25_retriever