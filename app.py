import streamlit as st
import re
import google.generativeai as genai
from pypdf import PdfReader

# ---------------------------
# GEMINI CONFIGURATION
# ---------------------------
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------
# MEMORY STORAGE
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "summary_history" not in st.session_state:
    st.session_state.summary_history = []

if "mcq_history" not in st.session_state:
    st.session_state.mcq_history = []

if "pdf_history" not in st.session_state:
    st.session_state.pdf_history = []

if "study_plans" not in st.session_state:
    st.session_state.study_plans = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------------------------
# PAGE SETTINGS
# ---------------------------
st.set_page_config(
    page_title="StudyGen AI",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton button {
    border-radius: 12px;
    font-weight: bold;
}

.stTextInput input {
    border-radius: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOGIN SCREEN
# ---------------------------

if not st.session_state.logged_in:

    st.markdown("""
# 📚 StudyGen AI

### 🚀 AI-Powered Learning Platform

#### Learn Smarter • Study Faster • Achieve More

---
""")
    
    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button("Login 🚀"):

        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"

        if not re.match(email_pattern, email):

            st.error(
                "Please enter a valid email address."
            )

        elif len(password) < 6:

            st.error(
                "Password must be at least 6 characters."
            )

        else:

            st.session_state.user_email = email

            st.session_state.logged_in = True

            st.rerun()

    st.stop()

# ---------------------------
# HEADER
# ---------------------------


# ---------------------------
# SIDEBAR
# ---------------------------
feature = st.sidebar.radio(
    "Choose a Feature",
    [

    "Home",
    "Profile",
    "Ask AI",
    "Summarize Notes",
    "Generate MCQs",
    "Flashcards",
    "PDF Summarizer",
    "Study Planner",
    "About"

]
)

st.sidebar.markdown("---")
st.sidebar.markdown("---")
st.sidebar.caption("StudyGen AI v8.0")
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.rerun()
st.sidebar.subheader("📜 History")

st.sidebar.write(
    f"🤖 Questions Asked: {len(st.session_state.chat_history)}"
)

st.sidebar.write(
    f"📄 Summaries Generated: {len(st.session_state.summary_history)}"
)

st.sidebar.write(
    f"📝 MCQ Sets Generated: {len(st.session_state.mcq_history)}"
)

st.sidebar.write(
    f"📄 PDF Summaries: {len(st.session_state.pdf_history)}"
)

st.sidebar.write(
    f"📅 Study Plans: {len(st.session_state.study_plans)}"
)

st.sidebar.write(
    f"🎴 Flashcards: {len(st.session_state.flashcards)}"
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 StudyGen AI")

# ---------------------------
# HOME DASHBOARD
# ---------------------------

if feature == "Home":
    
    st.header("🏠 Dashboard")
    

    st.info(
        "Welcome back! Use AI to study smarter, generate summaries, create flashcards, and plan your exams."
    )

    

    st.write("📚 Your Personal AI Study Assistant")

    st.markdown("---")

    st.subheader("📊 Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🤖 Questions",
            len(st.session_state.chat_history)
        )

        st.metric(
            "📝 MCQs",
            len(st.session_state.mcq_history)
        )

    with col2:
        st.metric(
            "📄 Summaries",
            len(st.session_state.summary_history)
        )

        st.metric(
            "📚 PDFs",
            len(st.session_state.pdf_history)
        )

        st.markdown("---")

    st.subheader("💡 Quick Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🤖 Ask AI")

    with col2:
        st.info("📝 Generate MCQs")

    with col3:
        st.info("📚 Summarize PDFs")

# ---------------------------
# PROFILE
# ---------------------------

elif feature == "Profile":
    
    st.header("👤 User Profile")

    st.info(
    f"Logged in as: {st.session_state.user_email}"
)

    st.success("Welcome to StudyGen AI")

    st.markdown("---")

    st.subheader("📊 Activity Statistics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🤖 Questions",
            len(st.session_state.chat_history)
        )

        st.metric(
            "📝 MCQs",
            len(st.session_state.mcq_history)
        )

        st.metric(
            "🎴 Flashcards",
            len(st.session_state.flashcards)
        )

    with col2:

        st.metric(
            "📄 Summaries",
            len(st.session_state.summary_history)
        )

        st.metric(
            "📚 PDFs",
            len(st.session_state.pdf_history)
        )

        st.metric(
            "📅 Study Plans",
            len(st.session_state.study_plans)
        )

    st.markdown("---")

    st.subheader("🏆 Achievement Level")

    total_activity = (
        len(st.session_state.chat_history)
        + len(st.session_state.summary_history)
        + len(st.session_state.mcq_history)
        + len(st.session_state.flashcards)
        + len(st.session_state.pdf_history)
        + len(st.session_state.study_plans)
    )

    progress = min(total_activity / 20, 1.0)

    st.progress(progress)

    st.write(
        f"Progress: {int(progress * 100)}%"
    )

    if total_activity < 5:
        st.info("🌱 Beginner Learner")

    elif total_activity < 15:
        st.success("📚 Active Learner")

    else:
        st.balloons()
        st.success("🚀 Study Master")

# ---------------------------
# ASK AI
# ---------------------------
elif feature == "Ask AI":

    st.header("🤖 Ask AI")

    question = st.text_area(
        "Enter your question:"
    )

    if st.button("Ask AI 🚀"):

        if question.strip():

            response = model.generate_content(question)

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": response.text
                }
            )

    if st.session_state.chat_history:

        st.subheader("Conversation History")

        for item in reversed(st.session_state.chat_history):

            st.markdown(f"### ❓ {item['question']}")
            st.write(item["answer"])
            st.divider()

# ---------------------------
# SUMMARIZER
# ---------------------------
elif feature == "Summarize Notes":

    st.header("📄 Notes Summarizer")

    notes = st.text_area(
        "Paste your notes:"
    )

    if st.button("Generate Summary"):

        if notes.strip():

            prompt = f"""
            Summarize the following notes
            into easy-to-read bullet points:

            {notes}
            """

            response = model.generate_content(prompt)

            st.session_state.summary_history.append(
                {
                    "notes": notes,
                    "summary": response.text
                }
            )

    if st.session_state.summary_history:

        st.subheader("Generated Summaries")

        for item in reversed(st.session_state.summary_history):

            st.markdown("### 📄 Summary")
            st.write(item["summary"])
            st.download_button(
    label="📥 Download Summary",
    data=item["summary"],
    file_name="summary.txt",
    mime="text/plain",
    key=f"summary_{hash(item['summary'])}"
)
            st.divider()

# ---------------------------
# MCQ GENERATOR
# ---------------------------
elif feature == "Generate MCQs":

    st.header("📝 MCQ Generator")

    topic = st.text_input(
        "Enter a topic:"
    )

    if st.button("Generate MCQs"):

        if topic.strip():

            prompt = f"""
            Generate 5 multiple-choice questions
            with answers on:

            {topic}
            """

            response = model.generate_content(prompt)

            st.session_state.mcq_history.append(
                {
                    "topic": topic,
                    "mcqs": response.text
                }
            )

    if st.session_state.mcq_history:

        st.subheader("Generated MCQs")

        for item in reversed(st.session_state.mcq_history):

            st.markdown(f"### 📝 {item['topic']}")
            st.write(item["mcqs"])
            st.download_button(
    label="📥 Download MCQs",
    data=item["mcqs"],
    file_name="mcqs.txt",
    mime="text/plain",
    key=f"mcq_{hash(item['mcqs'])}"
)
            st.divider()

# ---------------------------
# FLASHCARD GENERATOR
# ---------------------------
elif feature == "Flashcards":

    st.header("🎴 AI Flashcard Generator")

    topic = st.text_input(
        "Enter Topic"
    )

    if st.button("Generate Flashcards"):

        if topic.strip():

            prompt = f"""
            Create 10 flashcards on:

            {topic}

            Format:

            Question:
            Answer:
            """

            with st.spinner("Creating Flashcards..."):

                response = model.generate_content(prompt)

                st.session_state.flashcards.append(
                    {
                        "topic": topic,
                        "content": response.text
                    }
                )

    if st.session_state.flashcards:

        st.subheader("🎴 Flashcard History")

        for item in reversed(
            st.session_state.flashcards
        ):

            st.markdown(
                f"### 📚 {item['topic']}"
            )

            st.write(item["content"])

            st.download_button(
                label="📥 Download Flashcards",
                data=item["content"],
                file_name="flashcards.txt",
                mime="text/plain",
                key=f"flash_{hash(item['content'])}"
            )

            st.divider()



# ---------------------------
# PDF SUMMARIZER
# ---------------------------
elif feature == "PDF Summarizer":
    
    st.header("📄 PDF AI Summarizer")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        pdf = PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        st.success("PDF Loaded Successfully!")

        if st.button("Generate PDF Summary"):

            with st.spinner("AI is reading your PDF..."):

                prompt = f"""
                Summarize the following PDF notes
                into simple bullet points:

                {text[:10000]}
                """

                response = model.generate_content(prompt)

                st.session_state.pdf_history.append(
                    {
                        "file_name": uploaded_file.name,
                        "summary": response.text
                    }
                )

                st.subheader("📋 AI Summary")
                st.write(response.text)

    if st.session_state.pdf_history:

        st.subheader("📚 PDF History")

        for item in reversed(st.session_state.pdf_history):

            st.markdown(f"### 📄 {item['file_name']}")
            st.write(item["summary"])

            st.download_button(
                label="📥 Download PDF Summary",
                data=item["summary"],
                file_name="pdf_summary.txt",
                mime="text/plain",
                key=f"pdf_{hash(item['summary'])}"
            )

            st.divider()

# ---------------------------
# STUDY PLANNER
# ---------------------------
elif feature == "Study Planner":

    st.header("📅 AI Study Planner")

    days = st.number_input(
        "Days Until Exam",
        min_value=1,
        max_value=365,
        value=30
    )

    subjects = st.text_area(
        "Enter Subjects (one per line)",
        placeholder="Math\nPhysics\nChemistry"
    )

    if st.button("Generate Study Plan"):

        if subjects.strip():

            prompt = f"""
            Create a detailed {days}-day study plan.

            Subjects:
            {subjects}

            Make the plan balanced,
            practical and student-friendly.
            """

            with st.spinner("Creating Study Plan..."):

                response = model.generate_content(prompt)

                st.session_state.study_plans.append(
                    response.text
                )

                st.subheader("📋 Your Study Plan")

                st.write(response.text)

    if st.session_state.study_plans:

        st.subheader("📚 Previous Study Plans")

        for i, plan in enumerate(
            reversed(st.session_state.study_plans)
        ):

            st.write(plan)

            st.download_button(
                label=f"📥 Download Plan {i+1}",
                data=plan,
                file_name=f"study_plan_{i+1}.txt",
                mime="text/plain",
                key=f"study_plan_{i}"
            )

            st.divider()


# ---------------------------
# ABOUT
# ---------------------------
elif feature == "About":
    
    st.header("ℹ️ About StudyGen AI")

    st.markdown("""
# 📚 StudyGen AI

### AI-Powered Learning Platform

StudyGen AI is an AI-powered educational platform designed to help students learn more efficiently using Artificial Intelligence.

---

## 🎯 Objectives

- Automate note summarization
- Generate MCQs for revision
- Create flashcards for quick learning
- Summarize PDF study materials
- Build personalized study plans
- Improve student productivity

---

## 🛠 Technologies Used

- Python
- Streamlit
- Google Gemini AI
- PyPDF

---

## ✨ Features

✅ AI Question Answering

✅ Notes Summarizer

✅ MCQ Generator

✅ Flashcard Generator

✅ PDF Summarizer

✅ Study Planner

✅ User Profile

✅ Progress Tracking

✅ Download Options

---

## 🚀 Future Scope

- Google Authentication
- Cloud Deployment
- Multi-user Support
- Database Integration
- Mobile APK Version

---

## 📌 Conclusion

StudyGen AI combines multiple study tools into a single AI-powered platform, helping students learn faster, revise efficiently, and manage their studies more effectively.
""")