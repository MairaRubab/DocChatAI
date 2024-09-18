from chunk_vector_store import ChunkVectorStore as cvs
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI        
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

class Rag:

    vector_store = None
    retriever = None
    chain = None

    def __init__(self) -> None:
        self.csv_obj = cvs()
        self.prompt = PromptTemplate.from_template(
          """
          You are an assistant for question-answering tasks. Use the following pieces of retrieved context
          to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
          maximum and keep the answer concise.
          Question: {question}
          Context: {context}
          Answer: 

          """)
        
        self.model = ChatOpenAI(
        model="gpt-3.5-turbo",  
        temperature=0,  
        openai_api_key="api") 

    def set_retriever(self):
        self.retriever = self.vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.5,}        
        )

    # Augment the context to original prompt.
    def augment(self):
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser()
        )

    # Generate the response.
    def ask(self, query: str):
        if not self.chain:
            print("Upload a document first to set the context of conversation")
        
        return self.chain.invoke(query)
    
    # Stores the file into vector database
    def feed(self, file_path: str):
        chunks = self.csv_obj.split_into_chunks(file_path)
        self.vector_store = self.csv_obj.store_to_vector_database(chunks)

        self.set_retriever()
        self.augment()

    # Used in resetting the conversation when a new document is uploaded 
    def clear(self):
        self.vector_store = None                
        self.chain = None
        self.retriever = None
    
    