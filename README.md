# Chat with Your Product Manual - A RAG Application

## Introduction

This project is an intelligent, conversational AI application that allows users to "chat" with their product manuals. Users can create an account, log in, and upload any PDF document. The application then uses a Retrieval-Augmented Generation (RAG) model, powered by OpenAI and LangChain, to answer questions based on the content of that specific document.

This application demonstrates a full-stack approach to building modern AI tools, incorporating a secure database for user management, a sophisticated AI backend for question-answering, and an interactive web interface built with Streamlit.

---

## Features

* **Secure User Authentication:** Users can register for a new account and log in securely. User data is managed in a cloud-hosted MongoDB database.
* **Dynamic PDF Upload:** Users can upload any PDF document to serve as the knowledge base for their session.
* **Conversational Q&A:** Engage in a natural, back-and-forth conversation with the AI about the contents of the uploaded manual.
* **Session-Based Memory:** The application remembers the context of the current conversation, allowing for follow-up questions.
* **Data Isolation:** Each user's session, uploaded documents, and chat history are completely private and isolated from other users.

---

## Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) - For creating the interactive web interface.
* **AI Orchestration:** [LangChain](https://www.langchain.com/) - For building the RAG pipeline, managing prompts, and chaining AI components.
* **Language Model:** [OpenAI](https://openai.com/) - For generating embeddings and conversational responses.
* **Database:** [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - A cloud-hosted NoSQL database for scalable user management.
* **Authentication:** [Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) - A library for adding a secure login/registration system.
* **Vector Store:** [FAISS](https://github.com/facebookresearch/faiss) - For efficient in-memory similarity search of document embeddings.

---

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a file named `.env` in the root directory of the project. This file will store your secret keys.

```
# .env

# Your secret key from the OpenAI platform
OPENAI_API_KEY="sk-..."

# Your full connection string from MongoDB Atlas
MONGO_URI="mongodb+srv://your_user:your_password@your_cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

**Important:** Make sure your `MONGO_URI` is correct and that the password is URL-encoded if it contains special characters.

---

## Usage

Once the setup is complete, you can run the application with a single command:

```bash
streamlit run app.py
```

Your web browser should automatically open to the application's interface. From there, you can:

1.  Navigate to the **Register** page in the sidebar to create a new account.
2.  Go to the **Login** page to sign in with your credentials.
3.  Once logged in, use the sidebar to upload a PDF file and click "Process".
4.  After the document is processed, you can start asking questions in the main chat input box.

---

## Project Structure

```
your_rag_app/
│
├── .env                  # Stores secret API keys and database URI
├── app.py                # The main Streamlit application script
├── requirements.txt      # Lists all project dependencies
│
└── modules/
    ├── __init__.py
    ├── database.py         # Handles all MongoDB connection and user management logic
    ├── file_processor.py   # Responsible for loading and splitting uploaded PDFs
    └── model.py            # Contains the core RAG model and conversation chain logic
```
