# modules/model.py

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def create_vector_store(document_chunks):
    """
    Creates a FAISS vector store from document chunks. This store allows for
    efficient similarity searches to find relevant context for user questions.
    """
    # Initialize the model that will create numerical representations (embeddings) of the text
    embeddings = OpenAIEmbeddings()
    
    # Create the vector store from the document chunks and the embedding model
    vector_store = FAISS.from_documents(documents=document_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    """
    Creates a conversational retrieval chain that connects the language model,
    the vector store, and the conversation memory.
    """
    # Initialize the large language model (e.g., GPT-3.5, GPT-4)
    llm = ChatOpenAI()
    
    # Initialize a memory buffer to store the history of the conversation
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    
    # Create the main chain that will handle the conversation flow
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(), # The retriever fetches relevant documents
        memory=memory
    )
    return conversation_chain
