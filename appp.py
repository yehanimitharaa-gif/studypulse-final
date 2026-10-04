import pdfplumber
from groq import Groq
import streamlit as st

# Streamlit Page Config
st.set_page_config(
    page_title="StudyPulse AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional UI Styling (CSS)
st.markdown(
    """
    <style>
    /* Global Page Styling */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* Primary Buttons Styling */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 12px -1px rgba(37, 99, 235, 0.3);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    /* Output Card Boxes */
    .output-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Groq Client Setup
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
  st.error("⚠️ GROQ_API_KEY Missing! Please add it in Streamlit Secrets.")
  st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- SIDEBAR PANEL ---
with st.sidebar:
  st.title("🎓 StudyPulse")
  st.caption("Control Center")
  st.divider()

  uploaded_file = st.file_uploader(
      "📄 Upload Lecture Notes (PDF)", type=["pdf"]
  )

  st.divider()
  st.markdown("### 💡 Instructions")
  st.markdown("1. Upload a PDF document above.")
  st.markdown("2. Choose Summarizer or Q&A tab.")
  st.markdown("3. Click the action button to analyze.")
  st.caption("Powered by Groq Llama-3.1 & Streamlit")

# --- MAIN CONTENT AREA ---
st.markdown(
    '<div class="main-title">📚 StudyPulse AI Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Instantly summarize academic notes and ask'
    ' questions from your PDF documents</div>',
    unsafe_allow_html=True,
)

if uploaded_file is not None:
  text_content = ""
  with pdfplumber.open(uploaded_file) as pdf:
    for page in pdf.pages[:5]:
      extracted = page.extract_text()
      if extracted:
        text_content += extracted + "\n"

  st.success("✅ Document Loaded Successfully!")

  tab1, tab2 = st.tabs(["📝 Key Points Summarizer", "❓ Smart Q&A Assistant"])

  # 1. Summary Tab
  with tab1:
    st.markdown("### 📌 Document Summary")
    if st.button("🚀 Summarize Document"):
      with st.spinner("Generating summary..."):
        try:
          response = client.chat.completions.create(
              messages=[
                  {
                      "role": "system",
                      "content": (
                          "You are an expert academic assistant. Summarize the"
                          " document text clearly with structured bullet"
                          " points and bold headers."
                      ),
                  },
                  {
                      "role": "user",
                      "content": (
                          f"Text:\n{text_content[:3000]}\n\nSummarize key"
                          " points:"
                      ),
                  },
              ],
              model="llama-3.1-8b-instant",
          )
          st.info(response.choices[0].message.content)
        except Exception as e:
          st.error(f"Error: {e}")

  # 2. Q&A Tab
  with tab2:
    st.markdown("### 🔍 Ask Anything About The Document")
    user_question = st.text_input(
        "💬 Enter your question:",
        placeholder="e.g., What are the main objectives?",
    )
    if st.button("💡 Find Answer"):
      if user_question:
        with st.spinner("Finding answer..."):
          try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer strictly based on the provided document"
                            " context."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{text_content[:3000]}\n\nQuestion:"
                            f" {user_question}"
                        ),
                    },
                ],
                model="llama-3.1-8b-instant",
            )
            st.success(response.choices[0].message.content)
          except Exception as e:
            st.error(f"Error: {e}")
else:
  st.info(
      "👈 Please upload a PDF document from the **Left Sidebar** to get started."
  )
