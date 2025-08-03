# Chat with Your PDF - A RAG Application

## Introduction

This project is an intelligent, conversational AI application that allows you to "chat" with your documents. You can upload any PDF, and the application will use a Retrieval-Augmented Generation (RAG) model, powered by OpenAI and LangChain, to answer your questions based on the content of that specific document.

This application demonstrates a streamlined approach to building modern AI tools, focusing on a powerful AI backend for question-answering and an interactive web interface built with Streamlit.

---

## Features

*   **Direct PDF Interaction**: Simply upload any PDF document to serve as the knowledge base for your session.
*   **Conversational Q&A**: Engage in a natural, back-and-forth conversation with the AI about the contents of the uploaded manual.
*   **Session-Based Memory**: The application remembers the context of the current conversation, allowing for follow-up questions.
*   **Simple & Clean Interface**: A straightforward and user-friendly interface built with Streamlit.

---

## Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) - For creating the interactive web interface.
*   **AI Orchestration**: [LangChain](https://www.langchain.com/) - For building the RAG pipeline, managing prompts, and chaining AI components.
*   **Language Model**: [OpenAI](https://openai.com/) - For generating embeddings and conversational responses.
*   **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss) - For efficient in-memory similarity search of document embeddings.

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

Create a file named `.env` in the root directory of the project. This file will store your secret OpenAI API key.

```
# .env

# Your secret key from the OpenAI platform
OPENAI_API_KEY="sk-..."
```

---

## Usage

Once the setup is complete, you can run the application with a single command:

```bash
streamlit run app.py
```

Your web browser should automatically open to the application's interface. From there, you can:

1.  Use the sidebar to upload a PDF file.
2.  Click the "Process" button to have the AI read and understand the document.
3.  Once processing is complete, start asking questions in the main chat input box.

---

## Project Structure

```
your_rag_app/
│
├── .env                  # Stores the secret OpenAI API key
├── app.py                # The main Streamlit application script
├── requirements.txt      # Lists all project dependencies
│
└── modules/
    ├── __init__.py
    ├── file_processor.py   # Responsible for loading and splitting uploaded PDFs
    └── model.py            # Contains the core RAG model and conversation chain logic
```
