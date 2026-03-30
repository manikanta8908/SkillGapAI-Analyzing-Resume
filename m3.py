# ==============================
# SkillGapAI - Milestone 3
# Skill Gap Analysis & Similarity Matching
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

# ------------------------------
# Title Bar
# ------------------------------
st.markdown("""
<style>
.title-bar {
    background: linear-gradient(90deg, #6a1b9a, #8e24aa);
    padding: 18px;
    border-radius: 12px;
    color: white;
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 10px;
}
.objective {
    color: #444;
    font-size: 14px;
    margin-bottom: 25px;
}
</style>

<div class="title-bar">
    🧠 SkillGapAI - Milestone 3: Skill Gap Analysis & Similarity Matching
</div>
<div class="objective">
    <b>Objective:</b> Compare candidate and job skills using TF-IDF & cosine similarity to find matching skills, missing skills, partially matching skills.
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Input Skills")

candidate_input = st.sidebar.text_area(
    "Enter Candidate Skills (comma-separated)",
    placeholder="Python, SQL, Machine Learning"
)

job_input = st.sidebar.text_area(
    "Enter Job Required Skills (comma-separated)",
    placeholder="Python, SQL, AWS, Statistics"
)

analyze_btn = st.sidebar.button("Analyze Skills")

# ------------------------------
# Initialize Variables (IMPORTANT)
# ------------------------------
matched, partial, missing = [], [], []
overall_match = 0
similarity_matrix = None
candidate_skills, job_skills = [], []
similarity_df = None

# ------------------------------
# Run Analysis
# ------------------------------
if analyze_btn:

    if not candidate_input or not job_input:
        st.error("Please enter both Candidate Skills and Job Required Skills.")

    else:
        candidate_skills = [s.strip() for s in candidate_input.split(",")]
        job_skills = [s.strip() for s in job_input.split(",")]

        all_skills = candidate_skills + job_skills

        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        skill_vectors = vectorizer.fit_transform(all_skills)

        candidate_vectors = skill_vectors[:len(candidate_skills)]
        job_vectors = skill_vectors[len(candidate_skills):]

        similarity_matrix = cosine_similarity(candidate_vectors, job_vectors)

        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=candidate_skills,
            columns=job_skills
        )

        # --------------------------
        # Skill Classification
        # --------------------------
        for job in job_skills:
            max_score = similarity_df[job].max()

            if max_score >= 0.8:
                matched.append(job)
            elif max_score >= 0.5:
                partial.append(job)
            else:
                missing.append(job)

        overall_match = (len(matched) / len(job_skills)) * 100

# ==============================
# SHOW RESULTS ONLY AFTER ANALYSIS
# ==============================
if analyze_btn and similarity_matrix is not None:

# --------------------------
# Overview Cards
# --------------------------
    st.markdown("""
<style>
.overview-card {
    background-color: #0e1117;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.stat {
    text-align: center;
    color: white;
}
.stat h2 { font-size: 26px; margin: 0; }
.stat p { font-size: 13px; color: #b0b0b0; }
.green { color: #4CAF50; }
.yellow { color: #FFC107; }
.red { color: #F44336; }
</style>
""", unsafe_allow_html=True)

st.markdown("### 📊 Skill Match Overview")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='overview-card stat'><p>Matched</p><h2 class='green'>{len(matched)}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='overview-card stat'><p>Partial</p><h2 class='yellow'>{len(partial)}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='overview-card stat'><p>Missing</p><h2 class='red'>{len(missing)}</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='overview-card stat'><p>Overall</p><h2>{overall_match:.1f}%</h2></div>", unsafe_allow_html=True)

# --------------------------
# Visualizations
# --------------------------
st.subheader("Skill Matching Visualizations")

col_left, col_right = st.columns(2)

with col_left:
    fig, ax = plt.subplots()
    cax = ax.imshow(similarity_matrix, cmap="RdYlGn")
    ax.set_xticks(range(len(job_skills)))
    ax.set_yticks(range(len(candidate_skills)))
    ax.set_xticklabels(job_skills, rotation=45, ha="right")
    ax.set_yticklabels(candidate_skills)
    plt.colorbar(cax)
    st.pyplot(fig)

with col_right:
    labels = ["Matched", "Partial", "Missing"]
    sizes = [len(matched), len(partial), len(missing)]

    filtered = [(l, s) for l, s in zip(labels, sizes) if s > 0]
    labels, sizes = zip(*filtered)

    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

# --------------------------
# Missing Skills
# --------------------------
st.subheader("Missing / Low Match Skills")

if missing:
    for skill in missing:
        st.warning(f"❌ {skill}")
else:
    st.success("All required skills are matched!")

# --------------------------
# Detailed Match Table
# --------------------------
st.subheader("Detailed Skill Match Percentage")

job_match_data = [
    {"Job Required Skill": job, "Match Percentage (%)": round(similarity_df[job].max() * 100, 2)}
    for job in job_skills
]

st.dataframe(pd.DataFrame(job_match_data))

# ------------------------------------------
# FOOTER
# ------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Milestone 3 • Skill Gap Analysis & Similarity Matching • SkillGapAI Project • Developed by Mani</p>",
    unsafe_allow_html=True
)