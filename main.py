from dotenv import load_dotenv

load_dotenv()
from typing import Set
import streamlit as st
from streamlit_chat import message
from backend.core import run_llm
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(
    page_title="Chat",
    page_icon="🥷",
    layout="wide",
    initial_sidebar_state="expanded",
)


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


def get_profile_picture(email):
    gravatar_url = f"https://www.gravatar.com/avatar/{hash(email)}?d=identicon&s=200"
    response = requests.get(gravatar_url)
    img = Image.open(BytesIO(response.content))
    return img


# Enhanced CSS for better alignment and styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: #FFFFFF;
        height: 45px;
        margin-top: 0;
        vertical-align: middle;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: #FFFFFF;
        height: 45px;
        margin-top: 0;
        vertical-align: middle;
    }
    .stSidebar {
        background-color: #252526;
    }
    .stMessage {
        background-color: #2D2D2D;
    }
    /* New styles for input container */
    .input-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
    }
    .input-container > div {
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar user information
with st.sidebar:
    st.title("User Profile")
    user_name = "xx"
    user_email = "xxxxxx"
    profile_pic = get_profile_picture(user_email)
    st.image(profile_pic, width=150)
    st.write(f"**Name:** {user_name}")
    st.write(f"**Email:** {user_email}")

st.header("Chat with me")

# Initialize session state
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Create a container for input elements with custom CSS
st.markdown('<div class="input-container">', unsafe_allow_html=True)
# Adjust column ratio for better alignment
col1, col2 = st.columns([5, 1])

with col1:
    prompt = st.text_input(
        "", placeholder="Enter your message here...", label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("Submit", key="submit", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submit_button:
    prompt = prompt or "Hello"  # Default message if input is empty

if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        sources = set(doc.metadata["source"] for doc in generated_response["context"])
        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["answer"]))

# Display chat history
if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True, key=f"user_{user_query}")
        message(generated_response, key=f"bot_{generated_response}")

# Add a footer
st.markdown("---")
