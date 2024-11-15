import streamlit as st
from streamlit_chat import message
from backend.core import run_llm

st.set_page_config(
    page_title="Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* Main app background and text colors */
    .stApp {
        background-color: #f7f7f8;
        color: #1a1a1a;
    }
    
    /* Initial welcome message container */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        margin: 2rem auto;
        max-width: 800px;
        text-align: center;
    }
    
    .welcome-title {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #1a1a1a;
    }
    
    /* Chat messages container */
    .messages-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Message styling */
    .stMessage {
        margin: 0.5rem 0 !important;
    }
    
    .stMessage > div {
        padding: 0.5rem 1rem !important;
    }
    
    /* User message styling */
    .stMessage.user [data-testid="StyledMessage"] {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 12px !important;
        max-width: 80% !important;
        margin-left: auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Assistant message styling */
    .stMessage.assistant [data-testid="StyledMessage"] {
        background-color: white !important;
        color: #1a1a1a !important;
        border-radius: 12px !important;
        max-width: 80% !important;
        margin-right: auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f7f7f8;
        border-top: 1px solid #e5e5e5;
        padding: 1rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: transparent !important;
        border: none !important;
        padding: 0.5rem !important;
    }
    
    .stTextInput > div {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        border: none !important;
        transition: background-color 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #333 !important;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Additional spacing for messages to not hide behind input */
    .end-space {
        height: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.is_first_message = True
    st.session_state.message_counter = 0 

def process_message(prompt):
    if not prompt.strip():
        return
        
    with st.spinner("Thinking..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get response from LLM
        response = run_llm(
            query=prompt,
            chat_history=[(msg["role"], msg["content"]) for msg in st.session_state.messages]
        )
        
        # Add assistant response to state
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        st.session_state.is_first_message = False

# Display welcome message if no messages yet
if st.session_state.is_first_message:
    st.markdown(
        """
        <div class="welcome-container">
            <h1 class="welcome-title">How can I help you today?</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display chat messages
message_container = st.container()
with message_container:
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.messages):
        message(
            msg["content"],
            is_user=(msg["role"] == "user"),
            key=f"msg_{i}"  # Use string-based key instead of hash
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add space at bottom to prevent input covering messages
    st.markdown('<div class="end-space"></div>', unsafe_allow_html=True)

# Input area
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    
    # Create columns for input and button
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            key="input",
            label_visibility="collapsed",
            placeholder="Type your message here...",
            on_change=lambda: process_message(st.session_state.input) if st.session_state.input else None
        )
        
    with col2:
        submit = st.button("Send", use_container_width=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# Handle message submission
if submit and user_input:
    process_message(user_input)
    # Force a rerun to clear the input
    st.rerun()