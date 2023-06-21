
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
from apikey import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

## error : faiss 버전 에러
 
def main():
 
    # upload a PDF file
    pdf = '/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/자료실/[이슈 레포트] 업무활용편_ChatGPT 활용사례 및 활용 팁_최종버전.pdf'
 
    # st.write(pdf)
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
 
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
        chunks = text_splitter.split_text(text=text)
 
        # # embeddings
        store_name = pdf[:-4]
        # st.write(chunks)
 
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            # st.write('Embeddings Loaded from the Disk')s
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
 
        docs = VectorStore.similarity_search(query=query, k=3)
        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        while True:
                user_input = input("Enter a query: ")
                if user_input == "exit":
                    break

                query = f"###Prompt {user_input}"
                try:
                    with get_openai_callback() as cb:
                        response = chain.run(input_documents=docs, question=query)
                        print(response)
                except Exception as err:
                    print('Exception occurred. Please try again', str(err))

                    # 보고서 작성용 참고자료 조사 예시의 모든 절차를 알려줘
 
if __name__ == '__main__':
    main()