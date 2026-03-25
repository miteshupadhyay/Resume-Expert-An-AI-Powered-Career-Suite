import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import tempfile

# -------------------------------
# 🔐 API KEY
# -------------------------------
OPENAI_API_KEY = "sk-"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -------------------------------
# 🤖 LLM Setup
# -------------------------------
chat = ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
    streaming=True
)

# -------------------------------
# 🎨 Streamlit Page Config
# -------------------------------
st.set_page_config(layout="wide")
st.title("💼 AI Resume Coach")

# -------------------------------
# 🧠 Session State Init
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "context" not in st.session_state:
    st.session_state.context = ""

# -------------------------------
# 📂 File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    # Load PDF
    loader = PyPDFLoader(temp_path)
    documents = loader.load()
    context = "\n\n".join(doc.page_content for doc in documents)

    st.session_state.context = context

# -------------------------------
# 🧱 Layout: 2 Columns
# -------------------------------
col1, col2 = st.columns(2)

# -------------------------------
# 📄 LEFT: Resume Preview
# -------------------------------
with col1:
    st.subheader("📄 Resume Preview")

    if uploaded_file:
        st.download_button(
            label="Download Resume",
            data=uploaded_file,
            file_name=uploaded_file.name
        )

        st.write("----")
        st.text_area(
            "Extracted Text",
            st.session_state.context,
            height=600
        )
    else:
        st.info("Upload a resume to preview")

# -------------------------------
# 💬 RIGHT: Chatbot
# -------------------------------
with col2:
    st.subheader("💬 AI Career Coach")

    if st.session_state.context:

        # System message with resume
        system_message = SystemMessage(
            content=f"""
            You are a professional career coach and resume mentor.

            You help with:
            - Career Guidance
            - Resume Improvements
            - Interview Preparation
            - Job Search Strategy
            - Skill Gap analysis

            Candidate Resume:
            {st.session_state.context}
            """
        )

        # Display chat history
        for msg in st.session_state.chat_history:
            if isinstance(msg, HumanMessage):
                st.chat_message("user").write(msg.content)
            elif isinstance(msg, AIMessage):
                st.chat_message("assistant").write(msg.content)

        # User input
        user_input = st.chat_input("Ask anything about your resume...")

        if user_input:
            # Add user message
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.chat_message("user").write(user_input)

            # Prepare messages
            messages = [system_message] + st.session_state.chat_history

            # Stream response
            response_text = ""
            response_placeholder = st.chat_message("assistant").empty()

            for chunk in chat.stream(messages):
                if chunk.content:
                    response_text += chunk.content
                    response_placeholder.write(response_text)

            # Save AI response
            st.session_state.chat_history.append(AIMessage(content=response_text))

    else:
        st.info("Upload a resume to start chatting")