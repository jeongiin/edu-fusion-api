from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from app.models import UserRequest, TextResult
from app.apikey import OPENAI_API_KEY
import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY # openai 에서 발급 받은 key 입력



def generate_answer(user_request: UserRequest) -> TextResult:
     answer_result = TextResult()
     user_input = user_request.request_contents
     base_file_path = os.path.join(os.getcwd(), "app", "data", user_request.edu_class_folder_name, user_request.edu_title_file_name)
     if ".pdf" in base_file_path:
         loader = PyPDFLoader(base_file_path)
     elif ".txt" in base_file_path:
         loader = TextLoader(base_file_path)
     index = VectorstoreIndexCreator().from_loaders([loader])
     # pdf 를 기반으로 답변 생성
     try:
        response = index.query(llm = ChatOpenAI(model_name = 'gpt-3.5-turbo'), question = user_input, chain_type = "stuff")
        answer_result.txt_result = response

     except Exception as err:
        print('[ERROR][GENERATE_ANSWER] : ', str(err))

     return answer_result
     

if __name__ == '__main__':
    # base_file_path = '/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/디지털_트렌드/디지털트렌드_1. 메타버스.pdf'
    base_file_path = '/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/시니어_디지털_범죄/메신저 피싱.txt'
    if ".pdf" in base_file_path:
        loader = PyPDFLoader(base_file_path)
    elif ".txt" in base_file_path:
        loader = TextLoader(base_file_path)

    index = VectorstoreIndexCreator().from_loaders([loader])
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