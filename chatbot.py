import streamlit as st
import tempfile
import time                          
import os
from rag import Rag                   

def process_file():
      
    uploaded_files = st.session_state.get("file_uploader", [])
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete = False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.spinner("Uploading the document..."):   
            st.session_state["assistant"].feed(file_path)                                                            
            
        os.remove(file_path) 

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
  
def main():

    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 2em;
            }
            .icon {
                vertical-align: middle;
                margin-right: 10px;
            }
        </style>
        <h1 class='title'>
            DocChatAI
            <img class='icon' src='https://img.icons8.com/ios-filled/50/chat.png' alt='Chatbot Icon'/>
        </h1>
    """, unsafe_allow_html=True)

    if len(st.session_state) == 0:
        st.session_state.messages = []
        st.session_state["assistant"] = Rag()
    
    st.sidebar.header("Upload the Documents")

    st.sidebar.file_uploader("Upload the Document", type = ["pdf"], 
                     key = "file_uploader", on_change = process_file,
                     label_visibility = "collapsed", accept_multiple_files = True)  

    if not st.session_state.get("file_uploader"):
        st.warning("Please upload documents to start the conversation!")
        return
    
    if st.sidebar.button("Reset"):
        st.session_state.messages = []  
        st.session_state["assistant"].clear()
    
    display_messages()
    process_input()

    if st.session_state.messages:
        conversation_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" 
                                       for msg in st.session_state.messages])
        st.download_button(
            label="📥",
            data=conversation_text,
            file_name="conversation.txt",
            mime="text/plain"
        )
    
if __name__ == "__main__":
    main()
