from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings



class ChunkVectorStore:

  def __init__(self) -> None:
    pass

  def split_into_chunks(self, file_path: str):
    doc = PyPDFLoader(file_path).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
    chunks = text_splitter.split_documents(doc)
    chunks = filter_complex_metadata(chunks)

    return chunks
  
  def store_to_vector_database(self, chunks):
    return chroma.Chroma.from_documents(documents=chunks, embedding=OpenAIEmbeddings(
      model="text-embedding-ada-002", api_key="API"))
