import streamlit as st
import os
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
# 📄 COVER LETTER FUNCTION
# -----------------------------
def generate_cover_letter(context, job_description):
    messages = [
        SystemMessage(content="""
You are an expert recruiter and professional career assistant specializing in writing high-quality, tailored cover letters.

CRITICAL RULES:
- ALWAYS use the provided resume and job description
- NEVER ask for additional information
- Do NOT hallucinate
- Do NOT use placeholders like [Your Name] or [Company Name]
- Return ONLY the cover letter text
- Do NOT return JSON or explanations
"""),

        HumanMessage(content=f"""
RESUME CONTENT:
{context[:6000]}

JOB DESCRIPTION:
{job_description}

TASK:
Generate a highly personalized and professional cover letter.

INSTRUCTIONS:
- Tailor the cover letter specifically to the job description
- Highlight relevant skills, experience, and achievements from the resume
- Emphasize measurable impact and business value
- Do NOT repeat the resume word-for-word
- Use a professional, confident, and natural tone
- Keep the length between 300–400 words

STRUCTURE:
1. Strong introduction
2. Alignment with job requirements
3. Key achievements and impact
4. Why the candidate is a strong fit
5. Confident closing

OUTPUT:
Return ONLY the cover letter text.
Do NOT include headings, JSON, or formatting.
""")
    ]

    response = chat.invoke(messages)
    return response.content


# -----------------------------
# 🎨 STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="AI Cover Letter Generator", layout="wide")

st.title("✉️ AI Cover Letter Generator")
st.write("Upload your resume and paste a job description to generate a tailored cover letter 🚀")

# Upload Resume
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

# Job Description Input
job_description = st.text_area("🧾 Paste Job Description", height=250)

# Generate Button
if st.button("🚀 Generate Cover Letter"):

    if not uploaded_file:
        st.warning("⚠️ Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.warning("⚠️ Please enter a job description.")
        st.stop()

    with st.spinner("Generating cover letter... ⏳"):

        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        # Load PDF
        loader = PyPDFLoader(temp_path)
        documents = loader.load()
        context = "\n\n".join(doc.page_content for doc in documents)

        # Generate cover letter
        cover_letter = generate_cover_letter(context, job_description)

        # -----------------------------
        # 📄 DISPLAY OUTPUT
        # -----------------------------
        st.subheader("📄 Generated Cover Letter")
        st.write(cover_letter)

        # -----------------------------
        # 📥 DOWNLOAD OPTION
        # -----------------------------
        st.download_button(
            label="📥 Download Cover Letter",
            data=cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )