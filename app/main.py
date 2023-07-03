from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.answer_generator import *
from app.recap_generator import *
from app.quiz_generator import *
from app.debat_generator import *
from app.apikey import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

app = FastAPI()

@app.post("/answer")
async def make_answer(user_request: UserRequest):
    global g_answer
    g_answer = generate_answer(user_request)
    converted_answer = jsonable_encoder(g_answer)
    return JSONResponse(content=converted_answer)

@app.post("/recap")
async def make_recap(user_request: UserRequest):
    global g_recap
    g_recap = generate_recap(user_request)
    converted_recap = jsonable_encoder(g_recap)
    return JSONResponse(content=converted_recap)

@app.post("/quiz")
async def make_quiz(user_request: UserRequest):
    global g_quiz
    g_quiz = generate_quiz(user_request)
    converted_quiz = jsonable_encoder(g_quiz)
    return JSONResponse(content=converted_quiz)


@app.post("/debat")
async def make_debat(user_request: UserRequest):
    try:
        global g_debat
        g_debat = generate_debat(user_request)
        converted_debat = jsonable_encoder(g_debat)
        return JSONResponse(content=converted_debat)

    except Exception as e:
        print(e)


origins = [
    "http://0.0.0.0:80",
    "http://localhost",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)