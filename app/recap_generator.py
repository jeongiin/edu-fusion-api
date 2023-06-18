from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from apikey import OPENAI_API_KEY
from models import UserRequest, TextResult
from langchain.prompts import PromptTemplate
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def generate_recap(user_request: UserRequest, index) -> TextResult:
     answer_result = TextResult()

     # pdf 를 기반으로 답변 생성
     try:
            response = "내용을 넣어라"
            answer_result.txt_result = response

     except Exception as err:
            print('[ERROR][GENERATE_RECAP] : ', str(err))

     return answer_result

if __name__ == '__main__':
    loader = PyPDFLoader('/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/자료실/[이슈 레포트] 업무활용편_ChatGPT 활용사례 및 활용 팁_최종버전.pdf')
    docs = loader.load_and_split()
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    llm = OpenAI(temperature=0)
    map_prompt = """
        Write a concise summary of the following:
        "{text}"
        CONCISE SUMMARY:
    """
    combine_prompt = """
    Write a concise summary of the following text delimited by triple backquotes.
    Return your response in bullet points which covers the key points of the text.
    ```{text}```
    BULLET POINT SUMMARY:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
    summary_chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt = map_prompt_template, combine_prompt = combine_prompt_template)
    print(summary_chain.run(docs))