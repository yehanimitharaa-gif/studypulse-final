import pdfplumber
from groq import Groq
import streamlit as st

# Streamlit Page Config
st.set_page_config(
    page_title="StudyPulse AI Assistant", page_icon="🎓", layout="wide"
)

# Groq Client Setup
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
  st.error("⚠️ GROQ_API_KEY Missing! Please add it in Streamlit Secrets.")
  st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Custom UI Title
st.title("📚 StudyPulse AI Assistant")
st.caption("Powered by Groq Llama-3 & Streamlit Cloud")

uploaded_file = st.file_uploader(
    "📄 Upload Lecture Notes or Document (PDF)", type=["pdf"]
)

if uploaded_file is not None:
  text_content = ""
  with pdfplumber.open(uploaded_file) as pdf:
    for page in pdf.pages[:5]:
      extracted = page.extract_text()
      if extracted:
        text_content += extracted + "\n"

  st.success("✅ PDF Uploaded Successfully!")

  tab1, tab2 = st.tabs(["📝 Key Points Summarizer", "❓ Smart Q&A Assistant"])

  # 1. Summary Tab
  with tab1:
    st.markdown("### 📌 Lecture & Document Summary")
    if st.button("🚀 Summarize Document"):
      with st.spinner("Generating Summary..."):
        try:
          response = client.chat.completions.create(
              messages=[
                  {
                      "role": "system",
                      "content": (
                          "You are an assistant that summarizes academic"
                          " document text into clear bullet points."
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
              model="llama3-8b-8192",
          )
          st.write(response.choices[0].message.content)
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
                model="llama3-8b-8192",
            )
            st.write(response.choices[0].message.content)
          except Exception as e:
            st.error(f"Error: {e}")