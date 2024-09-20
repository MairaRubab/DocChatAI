import streamlit as st
import tempfile
import time                          
import os
from rag import Rag                   

def process_file():
    st.session_state.messages = []
    st.session_state["assistant"].clear()        # Used in resetting the conversation when a new document is uploaded or any of the documents is deleted
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete = False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["feeder_spinner"], st.spinner("Uploading the document"):
            # Implement function to feed this file to vector storage
            st.session_state["assistant"].feed(file_path)                                                             
            
        os.remove(file_path)  # To ensure file is removed after processing

# To display all the messages stored
def display_messages():
    for messages in st.session_state.messages:
        with st.chat_message(messages["role"]):
            st.markdown(messages["content"])

def process_input():
    if prompt := st.chat_input("How can I help?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        response = st.session_state["assistant"].ask(prompt)                           
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
# Main function to run the chatbot application   
def main():
    st.title("Document Based Chatbot")
    if len(st.session_state) == 0:
        st.session_state.messages = []
        st.session_state["assistant"] = Rag()   

    st.file_uploader("Upload the Document", type = ["pdf"], 
                     key = "file_uploader", on_change = process_file,
                     label_visibility = "collapsed", accept_multiple_files = True)
    
    st.session_state["feeder_spinner"] = st.empty()

    display_messages()
    process_input()

# Main call of our application
if __name__ == "__main__":
    main()
