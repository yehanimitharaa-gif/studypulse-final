import pdfplumber
from groq import Groq
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="StudyPulse AI | Smart Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Student-Friendly & High-Contrast CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main App Background */
    .stApp {
        background: #f8fafc;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 20px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.3);
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #e0e7ff;
        margin-top: 0.4rem;
        font-weight: 500;
    }

    /* Sidebar Base Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #cbd5e1 !important;
        font-size: 0.92rem;
    }

    /* Upload Box Styling Fix */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #1e293b !important;
        border: 2px dashed #4f46e5 !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        transition: all 0.3s ease-in-out !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
        border-color: #38bdf8 !important;
        background-color: #334155 !important;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.2) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background-color: transparent !important;
        border: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Feature Cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px -5px rgba(79, 70, 229, 0.15);
    }
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
    }
    .feature-title {
        font-weight: 700;
        color: #1e293b;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.4;
    }

    /* Stat Cards */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1rem 1.25rem;
        border-radius: 14px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        text-align: center;
    }
    .stat-val {
        font-size: 1.4rem;
        font-weight: 800;
        color: #4f46e5;
    }
    .stat-lbl {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.95rem;
        border-radius: 12px;
        padding: 0.7rem 1.25rem;
        border: none;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #2563eb 100%);
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.4);
        transform: translateY(-2px);
    }

    /* Output Container */
    .output-box {
        background: #ffffff;
        border-left: 5px solid #4f46e5;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        color: #334155;
        font-size: 0.98rem;
        line-height: 1.7;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Groq API Setup & Model Definition
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
  st.error("⚠️ `GROQ_API_KEY` missing! Add it under Streamlit Secrets.")
  st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ✅ Updated valid Groq model identifier
PRIMARY_MODEL = "llama3-8b-8192"

# 4. Sidebar Panel
with st.sidebar:
  st.markdown("## 📚 Study Hub")
  st.markdown("Upload your lecture slides or notes to get started.")
  st.divider()

  uploaded_file = st.file_uploader(
      "📄 Upload Lecture PDF",
      type=["pdf"],
      help="Supports PDF notes, slides, and past papers.",
  )

  st.divider()
  st.markdown("### 🚀 Quick Steps")
  st.markdown("1. **Upload** your PDF above.")
  st.markdown("2. **Summarize** complex topics fast.")
  st.markdown("3. **Ask questions** for exams & assignments.")

  st.divider()
  st.caption("⚡ Powered by Groq Llama 3 | Built for Students")

# 5. Header Banner
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🎓 StudyPulse AI Assistant</div>
        <div class="hero-subtitle">Your AI study buddy for instant lecture summaries, exam prep, and PDF Q&A</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 6. Main Workspace
if uploaded_file is not None:
  text_content = ""
  page_count = 0

  with pdfplumber.open(uploaded_file) as pdf:
    page_count = len(pdf.pages)
    for page in pdf.pages[:5]:
      extracted = page.extract_text()
      if extracted:
        text_content += extracted + "\n"

  # Metrics
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

  tab1, tab2 = st.tabs([
      "📌 Smart Summarizer & Key Points",
      "💬 Exam & Assignment Assistant",
  ])

  # Tab 1: Summarizer
  with tab1:
    st.markdown("### 📝 Instant Lecture Summary")
    st.caption("Get structured bullet points, key concepts, and exam notes.")

    if st.button("✨ Summarize Document", key="sum_btn"):
      with st.spinner("Analyzing lecture notes..."):
        try:
          response = client.chat.completions.create(
              messages=[
                  {
                      "role": "system",
                      "content": (
                          "You are an expert university study partner. Summarize"
                          " the text into clear bullet points, bold key"
                          " terms, and highlight main exam takeaways."
                      ),
                  },
                  {
                      "role": "user",
                      "content": (
                          f"Text:\n{text_content[:3500]}\n\nProvide key"
                          " study points:"
                      ),
                  },
              ],
              model=PRIMARY_MODEL,
          )
          st.markdown(
              f'<div class="output-box">{response.choices[0].message.content}</div>',
              unsafe_allow_html=True,
          )
        except Exception as e:
          st.error(f"Error: {e}")

  # Tab 2: Q&A
  with tab2:
    st.markdown("### 🔍 Ask Anything About Your PDF")
    st.caption(
        "Type your question below to get answers grounded in your document."
    )

    user_question = st.text_input(
        "Enter question:",
        placeholder="e.g., What are the key formulas/definitions discussed?",
    )

    if st.button("💡 Find Answer", key="qa_btn"):
      if user_question.strip():
        with st.spinner("Searching document notes..."):
          try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer accurately based strictly on the provided"
                            " document context."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{text_content[:3500]}\n\nQuestion:"
                            f" {user_question}"
                        ),
                    },
                ],
                model=PRIMARY_MODEL,
            )
            st.markdown(
                f'<div class="output-box">{response.choices[0].message.content}</div>',
                unsafe_allow_html=True,
            )
          except Exception as e:
            st.error(f"Error: {e}")
      else:
        st.warning("Please type a question first!")

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
