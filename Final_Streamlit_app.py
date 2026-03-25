import streamlit as st
import os
import json
import re
import tempfile

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# -----------------------------
# 🔑 API KEY
# -----------------------------
OPENAI_API_KEY = "sk-"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -----------------------------
# 🤖 MODEL
# -----------------------------
chat = ChatOpenAI(model="gpt-4o", streaming=True)

# -----------------------------
# 🧹 CLEAN JSON
# -----------------------------
def clean_json(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()

# -----------------------------
# 📄 LOAD PDF
# -----------------------------
def load_resume(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    loader = PyPDFLoader(path)
    docs = loader.load()
    return "\n\n".join(d.page_content for d in docs)

# -----------------------------
# 🧠 FUNCTIONS
# -----------------------------
def generate_cover_letter(context, jd):
    messages = [
        SystemMessage(content="You are an expert recruiter. Generate only cover letter."),
        HumanMessage(content=f"RESUME:\n{context[:6000]}\n\nJD:\n{jd}")
    ]
    return chat.invoke(messages).content


def evaluate_resume(context):
    messages = [
        SystemMessage(content="Return ONLY JSON resume evaluation"),
        HumanMessage(content=f"Resume:\n{context[:6000]}")
    ]
    return chat.invoke(messages).content


def score_resume(context, jd):
    messages = [
        SystemMessage(content="Return ONLY JSON ATS scoring"),
        HumanMessage(content=f"Resume:\n{context[:6000]}\nJD:\n{jd}")
    ]
    return chat.invoke(messages).content


# -----------------------------
# 🎨 UI CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("🚀 AI Career Suite")

# -----------------------------
# 🧠 SESSION STATE
# -----------------------------
if "context" not in st.session_state:
    st.session_state.context = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# 📂 SIDEBAR
# -----------------------------
st.sidebar.title("🧭 Navigation")

option = st.sidebar.radio(
    "Choose Feature",
    [
        "💬 Career Coach",
        "📄 Resume Evaluator",
        "📊 Resume Scorer (JD)",
        "✉️ Cover Letter Generator"
    ]
)

uploaded_file = st.sidebar.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file:
    st.session_state.context = load_resume(uploaded_file)

# -----------------------------
# 📄 MAIN SCREEN
# -----------------------------
if not st.session_state.context:
    st.info("👈 Upload your resume from sidebar to begin")
    st.stop()

# =============================
# 💬 1. CAREER COACH
# =============================
if option == "💬 Career Coach":

    st.header("💬 AI Career Coach")

    system_message = SystemMessage(
        content=f"""
        You are a professional career coach.

        Resume:
        {st.session_state.context}
        """
    )

    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)

    user_input = st.chat_input("Ask about your career...")

    if user_input:
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        st.chat_message("user").write(user_input)

        messages = [system_message] + st.session_state.chat_history

        response = ""
        placeholder = st.chat_message("assistant").empty()

        for chunk in chat.stream(messages):
            if chunk.content:
                response += chunk.content
                placeholder.write(response)

        st.session_state.chat_history.append(AIMessage(content=response))


# =============================
# 📄 2. RESUME EVALUATOR
# =============================
elif option == "📄 Resume Evaluator":

    st.header("📄 Resume Evaluation")

    if st.button("🚀 Evaluate"):
        with st.spinner("Analyzing..."):
            result = evaluate_resume(st.session_state.context)
            cleaned = clean_json(result)

            try:
                parsed = json.loads(cleaned)
                st.json(parsed)
            except:
                st.text(cleaned)


# =============================
# 📊 3. RESUME SCORER
# =============================
elif option == "📊 Resume Scorer (JD)":

    st.header("📊 Resume Scorer")

    jd = st.text_area("Paste Job Description")

    if st.button("🚀 Score Resume"):
        if not jd.strip():
            st.warning("Enter job description")
        else:
            with st.spinner("Scoring..."):
                result = score_resume(st.session_state.context, jd)
                cleaned = clean_json(result)

                try:
                    parsed = json.loads(cleaned)
                    st.json(parsed)
                except:
                    st.text(cleaned)


# =============================
# ✉️ 4. COVER LETTER
# =============================
elif option == "✉️ Cover Letter Generator":

    st.header("✉️ Cover Letter Generator")

    jd = st.text_area("Paste Job Description")

    if st.button("🚀 Generate Cover Letter"):
        if not jd.strip():
            st.warning("Enter job description")
        else:
            with st.spinner("Generating..."):
                letter = generate_cover_letter(st.session_state.context, jd)
                st.write(letter)

                st.download_button(
                    "📥 Download",
                    letter,
                    file_name="cover_letter.txt"
                )