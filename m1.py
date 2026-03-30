import streamlit as st 
import docx2txt
import PyPDF2
import re

# ==================================
# CONFIG
# ==================================

st.set_page_config(page_title="SkillGapAI - Milestone 1", layout="wide")


# ==================================
# FUNCTIONS
# ==================================


def clean_text(text: str) -> str:
    """Normalize text by removing extra spaces and line breaks"""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\r", "").replace("\n", " ")
    return text.strip()


def extract_text(uploaded_file):
    """Extract plain text from PDF, DOCX, or TXT with encrypted-file detection"""

    try:
        file_name = uploaded_file.name.lower()

        # ------------------------
        # PDF Handling
        # ------------------------
        if file_name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            # Detect encrypted or locked PDFs
            if pdf_reader.is_encrypted:
                st.error(
                    "🔒 This PDF is encrypted or password-protected. Unable to extract text."
                )
                return ""

            text = ""
            for page in pdf_reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

            return clean_text(text)

        # ------------------------
        # DOCX Handling
        # ------------------------
        elif file_name.endswith(".docx"):
            try:
                text = docx2txt.process(uploaded_file)
                return clean_text(text)
            except:
                st.error(
                    "❌ Unable to read DOCX file. It may be encrypted or corrupted."
                )
                return ""

        # ------------------------
        # TXT Handling
        # ------------------------
        elif file_name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
            return clean_text(text)

        else:
            st.error("❌ Unsupported file format.")
            return ""

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
        return ""


# ==================================
# HEADER
# ==================================
st.markdown(
    """
<h2 style='text-align: center; color:white; background-color:#1E3D59; padding:15px; border-radius:10px'>
🧠 SkillGapAI - Milestone 1: Data Ingestion & Parsing
</h2>
<p>Switch between File Upload and Manual Input for both Resume and Job Description.</p>
""",
    unsafe_allow_html=True,
)

# ==================================
# MAIN UI — SIDE BY SIDE
# ==================================
col_resume, col_jd = st.columns(2)


# ==================================
# REUSABLE INPUT BLOCK
# ==================================
def text_input_block(title, key_prefix):
    st.subheader(title)

    # Toggle between upload & manual typing
    input_mode = st.radio(
        "Choose Input Mode",
        ["Upload File", "Type Manually"],
        key=f"mode_{key_prefix}",
        horizontal=True,
    )

    text_output = ""

    # ------------------------
    # UPLOAD MODE
    # ------------------------
    if input_mode == "Upload File":
        uploaded_file = st.file_uploader(
            f"Upload {title} (PDF / DOCX / TXT)",
            type=["pdf", "docx", "txt"],
            key=f"file_{key_prefix}",
        )

        if uploaded_file:
            with st.spinner("Extracting text..."):
                text_output = extract_text(uploaded_file)

    # ------------------------
    # MANUAL MODE
    # ------------------------
    else:
        manual_text = st.text_area(
            f"Type/Paste {title}",
            "",
            height=200,
            key=f"manual_{key_prefix}",
        )
        if manual_text.strip():
            text_output = clean_text(manual_text)

    # ------------------------
    # OUTPUT PREVIEW
    # ------------------------
    if text_output:
        st.success("Text processed successfully.")
        st.text_area(
            f"Parsed {title}",
            text_output[:4000],
            height=250,
            key=f"preview_{key_prefix}",
        )

        st.caption(
            f"Characters: {len(text_output)} | Words: {len(text_output.split())}"
        )

        st.download_button(
            f"💾 Download Parsed {title}",
            text_output,
            file_name=f"parsed_{key_prefix}.txt",
            mime="text/plain",
        )

    return text_output


# ==================================
# RENDER BOTH SECTIONS
# ==================================
with col_resume:
    resume_text = text_input_block("Resume", "resume")

with col_jd:
    jd_text = text_input_block("Job Description", "jobdesc")


# ==================================
# FOOTER
# ==================================
st.markdown("---")
st.markdown(
    """
<p style='text-align:center; color:gray;'>Milestone 1 • Data Ingestion & Parsing • SkillGapAI • Developed by mani</p>
""",
    unsafe_allow_html=True,
)
