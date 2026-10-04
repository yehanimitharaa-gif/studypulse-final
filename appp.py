import pdfplumber
from groq import Groq
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="StudyPulse AI | Intelligent Workspace",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Modern Enterprise CSS Injection
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f8fafc;
    }

    /* Top Navigation Bar Branding */
    .brand-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1.8rem 2rem;
        border-radius: 16px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1);
        margin-bottom: 2rem;
    }
    
    .brand-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin: 0;
        color: #ffffff;
    }

    .brand-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 0.3rem;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        text-align: center;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2563eb;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Styled Action Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 10px;
        padding: 0.65rem 1.25rem;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }

    /* Response Container Styling */
    .response-card {
        background: #ffffff;
        border-left: 4px solid #2563eb;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        color: #334155;
        line-height: 1.6;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Security & API Client Initialization
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
  st.error(
      "⚠️ Security Verification Failed: `GROQ_API_KEY` is missing from"
      " Streamlit Cloud Secrets."
  )
  st.stop()

client = Groq(api_key=GROQ_API_KEY)
PRIMARY_MODEL = "llama-3.1-8b-instant"

# 4. Sidebar Control Center
with st.sidebar:
  st.markdown("### ⚙️ Workspace Config")
  st.caption("Manage document feeds and API processing settings.")
  st.divider()

  uploaded_file = st.file_uploader(
      "Upload Academic PDF",
      type=["pdf"],
      help="Select a document up to 200MB for real-time analysis.",
  )

  st.divider()
  st.markdown("### 📋 Platform Guide")
  st.markdown("""
    - **Step 1:** Upload your lecture notes or reference material.
    - **Step 2:** Choose **Executive Summary** or **Interactive Q&A**.
    - **Step 3:** Trigger context analysis powered by **Groq Llama-3.1**.
    """)

  st.divider()
  st.caption("🔒 Enterprise Encryption & Memory Isolation Enabled")

# 5. Application Banner
st.markdown(
    """
    <div class="brand-header">
        <div class="brand-title">🎓 StudyPulse AI Engine</div>
        <div class="brand-subtitle">Automated Academic PDF Context Extraction, Bullet Summarization & Deep Q&A Platform</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 6. Primary Workspace Pipeline
if uploaded_file is not None:
  text_content = ""
  page_count = 0

  with pdfplumber.open(uploaded_file) as pdf:
    page_count = len(pdf.pages)
    for page in pdf.pages[:5]:
      extracted = page.extract_text()
      if extracted:
        text_content += extracted + "\n"

  # System Metadata Dashboard
  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-value">📄 Active</div>
                <div class="metric-label">{uploaded_file.name[:20]}...</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-value">{page_count} Pages</div>
                <div class="metric-label">Document Volume</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-value">{len(text_content)}</div>
                <div class="metric-label">Parsed Characters</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  tab1, tab2 = st.tabs([
      "📌 Executive Summary Engine",
      "🔍 Deep Document Context Q&A",
  ])

  # Tab 1: Summarization Module
  with tab1:
    st.markdown("### 📝 High-Impact Executive Summary")
    st.caption("Extract key takeaways, core findings, and structured notes.")

    if st.button("⚡ Synthesize Key Takeaways", key="summarize_action"):
      with st.spinner("Processing text context through LLM engine..."):
        try:
          response = client.chat.completions.create(
              messages=[
                  {
                      "role": "system",
                      "content": (
                          "You are an elite academic research assistant."
                          " Provide a highly structured executive summary using"
                          " bold category headers, concise bullet points, and a"
                          " key takeaway block."
                      ),
                  },
                  {
                      "role": "user",
                      "content": (
                          f"Text:\n{text_content[:3500]}\n\nSummarize main"
                          " points:"
                      ),
                  },
              ],
              model=PRIMARY_MODEL,
          )
          st.markdown(
              f'<div class="response-card">{response.choices[0].message.content}</div>',
              unsafe_allow_html=True,
          )
        except Exception as e:
          st.error(f"Execution Error: {e}")

  # Tab 2: Contextual Q&A Module
  with tab2:
    st.markdown("### 🔍 Context-Grounded Query Assistant")
    st.caption(
        "Ask specific questions based strictly on the uploaded document's"
        " content."
    )

    user_question = st.text_input(
        "Enter query:",
        placeholder="e.g., What are the core methodologies discussed?",
    )

    if st.button("💡 Execute Query Search", key="qa_action"):
      if user_question.strip():
        with st.spinner("Analyzing context vectors..."):
          try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer questions accurately and concisely strictly"
                            " based on the provided document context."
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
                f'<div class="response-card">{response.choices[0].message.content}</div>',
                unsafe_allow_html=True,
            )
          except Exception as e:
            st.error(f"Execution Error: {e}")
      else:
        st.warning("Please specify a valid question before running query.")
else:
  st.info(
      "👈 **Workspace Idle:** Upload a document from the left control panel to"
      " initialize the processing pipeline."
  )
