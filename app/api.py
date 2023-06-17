from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.answer_generator import *


class UserRequest(BaseModel):
    request_type: Optional[str] # answer, quiz, recap, debat 
    request_contents: Optional[str] = '' # debat, answer 요청일 때만 활성화
    recap_option: Optional[int] = -1 # recap 요청일 때만 활성화, 몇 줄로 요약?
    quize_option: Optional[int] = -1 # quiz 요청일 때만 활성화, 몇 개의 퀴즈 생성?


class TextResult(BaseModel):
    emotion: Optional[str] = "" # happy, sad ...
    txt_result: Optional[str] = "" # answer, dabat, recap

class QuizResult(BaseModel):
    quiz_list: Optional[list] = [] # quize


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

@app.post("/debat")
async def make_debat(user_request: UserRequest):
    # pdf 주제 찾기 -> 해당 주제에 대해 토론
    global g_debat
    g_debat = generate_debat(user_request)
    converted_debat = jsonable_encoder(g_debat)
    return JSONResponse(content=converted_debat)


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