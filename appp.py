import google.genai as genai
import pdfplumber
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudyPulse AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. GET GEMINI API KEY
# ============================================================

GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")


# ============================================================
# 3. CUSTOM CSS
# ============================================================

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

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background-color: #0d1322 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #94a3b8 !important;
        font-size: 0.9rem;
    }

    /* ================= FILE UPLOADER ================= */

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #172033 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
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
        width: 100% !important;
    }

    /* ================= HERO ================= */

    .hero-banner {
        background: linear-gradient(
            135deg,
            #3b82f6 0%,
            #2563eb 50%,
            #06b6d4 100%
        );

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

        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .hero-banner p {
        font-size: 1.05rem;
        color: #e0e7ff;
        margin-top: 0.6rem;
        font-weight: 500;
    }

    /* ================= FEATURE CARDS ================= */

    .feature-card {
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 16px;

        padding: 2.2rem 1.5rem;

        text-align: center;

        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);

        height: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-weight: 700;
        color: #0f172a;
        font-size: 1.1rem;
        margin-bottom: 0.6rem;
    }

    .feature-desc {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* ================= STAT CARDS ================= */

    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;

        padding: 1.2rem;

        border-radius: 14px;

        text-align: center;

        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }

    .stat-val {
        font-size: 1.2rem;
        font-weight: 800;
        color: #2563eb;
    }

    .stat-lbl {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;

        text-transform: uppercase;

        margin-top: 0.2rem;
    }

    /* ================= BUTTONS ================= */

    .stButton > button {
        width: 100%;

        background: linear-gradient(
            135deg,
            #2563eb 0%,
            #1d4ed8 100%
        );

        color: #ffffff !important;

        font-weight: 700;

        font-size: 0.95rem;

        border-radius: 10px;

        padding: 0.75rem 1.2rem;

        border: none;

        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }

    /* ================= OUTPUT ================= */

    .output-box {
        background: #ffffff;

        border-left: 5px solid #2563eb;

        border-radius: 12px;

        padding: 1.5rem;

        margin-top: 1rem;

        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);

        color: #334155;

        line-height: 1.7;
    }

    /* ================= INFO ================= */

    .info-callout {
        background-color: #e0f2fe;

        border-radius: 12px;

        padding: 1rem 1.2rem;

        color: #0369a1;

        font-weight: 600;

        font-size: 0.95rem;

        display: flex;

        align-items: center;

        gap: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📚 Study Hub")

    st.markdown(
        "Upload your lecture slides or notes to get started."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Lecture PDF",
        type=["pdf"],
        help="Supports PDF notes, slides, and past papers.",
    )

    st.divider()

    st.markdown("### 🚀 Quick Steps")

    st.markdown(
        """
        1. **Upload** your PDF above.
        2. **Summarize** complex topics fast.
        3. **Ask questions** for exams & assignments.
        """
    )


# ============================================================
# 5. HERO BANNER
# ============================================================

st.markdown(
    """
    <div class="hero-banner">

        <h1>🎓 StudyPulse AI Assistant</h1>

        <p>
            Your AI study buddy for instant lecture summaries,
            exam prep, and PDF Q&A
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 6. MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------------

    text_content = ""
    page_count = 0

    try:

        with pdfplumber.open(uploaded_file) as pdf:

            page_count = len(pdf.pages)

            # Process maximum 20 pages
            for page in pdf.pages[:20]:

                extracted = page.extract_text()

                if extracted:
                    text_content += extracted + "\n"

    except Exception as e:

        st.error(
            f"❌ Could not read the PDF: {str(e)}"
        )

        st.stop()


    # --------------------------------------------------------
    # Check extracted text
    # --------------------------------------------------------

    if not text_content.strip():

        st.warning(
            "⚠️ No readable text was found in this PDF. "
            "If it is a scanned PDF, OCR may be required."
        )


    # ========================================================
    # DASHBOARD STATISTICS
    # ========================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-val">
                    📄 {uploaded_file.name[:18]}
                    {"..." if len(uploaded_file.name) > 18 else ""}
                </div>

                <div class="stat-lbl">
                    Active Document
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with c2:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-val">
                    {page_count} Pages
                </div>

                <div class="stat-lbl">
                    Total Volume
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with c3:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-val">
                    {len(text_content)}
                </div>

                <div class="stat-lbl">
                    Extracted Characters
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2 = st.tabs(
        [
            "📌 Key Points Summarizer",
            "❓ Smart Q&A Assistant",
        ]
    )


    # ========================================================
    # CHECK GEMINI API KEY
    # ========================================================

    if not GEMINI_KEY:

        st.error(
            "❌ Gemini API Key missing! "
            "Please add GEMINI_API_KEY to your Streamlit Cloud Secrets."
        )

    else:

        # ----------------------------------------------------
        # Create Gemini Client
        # ----------------------------------------------------

        try:

            ai_client = genai.Client(
                api_key=GEMINI_KEY.strip()
            )

        except Exception as e:

            st.error(
                f"❌ Could not connect to Gemini: {str(e)}"
            )

            st.stop()


        # ====================================================
        # TAB 1 — SUMMARY
        # ====================================================

        with tab1:

            st.markdown(
                "### 📌 Lecture & Document Summary"
            )


            if st.button(
                "🚀 Summarize Document",
                key="sum_btn",
            ):

                if not text_content.strip():

                    st.warning(
                        "⚠️ There is no readable text to summarize."
                    )

                else:

                    with st.spinner(
                        "🤖 AI is analyzing your document..."
                    ):

                        try:

                            prompt = f"""
You are a helpful university study assistant.

Analyze the following lecture/document content.

Create a clear and easy-to-study summary.

Requirements:

1. Use headings.
2. Use bullet points.
3. Bold important technical terms.
4. Explain difficult concepts simply.
5. Include important definitions.
6. Include important formulas if present.
7. Do not add information that is not supported by the document.
8. Make the summary useful for university exam preparation.

DOCUMENT CONTENT:

{text_content[:12000]}
"""


                            response = ai_client.models.generate_content(

                                # IMPORTANT:
                                # Old gemini-1.5-flash caused your error.
                                model="gemini-2.5-flash",

                                contents=prompt,
                            )


                            if response.text:

                                st.markdown(
                                    '<div class="output-box">',
                                    unsafe_allow_html=True,
                                )

                                st.markdown(
                                    response.text
                                )

                                st.markdown(
                                    "</div>",
                                    unsafe_allow_html=True,
                                )

                            else:

                                st.warning(
                                    "⚠️ Gemini returned an empty response."
                                )


                        except Exception as e:

                            st.error(
                                f"❌ Gemini Error: {str(e)}"
                            )


        # ====================================================
        # TAB 2 — Q&A
        # ====================================================

        with tab2:

            st.markdown(
                "### ❓ Ask Questions About Your PDF"
            )


            user_q = st.text_input(

                "Question:",

                placeholder=(
                    "e.g., Explain the core concepts in chapter 1"
                ),

            )


            if st.button(
                "💡 Find Answer",
                key="qa_btn",
            ):

                if not user_q.strip():

                    st.warning(
                        "⚠️ Please enter a question first."
                    )

                elif not text_content.strip():

                    st.warning(
                        "⚠️ There is no readable text in this PDF."
                    )

                else:

                    with st.spinner(
                        "🔍 Searching your document..."
                    ):

                        try:

                            prompt = f"""
You are a university study assistant.

Answer the student's question using ONLY
the information provided in the document context.

Rules:

1. Give a clear and simple explanation.
2. Use examples from the document when available.
3. Use bullet points when useful.
4. Highlight important technical terms.
5. If the answer is not available in the document,
   clearly say that the information is not found
   in the uploaded document.
6. Do not invent information.

DOCUMENT CONTEXT:

{text_content[:12000]}


STUDENT QUESTION:

{user_q}
"""


                            response = ai_client.models.generate_content(

                                model="gemini-2.5-flash",

                                contents=prompt,
                            )


                            if response.text:

                                st.markdown(
                                    '<div class="output-box">',
                                    unsafe_allow_html=True,
                                )

                                st.markdown(
                                    response.text
                                )

                                st.markdown(
                                    "</div>",
                                    unsafe_allow_html=True,
                                )

                            else:

                                st.warning(
                                    "⚠️ Gemini returned an empty response."
                                )


                        except Exception as e:

                            st.error(
                                f"❌ Gemini Error: {str(e)}"
                            )


# ============================================================
# 7. HOME PAGE — WHEN NO PDF IS UPLOADED
# ============================================================

else:

    st.markdown(
        "### ☀️ What you can do with StudyPulse:"
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )


    f1, f2, f3 = st.columns(3)


    # --------------------------------------------------------
    # CARD 1
    # --------------------------------------------------------

    with f1:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📑
                </div>

                <div class="feature-title">
                    Fast Summaries
                </div>

                <div class="feature-desc">
                    Convert lengthy lecture slides into
                    quick bullet points before your
                    lectures or exams.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # CARD 2
    # --------------------------------------------------------

    with f2:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ❓
                </div>

                <div class="feature-title">
                    Smart Q&A
                </div>

                <div class="feature-desc">
                    Ask specific questions and get clear
                    answers based strictly on your
                    uploaded materials.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # CARD 3
    # --------------------------------------------------------

    with f3:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🎓
                </div>

                <div class="feature-title">
                    Exam Prep
                </div>

                <div class="feature-desc">
                    Extract key concepts, definitions,
                    and important takeaways in seconds.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown(
        "<br><br>",
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # INFO MESSAGE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="info-callout">

            👉 <b>Get Started:</b>
            Upload a PDF from the
            <b>Left Sidebar</b>
            to start using StudyPulse!

        </div>
        """,
        unsafe_allow_html=True,
    )
