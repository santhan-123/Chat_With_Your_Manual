# app.py

import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv

# Import your custom modules
from modules.database import fetch_users, register_new_user
from modules.file_processor import load_and_split_pdf
from modules.model import create_vector_store, get_conversation_chain

def main():
    """
    Main function to run the Streamlit application.
    This function orchestrates the entire application flow, from user
    authentication to the main chat interface.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Set the page configuration for the Streamlit app
    st.set_page_config(page_title="Chat with your Product Manual", page_icon=":books:")

    # --- USER AUTHENTICATION ---
    
    # Fetch user credentials from the MongoDB database
    credentials = fetch_users()

    # Initialize the authenticator
    authenticator = stauth.Authenticate(
        credentials,
        'rag_app_cookie',      # Name of the cookie stored on the client's browser
        'rag_app_signature_key',# Key to hash the cookie signature
        cookie_expiry_days=30
    )

    # --- LOGIN / REGISTRATION LOGIC ---

    # Create a sidebar selection for Login or Register
    choice = st.sidebar.selectbox("Login/Register", ["Login", "Register"])

    if choice == "Login":
        name, authentication_status, username = authenticator.login('main')

        if authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')
        elif authentication_status:
            # If login is successful, run the main application logic
            run_main_app(name, authenticator)

    elif choice == "Register":
        st.subheader("Create a New Account")
        try:
            # The registration form is rendered here
            if authenticator.register_user('Register user', preauthorization=False):
                # The library temporarily stores the new user's info
                new_user_data = st.session_state['new_user_credentials']
                
                # Call our database function to permanently register the user in MongoDB
                register_new_user(
                    new_user_data['username'],
                    new_user_data['name'],
                    new_user_data['email'],
                    new_user_data['password']
                )
                st.success('User registered successfully! Please go to the Login page to log in.')
        except Exception as e:
            st.error(e)


def run_main_app(name, authenticator):
    """
    This function contains the core logic of the RAG application, which is
    executed only after a user has successfully logged in.
    """
    st.header(f"Welcome, {name}!")
    st.write("Upload your product manual and start asking questions!")

    # --- SESSION STATE INITIALIZATION ---
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    # --- MAIN CHAT INTERFACE ---
    user_question = st.text_input("Ask a question about your document:")
    if user_question:
        handle_user_input(user_question)

    # Display chat history
    st.write("---")
    st.write("### Conversation History")
    for message in reversed(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"<div style='text-align: right; color: #3498db;'><b>You:</b> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; color: #2ecc71;'><b>Bot:</b> {message['content']}</div>", unsafe_allow_html=True)


    # --- SIDEBAR FOR FILE UPLOAD AND LOGOUT ---
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
                    st.success("Processing complete! You can now ask questions.")
            else:
                st.warning("Please upload a PDF document first.")
        
        authenticator.logout('Logout', 'sidebar')


def handle_user_input(user_question):
    """
    Processes the user's question and updates the chat history.
    """
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history.append({'role': 'user', 'content': user_question})
        st.session_state.chat_history.append({'role': 'bot', 'content': response['answer']})
    else:
        st.warning("Please upload and process a document first.")

if __name__ == '__main__':
    main()
