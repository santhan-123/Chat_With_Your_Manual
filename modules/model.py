# modules/model.py

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def create_vector_store(document_chunks):
    """
    Creates a FAISS vector store from document chunks.
    """
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents=document_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    """
    Creates a conversational retrieval chain.
    """
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain
