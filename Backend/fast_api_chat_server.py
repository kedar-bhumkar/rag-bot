from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from bot_agent_with_memory_api_ready import *
import time

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from constants import *
from bot_agent_with_memory_api_ready import *
from vectorBuilder import *
from sparseIndexBuilder import *

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
    
    userId = request.headers.get('userId')
    print('User Id - ' , userId)
        
    bot_response = chat(userId, message.msg)            
    return {"bot_response": bot_response['output']}




