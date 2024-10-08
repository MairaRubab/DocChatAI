from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
import uuid  
import os

class ChunkVectorStore:

  def __init__(self) -> None:
     pass

  def split_into_chunks(self, file_path: str):
    doc = PyPDFLoader(file_path).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
    chunks = text_splitter.split_documents(doc)

    for chunk in chunks: 
      if 'metadata' not in chunk:  
                chunk.metadata = {}
      chunk.metadata['id'] = str(uuid.uuid4())  
      print(f"Chunk ID assigned: {chunk.metadata['id']}") 
    chunks = filter_complex_metadata(chunks)

    return chunks
  
  def store_to_vector_database(self, chunks):
    vector_store = chroma.Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY"))
    )

    chunk_ids = [chunk.metadata['id'] for chunk in chunks] 
    return vector_store, chunk_ids  
  
  def delete_chunks(self, chunk_ids: list):
    self.vector_store.delete(ids=chunk_ids)  

