# 🚀 AI Resume Intelligence Suite

> Transform your resume into a powerful career asset using AI 🤖
> Built with ❤️ using **Streamlit + LangChain + OpenAI**

---

## 🌟 Overview

The **AI Resume Intelligence Suite** is an all-in-one application designed to help candidates **analyze, improve, and optimize** their resumes for better job opportunities.

This app combines multiple powerful AI-driven tools into a single intuitive interface:

✨ Career Coaching Chatbot
📄 Resume Evaluation (ATS-style)
📊 Resume vs Job Description Scoring
✉️ Cover Letter Generator

---

## 🧠 Key Features

### 💬 AI Career Coach

* Interactive chatbot trained on your resume
* Get personalized:

  * Career guidance
  * Interview prep
  * Skill gap analysis
  * Job strategy

---

### 📄 Resume Evaluator (ATS-Based)

* Deep analysis of your resume
* Provides:

  * Overall score
  * Category-wise breakdown
  * Strengths & weaknesses
  * Improvement suggestions

---

### 📊 Resume Scorer (Job Description Matching)

* Compare resume with job description
* Get:

  * ATS compatibility score
  * Keyword match insights
  * Missing skills
  * Industry feedback

---

### ✉️ Cover Letter Generator

* Generate tailored cover letters instantly
* Based on:

  * Your resume
  * Job description
* Ready to download 📥

---

## 🎯 UI Experience

🧭 **Sidebar Navigation**

* Select any feature instantly

📂 **Single Resume Upload**

* Upload once → used across all tools

⚡ **Real-time AI Responses**

* Streaming chatbot responses (ChatGPT-like)

🎨 **Clean & Professional Layout**

* Designed for usability and clarity

---

## 🏗️ Architecture

```
Resume (PDF)
     ↓
Text Extraction (PyPDFLoader)
     ↓
LLM (OpenAI GPT-4o)
     ↓
Multiple AI Services:
   ├── Chatbot
   ├── Evaluation Engine
   ├── Scoring Engine
   └── Cover Letter Generator
```

---

## 🛠️ Tech Stack

| Layer     | Technology    |
| --------- | ------------- |
| UI        | Streamlit     |
| LLM       | OpenAI GPT-4o |
| Framework | LangChain     |
| Parsing   | PyPDFLoader   |
| Language  | Python        |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/ai-resume-suite.git
cd ai-resume-suite
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Set API Key

```bash
export OPENAI_API_KEY="your-api-key"
```

Or inside code:

```python
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

---

### 4️⃣ Run the App

```bash
streamlit run Final_Streamlit_app.py
```

---

## 🧪 Example Use Cases

💼 Job seekers optimizing resumes
🎓 Students preparing for placements
👨‍💻 Professionals switching careers
🏢 Recruiters analyzing candidate profiles

---

## 🔥 Future Enhancements

* 🔍 RAG-based resume intelligence (vector DB)
* 🤖 Multi-agent architecture
* 📊 Resume analytics dashboard
* 🧾 Multi-resume comparison
* 🎯 Job recommendation engine

---

## ⚠️ Important Notes

* Ensure your resume is in **PDF format**
* Avoid extremely large files (>10MB)
* API usage may incur costs (OpenAI)

---

## 🤝 Contributing

Contributions are welcome! 🎉

1. Fork the repo
2. Create a feature branch
3. Submit a PR

---

## 📜 License

This project is licensed under the **MIT License**

---

## 💡 Author

**Mitesh Upadhyay**
AI Engineer | GenAI Architect | Builder 🚀

---

## ⭐ Support

If you like this project:

👉 Give it a ⭐ on GitHub
👉 Share with your network
👉 Build something awesome with it

---

## 🧠 Final Thought

> "Your resume is not just a document — it's your personal brand.
> Let AI make it exceptional." 🚀

---
# Important, don't forget to create virtual env
py -3.11 -m venv resume

resume\Scripts\activate

pip install -r requirements.txt

