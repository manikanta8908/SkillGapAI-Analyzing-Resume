# ==========================================
# SkillGapAI - Milestone 2 (Enhanced Version)
# File Upload + Manual Input Toggle + Skill Highlighting
# ==========================================

import streamlit as st
import spacy
import re
import matplotlib.pyplot as plt
from io import BytesIO
from docx import Document
import pdfplumber

# ------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------
st.set_page_config(page_title="SkillGapAI - Milestone 2", layout="wide")

st.markdown(
    """
    <h2 style='color:white; text-align:center; background-color:#117A65; padding:15px; border-radius:10px'>
    🧠 SkillGapAI - Milestone 2: Skill Extraction using NLP
    </h2>
    <p><b>Objective:</b> Extract and classify technical & soft skills separately 
    from both Resume and Job Description using spaCy-based NLP pipelines. 
    Display structured tags, wanted job skills, highlights, and distribution charts.</p>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------
# LOAD SPACY MODEL
# ------------------------------------------
@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except:
        from spacy.cli import download

        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")


nlp = load_model()

# ------------------------------------------
# SKILL LISTS
# ------------------------------------------
technical_skills = [
    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "tensorflow",
    "pytorch",
    "machine learning",
    "data analysis",
    "data visualization",
    "aws",
    "azure",
    "gcp",
    "power bi",
    "tableau",
    "django",
    "flask",
    "scikit-learn",
    "nlp",
]

soft_skills = [
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "time management",
    "adaptability",
    "critical thinking",
    "creativity",
    "collaboration",
    "decision making",
]


# ------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()


def extract_skills(text):
    cleaned = clean_text(text)
    tech = [skill.title() for skill in technical_skills if skill in cleaned]
    soft = [skill.title() for skill in soft_skills if skill in cleaned]
    return list(set(tech)), list(set(soft))


def highlight_skills(text, tech, soft):
    highlighted = text

    for skill in tech:
        highlighted = re.sub(
            rf"(?i)({re.escape(skill)})",
            r"<span style='background-color:#D4E6F1; padding:2px;'><b>\1</b></span>",
            highlighted,
        )

    for skill in soft:
        highlighted = re.sub(
            rf"(?i)({re.escape(skill)})",
            r"<span style='background-color:#F9E79F; padding:2px;'><b>\1</b></span>",
            highlighted,
        )

    return highlighted


def read_file(uploaded_file):
    if uploaded_file is None:
        return ""

    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    elif (
        uploaded_file.type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


# ------------------------------------------
# YOUR INTEGRATED INPUT BLOCK FUNCTION
# ------------------------------------------
def text_input_block(title, key_prefix):
    st.subheader(title)

    mode = st.radio(
        "Choose Input Mode",
        ["Upload File", "Type Manually"],
        key=f"mode_{key_prefix}",
        horizontal=True,
    )

    text_output = ""

    # ---------------------------
    # FILE UPLOAD MODE
    # ---------------------------
    if mode == "Upload File":
        uploaded = st.file_uploader(
            f"Upload {title} (PDF/TXT/DOCX):",
            type=["pdf", "txt", "docx"],
            key=f"file_{key_prefix}",
        )
        text_output = read_file(uploaded)
        return text_output

    # ---------------------------
    # MANUAL TYPING MODE + SUBMIT BUTTON
    # ---------------------------
    with st.form(key=f"form_{key_prefix}"):
        manual_text = st.text_area(
            f"Paste {title} Here:", "", height=220, key=f"text_{key_prefix}"
        )

        submitted = st.form_submit_button("Submit Text")

        if submitted:
            return manual_text

    return ""


# ------------------------------------------
# MAIN LAYOUT (Resume | JD)
# ------------------------------------------
col1, col2 = st.columns(2)

with col1:
    resume_text = text_input_block("👨‍💻 Resume", "resume")

with col2:
    jd_text = text_input_block("🏢 Job Description", "jd")


# ------------------------------------------
# PROCESSING SECTION
# ------------------------------------------
if resume_text or jd_text:
    st.markdown("---")
    st.markdown("## 🔍 Skill Extraction Results")

    # Resume Skills
    if resume_text:
        tech_r, soft_r = extract_skills(resume_text)
        highlighted_r = highlight_skills(resume_text, tech_r, soft_r)

        st.markdown("### 📄 Resume Skills")
        st.write("*Technical Skills:*", ", ".join(tech_r) if tech_r else "None")
        st.write("*Soft Skills:*", ", ".join(soft_r) if soft_r else "None")

        st.markdown("#### ✨ Highlighted Resume Text")
        st.markdown(highlighted_r, unsafe_allow_html=True)

    # Job Description Skills
    if jd_text:
        tech_j, soft_j = extract_skills(jd_text)
        highlighted_j = highlight_skills(jd_text, tech_j, soft_j)

        st.markdown("### 🏢 Job Description Skills")
        st.write(
            "*Required Technical Skills:*", ", ".join(tech_j) if tech_j else "None"
        )
        st.write("*Required Soft Skills:*", ", ".join(soft_j) if soft_j else "None")

        st.markdown("#### ✨ Highlighted JD Text")
        st.markdown(highlighted_j, unsafe_allow_html=True)

else:
    st.info("Please provide Resume and/or Job Description input above.")

# ------------------------------------------
# PROCESS BOTH INPUTS
# ------------------------------------------
if resume_text or jd_text:
    st.markdown("---")
    st.markdown("## 🔍 Skill Extraction Results")

    # Resume extraction
    if resume_text:
        tech_resume, soft_resume = extract_skills(resume_text)
        total_resume = len(tech_resume) + len(soft_resume)

        st.markdown("### 📄 Resume Skill Extraction")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ⚙ Technical Skills (Candidate Possesses)")
            st.write(", ".join(tech_resume) if tech_resume else "None found.")
        with col2:
            st.markdown("#### 💬 Soft Skills (Candidate Possesses)")
            st.write(", ".join(soft_resume) if soft_resume else "None found.")

        # Resume Skill Chart
        fig, ax = plt.subplots(figsize=(3, 3))
        labels = ["Technical", "Soft"]
        sizes = [len(tech_resume), len(soft_resume)]
        colors = ["#1F77B4", "#2ECC71"]
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
        ax.axis("equal")
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)
        st.caption(f"Total Resume Skills: {total_resume}")

    # Job Description extraction (Wanted Skills)
    if jd_text:
        tech_jd, soft_jd = extract_skills(jd_text)
        total_jd = len(tech_jd) + len(soft_jd)

        st.markdown("### 🏢 Wanted Skills for Job Description")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### ⚙ Required Technical Skills (From Job Post)")
            st.write(
                ", ".join(tech_jd) if tech_jd else "No technical skills mentioned."
            )
        with col4:
            st.markdown("#### 💬 Required Soft Skills (From Job Post)")
            st.write(", ".join(soft_jd) if soft_jd else "No soft skills mentioned.")

        # JD Skill Chart
        fig2, ax2 = plt.subplots(figsize=(3, 3))
        labels2 = ["Technical", "Soft"]
        sizes2 = [len(tech_jd), len(soft_jd)]
        colors2 = ["#1F77B4", "#2ECC71"]
        ax2.pie(
            sizes2, labels=labels2, autopct="%1.1f%%", colors=colors2, startangle=90
        )
        ax2.axis("equal")
        buf2 = BytesIO()
        fig2.savefig(buf2, format="png")
        st.image(buf2)
        st.caption(f"Total Required Skills: {total_jd}")

else:
    st.info("Please paste resume and/or job description text to extract skills.")


# ------------------------------------------
# FOOTER
# ------------------------------------------
st.markdown("---")
st.markdown(
    "<p> style='text-align:center; color:gray;'>Milestone 2 • Skill Extraction using NLP • SkillGapAI • Developed by mani</p>",
    unsafe_allow_html=True,
)
