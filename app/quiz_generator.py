from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from models import UserRequest, TextResult
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import openai
from utils import en_to_ko, save_txt_file
from os import path
from apikey import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def generate_init_quiz(recap: str) -> str:
    # recap을 통해 객관식 퀴즈 생성
    prompt = '아래 내용으로 객관식 퀴즈를 만들어줘. 틀린 보기를 만들 때 너가 이미 알고 있는 지식을 이용할 수 있어.' + "\n === \n"
    prompt += recap
    
    # openai API 키 인증
    openai.api_key = OPENAI_API_KEY

    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    
    return answer