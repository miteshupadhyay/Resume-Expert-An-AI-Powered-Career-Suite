import streamlit as st
import os
import json
import re
import tempfile

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage

# -----------------------------
# 🔑 API KEY
# -----------------------------
OPENAI_API_KEY = "sk-"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -----------------------------
# 🤖 MODEL
# -----------------------------
chat = ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY
)

# -----------------------------
# 🧹 CLEAN JSON
# -----------------------------
def clean_json_response(response_text):
    cleaned = re.sub(r"```json\s*", "", response_text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()

# -----------------------------
# 📊 SCORING FUNCTION
# -----------------------------
def score_resume_against_jd(context, job_description):
    messages = [
        SystemMessage(content="""
You are an expert AI Resume Scorer acting as a senior technical recruiter, ATS system, and hiring manager.

CRITICAL RULES:
- ALWAYS use the provided resume and job description
- NEVER ask for additional input
- Do NOT hallucinate
- Return STRICT JSON only
- Do NOT wrap output in markdown
- Scores must be realistic and consistent
"""),

        HumanMessage(content=f"""
RESUME CONTENT:
{context[:6000]}

JOB DESCRIPTION:
{job_description}

TASK:
Evaluate how well the resume matches the job description and provide ATS-style scoring.

OUTPUT FORMAT:

{{
  "score": <number>,
  "overall_match": <number>,
  "keyword_match": <number>,
  "missing_keywords": [],
  "readability_score": <number>,
  "ats_compatibility_score": <number>,
  "two_line_analysis": "",
  "skills_gap_analysis": [],
  "overall_improvement_analysis": [],
  "industry_specific_feedback": []
}}
""")
    ]

    response = chat.invoke(messages)
    return response.content

# -----------------------------
# 🎨 STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="AI Resume Scorer", layout="wide")

st.title("📊 AI Resume Scorer (JD Based)")
st.write("Upload your resume and paste a job description to get ATS-style scoring 🚀")

# Upload resume
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("🧾 Paste Job Description", height=250)

# Button
if st.button("🚀 Score Resume"):

    if not uploaded_file:
        st.warning("⚠️ Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.warning("⚠️ Please enter a job description.")
        st.stop()

    with st.spinner("Analyzing resume... ⏳"):

        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        # Load PDF
        loader = PyPDFLoader(temp_path)
        documents = loader.load()
        context = "\n\n".join(doc.page_content for doc in documents)

        # Get score
        result = score_resume_against_jd(context, job_description)

        # Clean JSON
        cleaned = clean_json_response(result)

        try:
            parsed = json.loads(cleaned)
        except:
            st.error("⚠️ Failed to parse response")
            st.text(cleaned)
            st.stop()

        # -----------------------------
        # 📊 DISPLAY RESULTS
        # -----------------------------
        st.subheader("📊 Overall Score")
        st.metric("Score", parsed.get("score", "N/A"))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Overall Match", parsed.get("overall_match", "N/A"))
        with col2:
            st.metric("Keyword Match", parsed.get("keyword_match", "N/A"))
        with col3:
            st.metric("ATS Score", parsed.get("ats_compatibility_score", "N/A"))

        st.subheader("🧾 2-Line Analysis")
        st.write(parsed.get("two_line_analysis", ""))

        st.subheader("❌ Missing Keywords")
        st.write(", ".join(parsed.get("missing_keywords", [])))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📉 Skills Gap Analysis")
            for item in parsed.get("skills_gap_analysis", []):
                st.write(f"- {item}")

        with col2:
            st.subheader("🛠 Improvement Suggestions")
            for item in parsed.get("overall_improvement_analysis", []):
                st.write(f"- {item}")

        st.subheader("🏭 Industry Feedback")
        for item in parsed.get("industry_specific_feedback", []):
            st.write(f"- {item}")

        # Download JSON
        st.download_button(
            label="📥 Download Report",
            data=json.dumps(parsed, indent=2),
            file_name="resume_score.json",
            mime="application/json"
        )