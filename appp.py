else:
    ai_client = genai.Client(api_key=GEMINI_KEY.strip())

    with tab1:
        st.markdown("### 📌 Lecture & Document Summary")

        if st.button("🚀 Summarize Document", key="sum_btn"):
            with st.spinner("Processing document..."):
                try:
                    prompt = (
                        "You are a helpful university study assistant. "
                        "Summarize the key points clearly using bullet points "
                        "and bold core technical terms.\n\n"
                        f"Text:\n{text_content[:8000]}"
                    )

                    res = ai_client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.markdown(
                        f'<div class="output-box">{res.text}</div>',
                        unsafe_allow_html=True,
                    )

                except Exception as e:
                    st.error(f"Error: {e}")

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
                        prompt = (
                            "Answer questions accurately based on the "
                            "provided context.\n\n"
                            f"Context:\n{text_content[:8000]}\n\n"
                            f"Question: {user_q}"
                        )

                        res = ai_client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                        st.markdown(
                            f'<div class="output-box">{res.text}</div>',
                            unsafe_allow_html=True,
                        )

                    except Exception as e:
                        st.error(f"Error: {e}")

            else:
                st.warning("Please enter a question first.")
