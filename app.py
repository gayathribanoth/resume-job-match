import streamlit as st
import pandas as pd
import time
from utils.parser import extract_text
from utils.skills import extract_skills
from utils.matcher import match_jobs

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

# 🌈 CSS UI
st.markdown("""
<style>

/* Background Animation */
body {
    background: linear-gradient(-45deg, #ff6a00, #ee0979, #00c9ff, #92fe9d);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% { background-position: 0% }
    50% { background-position: 100% }
    100% { background-position: 0% }
}

/* Title */
.title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Card */
.card {
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    margin-bottom: 20px;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px rgba(255,255,255,0.6);
}

/* Skill Tags */
.tag {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    margin: 4px;
    font-size: 14px;
    color: white;
    font-weight: bold;
}

.tag:nth-child(1) { background: #ff4b2b; }
.tag:nth-child(2) { background: #1fa2ff; }
.tag:nth-child(3) { background: #f7971e; }
.tag:nth-child(4) { background: #00c9ff; }
.tag:nth-child(5) { background: #8e2de2; }
.tag:nth-child(6) { background: #43e97b; }

/* Match Bar */
.bar {
    height: 12px;
    border-radius: 10px;
    background: linear-gradient(90deg, #ff512f, #dd2476, #00c9ff);
    animation: load 1.5s ease-in-out;
}

@keyframes load {
    from { width: 0; }
}

</style>
""", unsafe_allow_html=True)

# 🧠 ATS Score Function
def ats_score(resume_skills, job_skills):
    resume_skills = set(resume_skills)
    job_skills = set(job_skills)
    if len(job_skills) == 0:
        return 0
    return int(len(resume_skills & job_skills) / len(job_skills) * 100)

# 🎯 Title
st.markdown('<p class="title">🚀✨ AI Resume Matcher ✨🚀</p>', unsafe_allow_html=True)

st.write("")

# Sidebar
st.sidebar.title("⚙️ Dashboard")
st.sidebar.info("Upload your resume and get AI-powered job matches instantly")

# Upload
uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)

    # 🤖 Loading animation
    st.write("### 🤖 AI is analyzing your resume...")
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress.progress(i + 1)

    col1, col2 = st.columns(2)

    # 📄 Resume Preview
    with col1:
        st.markdown("### 📄 Resume Preview")
        st.markdown(f'<div class="card">{text[:700]}</div>', unsafe_allow_html=True)

    # 🧠 Skills
    with col2:
        skills = extract_skills(text)
        st.markdown("### 🧠 Skills Detected")

        skill_tags = "".join([f'<span class="tag">{s}</span>' for s in skills])
        st.markdown(f'<div class="card">{skill_tags}</div>', unsafe_allow_html=True)

    # 🎯 Job Matching
    jobs = pd.read_csv("data/jobs.csv")
    results = match_jobs(text, jobs)

    st.markdown("### 🎯 Top Matches")

    for _, row in results.head(5).iterrows():
        st.markdown(f"""
        <div class="card">
            <h3 style="color:#00C9FF">{row['title']}</h3>
            <p><b>Match Score:</b> {row['match_score']:.2f}%</p>
            <div class="bar" style="width:{row['match_score']}%"></div>
        </div>
        """, unsafe_allow_html=True)

    best = results.iloc[0]

    # 🏆 Best Match
    st.markdown(f"""
    <div class="card">
        <h2 style="color:#6C63FF">🏆 Best Match: {best['title']}</h2>
        <p>Match Score: {best['match_score']:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

    # 🧠 ATS Score
    score = ats_score(skills, best['skills'].split(", "))

    st.markdown(f"""
    <div class="card">
        <h3>🧠 ATS Score</h3>
        <div style="background:#333;border-radius:10px;">
            <div style="width:{score}%;background:linear-gradient(90deg,#00c9ff,#ff512f);
            padding:10px;border-radius:10px;color:white;text-align:center;">
            {score}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 📉 Skill Gap
    st.markdown("### 📉 Skill Gap Analysis")

    missing_skills = set(best['skills'].split(", ")) - set(skills)

    if missing_skills:
        missing_tags = "".join([f'<span class="tag">{s}</span>' for s in missing_skills])
        st.markdown(f'<div class="card">❌ Missing: {missing_tags}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card">✅ Perfect Match!</div>', unsafe_allow_html=True)
