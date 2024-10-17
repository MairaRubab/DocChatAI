import streamlit as st
import tempfile                        
import os
import base64
from fpdf import FPDF
from io import BytesIO
from rag import Rag 


def process_file():
      
    uploaded_files = st.session_state.get("file_uploader", [])
    
    if 'chunk_ids' not in st.session_state:
        st.session_state['chunk_ids'] = [] 

    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete = False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.spinner("Uploading the document..."):    
            chunk_ids = st.session_state["assistant"].feed(file_path)  
            st.session_state['chunk_ids'].extend(chunk_ids)                                                          
            
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

def generate_pdf(conversation_text):
    pdf = FPDF(format='A4')
    pdf.add_page()
    base_dejavu_path = 'resources'
    pdf.add_font('DejaVu', '', os.path.join(base_dejavu_path, 'DejaVuSans.ttf'), uni=True)
    pdf.set_font("DejaVu", size=10)
    pdf.set_left_margin(10)
    max_width = 190
    
    lines = conversation_text.split("\n")
    for line in lines:
        pdf.multi_cell(max_width, 7, txt=line, align='L')
        pdf.set_x(10)
    
    buffer = BytesIO()  
    pdf_output = pdf.output(dest='S').encode('latin1')  
    buffer.write(pdf_output)  
    buffer.seek(0)  
    
    return buffer

def main():

    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 2em;
                margin-top: -27px;
                margin-left: 40px;
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

    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    #logo1 = get_base64_image("C:/Users/maira/OneDrive/Desktop/git_folder/DocChatAI/Maynooth_logo.png")    #For local in Windows
    #logo2 = get_base64_image("C:/Users/maira/OneDrive/Desktop/git_folder/DocChatAI/SFI_logo1.png")
    #logo3 = get_base64_image("C:/Users/maira/OneDrive/Desktop/git_folder/DocChatAI/SFI_logo2.png")
    #logo4 = get_base64_image("C:/Users/maira/OneDrive/Desktop/git_folder/DocChatAI/TCS_logo.png")
    
    
    logo1 = get_base64_image("Maynooth_logo.png")    # for AWS Linux EC2 instance deployment
    logo2 = get_base64_image("SFI_logo1.png")
    logo3 = get_base64_image("SFI_logo2.png")
    logo4 = get_base64_image("TCS_logo.png")

    st.markdown(
        f"""
        <style>
        .footer {{
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 20px 0;
            background-color: white;
            margin-top: 50px;
            left: 14.5%;
        }}
        </style>
        
        <div class="footer">
            <img src="data:image/png;base64,{logo1}" alt="Logo 1" style="height: 35px; margin: 0 2px;">
            <img src="data:image/png;base64,{logo2}" alt="Logo 2" style="height: 40px; margin: 0 2px;">
            <img src="data:image/png;base64,{logo3}" alt="Logo 3" style="height: 60px; margin: 0 2px;">
            <img src="data:image/png;base64,{logo4}" alt="Logo 4" style="height: 45px; margin: 0 2px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    if len(st.session_state) == 0:
        st.session_state.messages = []
        st.session_state["assistant"] = Rag()
    
    st.sidebar.header("Upload the Documents")

    st.sidebar.file_uploader("Upload the Document", type = ["pdf"], 
                     key = "file_uploader", on_change = process_file,
                     label_visibility = "collapsed", accept_multiple_files = True)  

    if not st.session_state.get("file_uploader"):
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 50vh;">
                <div style="display: inline-block; background-color: rgba(255, 230, 140, 0.25); border-radius: 7px; padding: 10px 90px; border: 1px rgba(255, 255, 153, 0.8);">
                    <p style="margin: 0; color: #6c757d;">Please upload the documents to start the conversation!</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    if st.sidebar.button("Reset"):
        st.session_state.messages = []  
        if "chunk_ids" in st.session_state:
            st.session_state["assistant"].clear(st.session_state['chunk_ids'])
            st.session_state['chunk_ids'] = [] 

    display_messages()
    process_input()

    if st.session_state.messages:
        conversation_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" 
                                       for msg in st.session_state.messages])
        
        pdf_data = generate_pdf(conversation_text)
        st.download_button(
            label="📥",
            data=pdf_data,
            file_name="conversation.pdf",
            mime="application/pdf"
        )
    
if __name__ == "__main__":
    main()
