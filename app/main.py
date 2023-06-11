from typing import Union
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from pydantic import BaseModel
import os
from apikey import apikey
os.environ["OPEN_API_KEY"] = apikey
loader = PyPDFLoader('pdf 경로')
index = VectorstoreIndexCreator().from_loaders([loader])

app = FastAPI()

@app.get('/')

class Item(BaseModel):
    query:str

def read_root():
    return 

@app.post('/')
def answer_query(item:Item):
    try:
        response = index.query(item.query)
        return response
    except:
        return {"message" : "Some error happend"}