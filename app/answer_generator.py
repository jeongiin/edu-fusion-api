from typing import Union
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from pydantic import BaseModel
import os
from api import UserRequest, TextResult
from apikey import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
loader = PyPDFLoader('/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/자료실/[이슈 레포트] 업무활용편_ChatGPT 활용사례 및 활용 팁_최종버전.pdf')
index = VectorstoreIndexCreator().from_loaders([loader])


def generate_answer(user_request: UserRequest) -> TextResult:
     answer_result = TextResult()

     # pdf 를 기반으로 답변 생성
     try:
                response = index.query(llm = ChatOpenAI(model_name = 'gpt-3.5-turbo'), question = user_input, chain_type = "stuff")
                answer_result.txt_result = response

     except Exception as err:
                print('[ERROR][GENERATE_ANSWER] : ', str(err))

     return answer_result
     

if __name__ == '__main__':
    while True:
            user_input = input("Enter a query: ")
            if user_input == "exit":
                break

            query = f"###Prompt {user_input}"
            try:
                response = index.query(llm = ChatOpenAI(model_name = 'gpt-3.5-turbo'), question = user_input, chain_type = "stuff")
                print(response)
            except Exception as err:
                print('Exception occurred. Please try again', str(err))

                # 보고서 작성용 참고자료 조사 예시의 모든 절차를 알려줘