from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import openai
from os import path

## for docker build
from app.utils import *
from app.models import UserRequest, TextResult
from app.chatgpt import *
from app.apikey import OPENAI_API_KEY

## for develop environment
# from utils import *
# from models import UserRequest, TextResult
# from chatgpt import *
# from apikey import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY # openai 에서 발급 받은 key 입력


def format_recap(unformated_recap: str, base_file_path: str) -> str:
    # 어투 설정, 자연스러운 번역
    # unformated_recap = en_to_ko(unformated_recap) # 보다 chatGPT가 더 매끄럽게 번역함
    recap_save_path = base_file_path[:-4] + "_recap_ko.txt"
    if path.exists(recap_save_path):
        print("[EXISTS OK] " + recap_save_path)
        file = open(recap_save_path, "r")
        answer = file.read()
         
    else:
        prompt = '공손한 어투의 한국어로 자연스럽게 작성해줘.' + "\n === \n"
        prompt += unformated_recap

        # 메시지 설정하기
        messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
        ]

        answer = ChatGPT(messages=messages)
        save_txt_file(recap_save_path,answer)
    
    return answer

def generate_init_recap(base_file_path: str) -> str:
    # log가 있다면 불러오기
    recap_save_path = base_file_path[:-4] + "_recap.txt"
    if path.exists(recap_save_path):
        print("[EXISTS OK] " + recap_save_path)
        file = open(recap_save_path, "r")
        init_recap = file.read()
         
    else:
        if ".pdf" in base_file_path:
            loader = PyPDFLoader(base_file_path)
            # Combine the pages, and replace the tabs with spaces
            docs = loader.load_and_split()
        elif ".txt" in base_file_path:
            text_splitter = CharacterTextSplitter()
            with open(base_file_path) as f:
                state_of_the_union = f.read()
            texts = text_splitter.split_text(state_of_the_union)
            docs = [Document(page_content=t) for t in texts]
        else :
            print("[ERROR] This file extention is not supported")
            exit()

        llm = OpenAI(temperature=0)
        map_prompt = """
        Write a detailed summary of the following:
        "{text}"
        DETAILED SUMMARY:
        """
        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
        summary_chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt = map_prompt_template)
        init_recap = summary_chain.run(docs)
        save_txt_file(recap_save_path,init_recap)

    return init_recap

def generate_recap(user_request: UserRequest) -> TextResult:
     answer_result = TextResult()
     base_file_path = create_base_path(user_request.edu_class_folder_name, user_request.edu_title_file_name)

     # pdf 를 기반으로 답변 생성
     try:
         generated_recap = generate_init_recap(base_file_path = base_file_path)
         formmated_recap = format_recap(unformated_recap=generated_recap, base_file_path=base_file_path)

         answer_result.txt_result = formmated_recap

     except Exception as err:
         print('[ERROR][GENERATE_RECAP] : ', str(err))

     return answer_result

if __name__ == '__main__':
    ## pdf 기반 방법
    # base_file_path = '/data/디지털_트렌드/디지털트렌드_1. 메타버스.pdf'
    
    ## txt 기반 방법
    user_request = UserRequest()
    base_file_path = create_base_path(user_request.edu_class_folder_name, user_request.edu_title_file_name)

    
    generated_recap = generate_init_recap(base_file_path = base_file_path)
    # generated_recap = 'Messenger phishing is a type of digital crime that takes advantage of social networks to send messages that appear to come from someone close to the victim. The messages often start with something familiar and ask for personal information or to purchase something. It is important to be aware of these tactics and to be suspicious of any messages that appear to come from someone close to you.'
    print(generated_recap)

    formmated_recap = format_recap(unformated_recap = generated_recap)
    print(formmated_recap)