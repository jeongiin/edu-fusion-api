# 많은 데이터를 효율적으로 처리하기 위한 방법
# 중간 kmeans 관련 에러가 나서 보류
from langchain.document_loaders import PyPDFLoader
# Loaders
from langchain.schema import Document
# Splitters
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Model
from langchain.chat_models import ChatOpenAI
# Embedding Support
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
# Summarizer we'll use for Map Reduce
from langchain.chains.summarize import load_summarize_chain
# Data Science
import numpy as np
from sklearn.cluster import KMeans
# OpenAI Key
import os
from apikey import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
from langchain.prompts import PromptTemplate

if __name__ == "__main__":
    # Load the book
    loader = PyPDFLoader('/Users/timdalxx/2023_PROJECT/edu-fusion-api/app/data/자료실/[이슈 레포트] 업무활용편_ChatGPT 활용사례 및 활용 팁_최종버전.pdf')
    pages = loader.load()

    # Combine the pages, and replace the tabs with spaces
    text = ""

    for page in pages:
        text += page.page_content
        
    text = text.replace('\t', ' ')
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=10000, chunk_overlap=3000)

    docs = text_splitter.create_documents([text])

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectors = embeddings.embed_documents([x.page_content for x in docs])
    # Assuming 'embeddings' is a list or array of 1536-dimensional embeddings

    # Choose the number of clusters, this can be adjusted based on the book's content.
    # I played around and found ~10 was the best.
    # Usually if you have 10 passages from a book you can tell what it's about
    num_clusters = 3

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    # Find the closest embeddings to the centroids

    # Create an empty list that will hold your closest points
    closest_indices = []

    # Loop through the number of clusters you have
    for i in range(num_clusters):
        
        # Get the list of distances from that particular cluster center
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        
        # Find the list position of the closest one (using argmin to find the smallest distance)
        closest_index = np.argmin(distances)
        
        # Append that position to your closest indices list
        closest_indices.append(closest_index)

    selected_indices = sorted(closest_indices)


    llm3 = ChatOpenAI(temperature=0,
                 openai_api_key=OPENAI_API_KEY,
                 max_tokens=1000,
                 model='gpt-3.5-turbo'
                )
    map_prompt = """
    You will receive educational materials. 
    Your goal is to provide a summary of this material so that students can fully understand what it is about.
    Your response must fully cover the content of the material.

    ```{text}```
    BULLET POINT SUMMARY::
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

    map_chain = load_summarize_chain(llm=llm3,
                             chain_type="map_reduce",
                             prompt=map_prompt_template)
    
    selected_docs = [docs[doc] for doc in selected_indices]

    # Make an empty list to hold your summaries
    summary_list = []

    # Loop through a range of the lenght of your selected docs
    for i, doc in enumerate(selected_docs):
        
        # Go get a summary of the chunk
        chunk_summary = map_chain.run([doc])
        
        # Append that summary to your list
        summary_list.append(chunk_summary)
        
        print (f"Summary #{i} (chunk #{selected_indices[i]}) - Preview: {chunk_summary} \n")

    