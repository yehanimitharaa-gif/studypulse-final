import pdfplumber
from groq import Groq
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="StudyPulse AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. UI Styling Matching the Sidebar and Cards
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* Sidebar Background & Text Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b1120 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #94a3b8 !important;
        font-size: 0.9rem;
    }

    /* Custom File Uploader Styling */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #172033 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
        border: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    /* Gradient Banner Header */
    .hero-banner {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #06b6d4 100%);
        padding: 2.5rem 2.8rem;
        border-radius: 20px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
        margin-bottom: 2rem;
    }

    .hero-banner h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
    }

    .hero-banner p {
        font-size: 1.05rem;
        color: #e0e7ff;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Feature Cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        height: 100%;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }

    .feature-title {
        font-weight: 700;
        color: #0f172a;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    /* Stat Dashboard Cards */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    }

    .stat-val {
        font-size: 1.25rem;
        font-weight: 800;
        color: #2563eb;
    }

    .stat-lbl {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* Action Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.95rem;
        border-radius: 10px;
        padding: 0.65rem 1.2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }

    .output-box {
        background: #ffffff;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        color: #334155;
        line-height: 1.7;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Secure Key Retrieval & Groq Initialization
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
  st.markdown("## 📚 Study Hub")
  st.markdown("Upload your lecture slides or notes to get started.")
  st.divider()

  if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("🔑 Groq API Key", type="password")

  uploaded_file = st.file_uploader(
      "Upload Lecture PDF",
      type=["pdf"],
      help="Supports PDF notes, slides, and past papers.",
  )

  st.divider()
  st.markdown("### 🚀 Quick Steps")
  st.markdown("1. **Upload** your PDF above.")
  st.markdown("2. **Summarize** complex topics fast.")
  st.markdown("3. **Ask questions** for exams & assignments.")

if not GROQ_API_KEY:
  st.info("👈 Please enter your Groq API key in the sidebar to activate.")
  st.stop()

# Verified active model ID (prevents model_decommissioned 400 & 404 errors)
client = Groq(api_key=str(GROQ_API_KEY).strip())
ACTIVE_MODEL = "llama-3.3-70b-versatile"

# 4. Hero Banner
st.markdown(
    """
    <div class="hero-banner">
        <h1>🎓 StudyPulse AI Assistant</h1>
        <p>Your AI study buddy for instant lecture summaries, exam prep, and PDF Q&A</p>
    </div>
""",
    unsafe_allow_html=True,
)

# 5. Application Logic
if uploaded_file is not None:
  text_content = ""
  page_count = 0

  with pdfplumber.open(uploaded_file) as pdf:
    page_count = len(pdf.pages)
    for page in pdf.pages[:10]:
      extracted = page.extract_text()
      if extracted:
        text_content += extracted + "\n"

  c1, c2, c3 = st.columns(3)
  with c1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-val">📄 {uploaded_file.name[:18]}...</div>
            <div class="stat-lbl">Active Document</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with c2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-val">{page_count} Pages</div>
            <div class="stat-lbl">Total Volume</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with c3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-val">{len(text_content)}</div>
            <div class="stat-lbl">Extracted Characters</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  tab1, tab2 = st.tabs(
      ["📌 Key Points Summarizer", "❓ Smart Q&A Assistant"]
  )

  with tab1:
    st.markdown("### 📌 Lecture & Document Summary")
    if st.button("🚀 Summarize Document", key="sum_btn"):
      with st.spinner("Processing document..."):
        try:
          response = client.chat.completions.create(
              messages=[
                  {
                      "role": "system",
                      "content": (
                          "You are a helpful university study assistant."
                          " Summarize the key points clearly using bullet"
                          " points and bold core technical terms."
                      ),
                  },
                  {
                      "role": "user",
                      "content": (
                          f"Text:\n{text_content[:4000]}\n\nSummary:"
                      ),
                  },
              ],
              model=ACTIVE_MODEL,
          )
          st.markdown(
              f'<div class="output-box">{response.choices[0].message.content}</div>',
              unsafe_allow_html=True,
          )
        except Exception as e:
          st.error(f"API Error: {e}")

  with tab2:
    st.markdown("### ❓ Ask Questions About Your PDF")
    user_q = st.text_input(
        "Question:",
        placeholder="e.g., Explain the core concepts in chapter 1",
    )
    if st.button("💡 Find Answer", key="qa_btn"):
      if user_q.strip():
        with st.spinner("Searching document content..."):
          try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer questions accurately based on the provided"
                            " context."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{text_content[:4000]}\n\nQuestion:"
                            f" {user_q}"
                        ),
                    },
                ],
                model=ACTIVE_MODEL,
            )
            st.markdown(
                f'<div class="output-box">{response.choices[0].message.content}</div>',
                unsafe_allow_html=True,
            )
          except Exception as e:
            st.error(f"API Error: {e}")
      else:
        st.warning("Please enter a question first.")

else:
  # Landing View
  st.markdown("### 🌟 What you can do with StudyPulse:")
  f1, f2, f3 = st.columns(3)

  with f1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📑</div>
            <div class="feature-title">Fast Summaries</div>
            <div class="feature-desc">Convert lengthy lecture slides into quick bullet points before your lectures or exams.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with f2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">❓</div>
            <div class="feature-title">Smart Q&A</div>
            <div class="feature-desc">Ask specific questions and get clear answers based strictly on your uploaded materials.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with f3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎓</div>
            <div class="feature-title">Exam Prep</div>
            <div class="feature-desc">Extract key concepts, definitions, and important takeaways in seconds.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)
  st.info(
      "👈 **Get Started:** Upload a PDF from the **Left Sidebar** to start using"
      " StudyPulse!"
  )
