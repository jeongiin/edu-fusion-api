import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from apikey import OPENAI_API_KEY
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# 
# LangChain PDF Data Loaders
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
loader = PyMuPDFLoader('/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/자료실/[이슈 레포트] 업무활용편_ChatGPT 활용사례 및 활용 팁_최종버전.pdf')
documents = loader.load()

## Text Splitters
## 답변의 정확도를 높이기 위해 PDF를 의미있는 텍스트 단위로 분해함
## chunk_size = 그룹화될 입력 텍스트 수
## chunk_overlap = 연속 텍스트간 최대 겹침
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Leveraging Embeddings
## Embedding Class -> OpenAI, Cohere, Hugging Face 등을 포함한 다양한 임베딩 공급자를 위한 표준화된 인터페이스 역할
## 텍스트를 고차원의 벡터로 재표현함
## persist_directory : 컬렉션이 유지될 디렉터리 경로
## embedding : OpenAIEmbeddings임베딩 공급자를 나타내는 의 인스턴스 생성, 이 인스턴스는 텍스트 모음에 대한 임베딩 생성을 처리
## 매개 변수 가 메서드 persist_directory에 전달되어 Chroma.from_documents특정 디렉터리가 지정되면 컬렉션과 포함 항목이 해당 디렉터리에 유지됨, 반면에 디렉터리를 지정하지 않으면 데이터가 메모리에 저장되고 세션 간에 지속되지 않음.
persist_directory = "./storage"
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, 
                                 embedding=embeddings,
                                 persist_directory=persist_directory)
vectordb.persist()

# Chatting with PDF Documents
retriever = vectordb.as_retriever()
# llm = ChatOpenAI(model_name='gpt-3.5-turbo')
llm = OpenAI()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
        user_input = input("Enter a query: ")
        if user_input == "exit":
            break

        query = f"###Prompt {user_input}"
        try:
            llm_response = qa(query)
            print(llm_response["result"])
        except Exception as err:
            print('Exception occurred. Please try again', str(err))

# print(index.query("보고서 작성용 참고자료 조사 예시의 모든 절차를 알려줘"))