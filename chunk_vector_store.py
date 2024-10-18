from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
import uuid  
import os
import math

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
  
  def store_to_vector_database(self, chunks, batch_size=166):
    all_chunk_ids = []

    num_batches = math.ceil(len(chunks) / batch_size)

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = start_idx + batch_size
        batch_chunks = chunks[start_idx:end_idx]

        vector_store = chroma.Chroma.from_documents(
            documents=batch_chunks,
            embedding=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY"))
            )
        batch_chunk_ids = [chunk.metadata['id'] for chunk in batch_chunks]
        all_chunk_ids.extend(batch_chunk_ids) 
    return vector_store, all_chunk_ids
  
  def delete_chunks(self, chunk_ids: list):
    self.vector_store.delete(ids=chunk_ids)  

