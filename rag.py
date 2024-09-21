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
          You are an intelligent assistant designed to answer user questions effectively. 
          Use the provided context to answer the question as thoroughly as possible. 
          Pay close attention to every detail to ensure the answer is accurate, clear, and 
          complete. Keep the tone conversational and engaging while ensuring the information 
          comes directly from the context. If the exact answer is unavailable, offer a helpful, 
          closely related response, and politely inform the user. For entirely irrelevant 
          questions, provide correct and useful information based on your broader knowledge, 
          clarifying that the response is not from the context. In the case of comments instead of 
          questions, keep the response short and friendly.

          Question: {question}
          Context: {context}
          Answer: 

          """)
        
        self.model = ChatOpenAI(
        model="gpt-4-turbo",  
        temperature=0,  
        openai_api_key="API") 

    def set_retriever(self):
        self.retriever = self.vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 5, "score_threshold": 0.5,}        
        )

    def augment(self):
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser()
        )

    def ask(self, query: str):
        if not self.chain:
            return "Please upload the documents first to establish the context for the conversation"

        return self.chain.invoke(query)
    
    def feed(self, file_path: str):
        chunks = self.csv_obj.split_into_chunks(file_path)
        self.vector_store = self.csv_obj.store_to_vector_database(chunks)

        self.set_retriever()
        self.augment()

    def clear(self):
        self.vector_store = None                
        self.chain = None
        self.retriever = None


    