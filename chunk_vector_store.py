from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import chroma
from langchain_community.embeddings import fastembed
from langchain_community.document_loaders import PyPDFLoader

class ChunkVectorStore:

  def __init__(self) -> None:
    pass

  def split_into_chunks(self, file_path: str):
    doc = PyPDFLoader(file_path).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
    chunks = text_splitter.split_documents(doc)
    chunks = filter_complex_metadata(chunks)
    print("before",  str(len(chunks)))

    return chunks
  
  
  def store_to_vector_database(self, chunks):
    
    try:
       print("Starting embedding initialization...")  # tried to see where the error was coming
       embeddings = fastembed.FastEmbedEmbeddings()
       print("embeddings", embeddings)
       print(f"The type of _model: {type(embeddings._model)}")
       print(f"The _model object: {embeddings._model}")

       if embeddings._model is None:
          print("Embedding model is not initialized. Please check the model setup.")
       else:
         print("All set! Embedding model is initialized correctly.")
    except Exception as e:
      print(f"An error occurred: {str(e)}")

    
    # Store to vector database
    return chroma.Chroma.from_documents(documents=chunks, embedding=embeddings)

