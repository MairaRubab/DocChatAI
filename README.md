# DocChatAI: Intelligent Document Assistant for Efficient Information Retrieval


DocChatAI is an advanced streamlit based web application that leverages Retrieval-Augmented Generation (RAG) to deliver intelligent, context-aware responses to user queries based on the content of uploaded PDF documents.

# Features

- **Document Upload:** Users have the option to upload PDF documents which the app will utilize as additional context for generating answers.
- **Chat Interface:** Ask questions and receive contexually relevant & accurate answers, with insights pulled directly from the uploaded PDFs.
- **Download Conversation:** Before resetting the session, users can download a PDF of the conversation, including all interactions and responses generated from the uploaded documents. This feature ensures that users can retain a complete record of the session's context for future reference.
- **Reset Button:** This feature clears the chat history and removes all uploaded documents from backend storage. To start a new session, users will need to re-upload the documents.

# Getting Started
These instructions will walk you through the process of setting up DocChatAI on your local machine for development and testing.

# Prerequisites, Installations & Usage
1. Set up project directory
2. Install python 3.8 or higher (Used 3.10.9)
3. Clone the repository:
   git clone https://github.com/yourusername/DocChatAI.git
4. Navigate to the project directory:
   cd DocChatAI
5. Install necessary dependencies:
   pip install -r requirements.txt
6. Create a virtual environment to isolate dependencies for your project. For Windows:
   python -m venv venv
   .\venv\Scripts\activate
7. Create a config.toml file to configure global settings for Streamlit app, including parameters such as the application theme, server port, and other essential options.
8. Run the Streamlit app
   streamlit run app.py

