# ============================================
# SkillGapAI - Milestone 4: Dashboard & AI Report
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

st.set_page_config(page_title="SkillGapAI - Dashboard", layout="wide")

# -------------------------------------------
# HEADER
# -------------------------------------------
st.markdown("""
<h2 style='color:white; background-color:#0074D9; padding:12px; border-radius:8px'>
📊 SkillGapAI – Dashboard & AI Recommendations
</h2>
<p>AI-driven skill gap analysis, visualization, and report export</p>
""", unsafe_allow_html=True)

# -------------------------------------------
# Dummy Data (Replace with Milestone 3 output)
# -------------------------------------------
resume_skills = {
    "Python": 92,
    "Machine Learning": 88,
    "TensorFlow": 85,
    "SQL": 65,
    "Statistics": 89,
    "Communication": 70,
    "AWS": 30,
    "Project Management": 40
}

job_requirements = {
    "Python": 95,
    "Machine Learning": 90,
    "TensorFlow": 88,
    "SQL": 75,
    "Statistics": 90,
    "Communication": 85,
    "AWS": 80,
    "Project Management": 75
}

skills_df = pd.DataFrame({
    "Skill": resume_skills.keys(),
    "Resume Score": resume_skills.values(),
    "Job Requirement Score": job_requirements.values()
})

matched = sum(
    1 for s in resume_skills
    if resume_skills[s] >= job_requirements[s] - 10
)
missing = len(resume_skills) - matched
overall_match = int((matched / len(resume_skills)) * 100)

# -------------------------------------------
# METRICS
# -------------------------------------------
st.subheader("📌 Skill Match Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall Match", f"{overall_match}%")
c2.metric("Matched Skills", matched)
c3.metric("Missing Skills", missing)
c4.metric("Total Skills", len(resume_skills))

st.markdown("---")

# -------------------------------------------
# COMPARISON CHARTS 
# -------------------------------------------
st.subheader("📊 Skill Comparison")

left, right = st.columns(2)

# Bar Chart
with left:
    st.markdown("**Resume vs Job Requirements**")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    x = np.arange(len(skills_df))
    width = 0.35

    ax.bar(x - width/2, skills_df["Resume Score"], width, label="Resume")
    ax.bar(x + width/2, skills_df["Job Requirement Score"], width, label="Job")

    ax.set_xticks(x)
    ax.set_xticklabels(skills_df["Skill"], rotation=45, fontsize=8)
    ax.set_ylabel("Score (%)")
    ax.legend(fontsize=8)

    st.pyplot(fig)

# Radar Chart
with right:
    st.markdown("**Role View Comparison**")
    labels = list(resume_skills.keys())[:5]
    resume_vals = [resume_skills[k] for k in labels]
    job_vals = [job_requirements[k] for k in labels]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    resume_vals += resume_vals[:1]
    job_vals += job_vals[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(6, 3.5))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, resume_vals, linewidth=2, label="Resume")
    ax.fill(angles, resume_vals, alpha=0.2)

    ax.plot(angles, job_vals, linewidth=2, label="Job Role")
    ax.fill(angles, job_vals, alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.legend(fontsize=8)

    st.pyplot(fig)

# -------------------------------------------
# AI-BASED RECOMMENDATION ENGINE
# -------------------------------------------
st.markdown("---")
st.subheader("🤖 AI-Based Skill Recommendations")

def generate_ai_recommendations(df):
    results = []
    for _, row in df.iterrows():
        gap = row["Job Requirement Score"] - row["Resume Score"]

        if gap <= 0:
            priority = "Strong"
            action = "Maintain skill level"
        elif gap <= 10:
            priority = "Low Gap"
            action = "Short-term practice"
        elif gap <= 30:
            priority = "High Priority"
            action = "Enroll in structured course"
        else:
            priority = "Critical Gap"
            action = "Start from fundamentals"

        results.append({
            "Skill": row["Skill"],
            "Gap (%)": max(gap, 0),
            "Priority": priority,
            "AI Recommendation": action
        })

    return pd.DataFrame(results)

ai_df = generate_ai_recommendations(skills_df)

st.dataframe(ai_df, use_container_width=True)

# -------------------------------------------
# PERSONALIZED LEARNING PATH
# -------------------------------------------
st.markdown("### 🎯 Personalized Learning Path")

for _, row in ai_df.iterrows():
    if row["Gap (%)"] > 30:
        st.error(f"🔥 {row['Skill']} → {row['AI Recommendation']}")
    elif row["Gap (%)"] > 10:
        st.warning(f"⚡ {row['Skill']} → {row['AI Recommendation']}")
    elif row["Gap (%)"] > 0:
        st.info(f"🧩 {row['Skill']} → Minor improvement suggested")
    else:
        st.success(f"✅ {row['Skill']} → Job ready")

# -------------------------------------------
# AI SKILL GAP SCORE
# -------------------------------------------
avg_gap = ai_df["Gap (%)"].mean()
st.metric("🧠 AI Skill Gap Score", f"{round(avg_gap, 1)}%")

# -------------------------------------------
# CSV DOWNLOAD
# -------------------------------------------
st.download_button(
    "📥 Download Skill Report (CSV)",
    skills_df.to_csv(index=False),
    file_name="skillgap_report.csv",
    mime="text/csv"
)

# -------------------------------------------
# PDF EXPORT WITH AI RECOMMENDATIONS
# -------------------------------------------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.cell(0, 10, "SkillGapAI - AI Skill Gap Report", ln=True, align="C")
    pdf.ln(5)

    pdf.cell(0, 8, f"Overall Match: {overall_match}%", ln=True)
    pdf.cell(0, 8, f"AI Skill Gap Score: {round(avg_gap,1)}%", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, "Skill Analysis & AI Recommendations:", ln=True)

    for _, row in ai_df.iterrows():
        pdf.cell(
            0, 8,
            f"{row['Skill']} | Gap: {row['Gap (%)']}% | {row['AI Recommendation']}",
            ln=True
        )

    return pdf.output(dest="S").encode("latin1")

st.download_button(
    "📄 Download Full Report (PDF)",
    generate_pdf(),
    file_name="skillgap_ai_report.pdf",
    mime="application/pdf"
)

# -------------------------------------------
# FOOTER
# -------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Milestone 4 • AI Dashboard • SkillGapAI • Developed by mani</p>",
    unsafe_allow_html=True
)