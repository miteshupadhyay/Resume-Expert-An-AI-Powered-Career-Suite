import streamlit as st
import os
import json
import re
import tempfile

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage

# -----------------------------
# 🔑 SET API KEY
# -----------------------------
OPENAI_API_KEY = "sk-"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -----------------------------
# 🤖 INIT MODEL
# -----------------------------
chat = ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY
)

# -----------------------------
# 🧹 CLEAN JSON RESPONSE
# -----------------------------
def clean_json_response(response_text):
    cleaned = re.sub(r"```json\s*", "", response_text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()

# -----------------------------
# 📊 RESUME EVALUATION FUNCTION
# -----------------------------
def evaluate_resume(context, question):
    messages = [
        SystemMessage(content="""
You are an expert AI Resume Evaluator acting as a senior technical recruiter and ATS system.

CRITICAL RULES:
- NEVER ask for the resume again
- ALWAYS use provided resume
- Return ONLY valid JSON
- Do NOT wrap response in ```json``` or markdown
- Do NOT hallucinate
- overall_score = weighted average
"""),

        HumanMessage(content=f"""
RESUME CONTENT:
{context[:6000]}

USER REQUEST:
{question}

EVALUATION CRITERIA:
1. Content Quality
2. Skills Relevance
3. Experience Quality
4. Projects
5. Structure
6. ATS Optimization

OUTPUT FORMAT:

{{
  "overall_score": <number>,
  "category_scores": {{
    "content_quality": <number>,
    "skills_relevance": <number>,
    "experience_quality": <number>,
    "projects": <number>,
    "structure_formatting": <number>,
    "ats_optimization": <number>
  }},
  "strengths": [],
  "weaknesses": [],
  "skills_detected": [],
  "missing_or_recommended_skills": [],
  "improvement_suggestions": []
}}
""")
    ]

    response = chat.invoke(messages)
    return response.content

# -----------------------------
# 📄 STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="AI Resume Evaluator", layout="wide")

st.title("📄 AI Resume Evaluator")
st.write("Upload your resume and get ATS-style evaluation instantly 🚀")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    if st.button("🚀 Evaluate Resume"):
        with st.spinner("Analyzing resume... Please wait ⏳"):

            # Load PDF
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            context = "\n\n".join(doc.page_content for doc in documents)

            # Run evaluation
            result = evaluate_resume(
                context=context,
                question="Please evaluate this resume"
            )

            # Clean response
            cleaned_result = clean_json_response(result)

            # Parse JSON
            try:
                parsed_result = json.loads(cleaned_result)
            except Exception:
                st.error("⚠️ Failed to parse response. Showing raw output.")
                st.text(cleaned_result)
                st.stop()

            # -----------------------------
            # 📊 DISPLAY RESULTS
            # -----------------------------
            st.subheader("📊 Overall Score")
            st.metric("Score", parsed_result.get("overall_score", "N/A"))

            st.subheader("📈 Category Scores")
            st.json(parsed_result.get("category_scores", {}))

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Strengths")
                for item in parsed_result.get("strengths", []):
                    st.write(f"- {item}")

                st.subheader("🛠 Improvement Suggestions")
                for item in parsed_result.get("improvement_suggestions", []):
                    st.write(f"- {item}")

            with col2:
                st.subheader("⚠️ Weaknesses")
                for item in parsed_result.get("weaknesses", []):
                    st.write(f"- {item}")

                st.subheader("💡 Recommended Skills")
                for item in parsed_result.get("missing_or_recommended_skills", []):
                    st.write(f"- {item}")

            st.subheader("🧠 Skills Detected")
            st.write(", ".join(parsed_result.get("skills_detected", [])))

            # -----------------------------
            # 📥 DOWNLOAD BUTTON
            # -----------------------------
            st.download_button(
                label="📥 Download Evaluation Report",
                data=json.dumps(parsed_result, indent=2),
                file_name="resume_evaluation.json",
                mime="application/json"
            )