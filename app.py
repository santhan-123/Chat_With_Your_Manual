# app.py

import streamlit as st
from dotenv import load_dotenv

# Import your custom modules
from modules.file_processor import load_and_split_pdf
from modules.model import create_vector_store, get_conversation_chain

def main():
    """
    Main function to run the Streamlit application.
    """
    load_dotenv()
    st.set_page_config(page_title="Chat with your Product Manual", page_icon=":books:")

    # --- CUSTOM CSS FOR STYLING ---
    st.markdown("""
    <style>
        .st-emotion-cache-1c7y2kd {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- SESSION STATE INITIALIZATION ---
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    # --- UI LAYOUT ---
    st.header("Chat with Your Product Manual 💬")
    st.write("Upload a PDF manual, and I'll answer your questions about it.")

    # --- SIDEBAR FOR FILE UPLOAD AND CHAT CLEAR ---
    with st.sidebar:
        st.subheader("Your Document")
        pdf_doc = st.file_uploader("Upload your PDF manual and click 'Process'", type="pdf")
        
        if st.button("Process"):
            if pdf_doc is not None:
                with st.spinner("Processing document..."):
                    document_chunks = load_and_split_pdf(pdf_doc)
                    vector_store = create_vector_store(document_chunks)
                    st.session_state.vector_store = vector_store
                    st.session_state.conversation = get_conversation_chain(st.session_state.vector_store)
                    # Clear previous chat history when a new document is processed
                    st.session_state.chat_history = []
                    st.success("Processing complete! You can now ask questions.")
            else:
                st.warning("Please upload a PDF document first.")
        
        st.write("---")
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


    # --- MAIN CHAT INTERFACE ---
    # Display existing chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input at the bottom of the page
    if user_question := st.chat_input("Ask a question about your document..."):
        handle_user_input(user_question)


def handle_user_input(user_question):
    """
    Processes the user's question, gets a response from the RAG model,
    and updates the chat history in the session state.
    """
    # Add user question to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    # Display user question in the chat
    with st.chat_message("user"):
        st.markdown(user_question)

    if st.session_state.conversation:
        with st.spinner("Thinking..."):
            # Get the bot's response
            response = st.session_state.conversation({'question': user_question})
            bot_response = response['answer']
            
            # Add bot response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            
            # Display bot response
            with st.chat_message("assistant"):
                st.markdown(bot_response)
    else:
        st.warning("Please upload and process a document first.")
        # Also add the warning to the chat history
        st.session_state.chat_history.append({"role": "assistant", "content": "Please upload and process a document first."})


if __name__ == '__main__':
    main()
