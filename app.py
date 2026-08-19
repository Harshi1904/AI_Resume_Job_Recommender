import streamlit as st
import pandas as pd
import re

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: bold;
        margin-top: 25px;
    }

    .improvement-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI Resume Screening System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered resume analysis and job recommendation'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SKILL DATABASE
# =========================================================

skills_list = [

    "python",
    "java",
    "c",
    "c++",
    "sql",

    "html",
    "css",
    "javascript",

    "react",
    "node.js",
    "express",
    "mongodb",
    "mysql",
    "postgresql",

    "git",
    "github",
    "docker",
    "ci/cd",

    "aws",
    "azure",
    "linux",

    "machine learning",
    "deep learning",
    "artificial intelligence",

    "tensorflow",
    "pytorch",
    "scikit-learn",

    "pandas",
    "numpy",

    "power bi",
    "excel",

    "django",
    "flask",
    "spring boot",

    "rest api",

    "testing",
    "selenium",
    "communication",
    "networking",
    "statistics",
    "etl",
    "opencv"
]


# =========================================================
# RESUME SECTION DATABASE
# =========================================================

resume_sections = [

    "career objective",
    "objective",
    "summary",
    "education",
    "academic credentials",
    "technical skills",
    "skills",
    "experience",
    "internships",
    "projects",
    "certifications",
    "achievements"

]


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s+#.-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_resume_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# =========================================================
# LOAD JOB DATA
# =========================================================

@st.cache_data
def load_jobs():

    jobs = pd.read_csv(
        "dataset/jobs.csv"
    )

    jobs["job_text"] = (
        jobs["skills"].fillna("").astype(str)
        + " "
        + jobs["description"].fillna("").astype(str)
    )

    jobs["clean_job_text"] = (
        jobs["job_text"]
        .apply(clean_text)
    )

    return jobs


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "recommended_jobs" not in st.session_state:
    st.session_state.recommended_jobs = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""


# =========================================================
# RESUME UPLOAD
# =========================================================

st.divider()

st.markdown(
    "## 📄 Upload Your Resume"
)

st.write(
    "Upload your resume in PDF format to analyze "
    "your skills, ATS score, and suitable job roles."
)

uploaded_file = st.file_uploader(
    "Choose your Resume PDF",
    type=["pdf"]
)


# =========================================================
# MAIN ANALYSIS
# =========================================================

if uploaded_file is not None:

    st.success(
        "Resume uploaded successfully! ✅"
    )

    if st.button(
        "🔍 Analyze Resume",
        type="primary"
    ):

        with st.spinner(
            "Analyzing your resume..."
        ):

            # =================================================
            # EXTRACT RESUME
            # =================================================

            resume_text = extract_resume_text(
                uploaded_file
            )

            cleaned_resume = clean_text(
                resume_text
            )

            st.session_state.resume_text = (
                cleaned_resume
            )


            # =================================================
            # DETECT SKILLS
            # =================================================

            resume_skills = []

            for skill in skills_list:

                pattern = (
                    r"(?<!\w)"
                    + re.escape(skill)
                    + r"(?!\w)"
                )

                if re.search(
                    pattern,
                    cleaned_resume
                ):

                    resume_skills.append(
                        skill
                    )


            resume_skills = list(
                dict.fromkeys(
                    resume_skills
                )
            )

            st.session_state.resume_skills = (
                resume_skills
            )


            # =================================================
            # LOAD JOBS
            # =================================================

            jobs = load_jobs()


            # =================================================
            # TF-IDF
            # =================================================

            all_text = (
                [cleaned_resume]
                +
                jobs["clean_job_text"].tolist()
            )

            vectorizer = TfidfVectorizer(
                stop_words="english"
            )

            tfidf_matrix = (
                vectorizer.fit_transform(
                    all_text
                )
            )

            resume_vector = (
                tfidf_matrix[0]
            )

            job_vectors = (
                tfidf_matrix[1:]
            )


            # =================================================
            # COSINE SIMILARITY
            # =================================================

            similarity_scores = (
                cosine_similarity(
                    resume_vector,
                    job_vectors
                )[0]
            )


            # =================================================
            # SKILL MATCHING
            # =================================================

            skill_scores = []

            matched_skills_list = []

            missing_skills_list = []


            for index, job in jobs.iterrows():

                job_skills = [

                    skill.strip().lower()

                    for skill in str(
                        job["skills"]
                    ).split(",")

                    if skill.strip()

                ]

                matched = []

                missing = []


                for skill in job_skills:

                    if skill in resume_skills:

                        matched.append(
                            skill
                        )

                    else:

                        missing.append(
                            skill
                        )


                if len(job_skills) > 0:

                    skill_score = (

                        len(matched)
                        /
                        len(job_skills)

                    ) * 100

                else:

                    skill_score = 0


                skill_scores.append(
                    skill_score
                )

                matched_skills_list.append(
                    matched
                )

                missing_skills_list.append(
                    missing
                )


            # =================================================
            # FINAL JOB SCORES
            # =================================================

            jobs["tfidf_score"] = (
                similarity_scores * 100
            )

            jobs["skill_score"] = (
                skill_scores
            )

            jobs["match_score"] = (

                jobs["skill_score"] * 0.60

                +

                jobs["tfidf_score"] * 0.40

            )

            jobs["matched_skills"] = (
                matched_skills_list
            )

            jobs["missing_skills"] = (
                missing_skills_list
            )


            # =================================================
            # SORT JOBS
            # =================================================

            recommended_jobs = (
                jobs.sort_values(
                    by="match_score",
                    ascending=False
                )
                .reset_index(drop=True)
            )

            st.session_state.recommended_jobs = (
                recommended_jobs
            )

            st.session_state.analysis_done = True


            # =================================================
            # BEST JOB
            # =================================================

            best_job = (
                recommended_jobs.iloc[0]
            )

            best_score = (
                best_job["match_score"]
            )


            # =================================================
            # RESUME STRENGTH
            # =================================================

            total_skills = len(
                resume_skills
            )

            resume_strength = min(
                (total_skills / 20) * 100,
                100
            )


            # =================================================
            # ATS SKILLS SCORE
            # =================================================

            ats_skills_score = min(
                (total_skills / 15) * 100,
                100
            )


            # =================================================
            # ATS JOB RELEVANCE
            # =================================================

            ats_relevance_score = (
                best_score
            )


            # =================================================
            # ATS KEYWORD SCORE
            # =================================================

            job_keywords = set(
                clean_text(
                    best_job["job_text"]
                ).split()
            )

            resume_keywords = set(
                cleaned_resume.split()
            )

            common_keywords = (
                job_keywords
                .intersection(
                    resume_keywords
                )
            )


            if len(job_keywords) > 0:

                ats_keyword_score = (

                    len(common_keywords)
                    /
                    len(job_keywords)

                ) * 100

            else:

                ats_keyword_score = 0


            ats_keyword_score = min(
                ats_keyword_score,
                100
            )


            # =================================================
            # ATS CONTENT SCORE
            # =================================================

            detected_sections = 0

            detected_section_names = []

            missing_section_names = []


            for section in resume_sections:

                if section in cleaned_resume:

                    detected_sections += 1

                    detected_section_names.append(
                        section
                    )

                else:

                    missing_section_names.append(
                        section
                    )


            ats_content_score = (

                detected_sections
                /
                len(resume_sections)

            ) * 100


            # =================================================
            # OVERALL ATS SCORE
            # =================================================

            ats_score = (

                ats_skills_score * 0.35

                +

                ats_relevance_score * 0.30

                +

                ats_keyword_score * 0.20

                +

                ats_content_score * 0.15

            )

            ats_score = min(
                ats_score,
                100
            )


            # =================================================
            # STORE RESULTS
            # =================================================

            st.session_state["total_skills"] = (
                total_skills
            )

            st.session_state["resume_strength"] = (
                resume_strength
            )

            st.session_state["ats_skills_score"] = (
                ats_skills_score
            )

            st.session_state["ats_relevance_score"] = (
                ats_relevance_score
            )

            st.session_state["ats_keyword_score"] = (
                ats_keyword_score
            )

            st.session_state["ats_content_score"] = (
                ats_content_score
            )

            st.session_state["ats_score"] = (
                ats_score
            )

            st.session_state["detected_sections"] = (
                detected_section_names
            )

            st.session_state["missing_sections"] = (
                missing_section_names
            )


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.analysis_done:

    resume_skills = (
        st.session_state.resume_skills
    )

    recommended_jobs = (
        st.session_state.recommended_jobs
    )

    total_skills = (
        st.session_state["total_skills"]
    )

    resume_strength = (
        st.session_state["resume_strength"]
    )

    ats_skills_score = (
        st.session_state["ats_skills_score"]
    )

    ats_relevance_score = (
        st.session_state["ats_relevance_score"]
    )

    ats_keyword_score = (
        st.session_state["ats_keyword_score"]
    )

    ats_content_score = (
        st.session_state["ats_content_score"]
    )

    ats_score = (
        st.session_state["ats_score"]
    )

    detected_sections = (
        st.session_state["detected_sections"]
    )

    missing_sections = (
        st.session_state["missing_sections"]
    )

    best_job = (
        recommended_jobs.iloc[0]
    )

    best_score = (
        best_job["match_score"]
    )


    # =========================================================
    # RESUME ANALYSIS
    # =========================================================

    st.markdown(
        "## 📊 Resume Analysis"
    )

    st.write(
        "Here is a quick overview of your resume performance."
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "🎯 Skills Detected",
            total_skills
        )


    with col2:

        st.metric(
            "💼 Jobs Analyzed",
            len(recommended_jobs)
        )


    with col3:

        st.metric(
            "🏆 Best Match",
            f"{best_score:.1f}%"
        )


    with col4:

        st.metric(
            "📋 ATS Score",
            f"{ats_score:.1f}%"
        )


    # =========================================================
    # ATS ANALYSIS
    # =========================================================

    st.header(
        "📋 ATS Resume Analysis"
    )

    st.write(
        "This project calculates an ATS-style score "
        "using skills, job relevance, keywords, "
        "and resume sections."
    )

    st.subheader(
        f"Overall ATS Score: {ats_score:.1f}%"
    )

    st.progress(
        int(ats_score)
    )


    if ats_score >= 80:

        st.success(
            "Excellent ATS compatibility! 🚀"
        )

    elif ats_score >= 60:

        st.info(
            "Good ATS compatibility. "
            "A few improvements can strengthen your resume."
        )

    else:

        st.warning(
            "Your resume could be improved "
            "for better ATS compatibility."
        )


    # =========================================================
    # ATS SCORE BREAKDOWN
    # =========================================================

    st.subheader(
        "📊 ATS Score Breakdown"
    )

    ats_data = pd.DataFrame({

        "Category": [

            "Skills Coverage",
            "Job Relevance",
            "Keyword Match",
            "Resume Content"

        ],

        "Score": [

            ats_skills_score,
            ats_relevance_score,
            ats_keyword_score,
            ats_content_score

        ]

    })


    st.bar_chart(
        ats_data.set_index(
            "Category"
        )
    )


    # =========================================================
    # DETECTED SKILLS
    # =========================================================

    st.header(
        "🎯 Detected Skills"
    )


    if resume_skills:

        skill_text = " • ".join(

            skill.title()

            for skill in resume_skills

        )

        st.success(
            skill_text
        )

    else:

        st.warning(
            "No technical skills detected."
        )


    # =========================================================
    # RESUME STRENGTH
    # =========================================================

    st.header(
        "📈 Resume Strength"
    )

    st.progress(
        int(resume_strength)
    )

    st.write(
        f"Resume technical skill strength: "
        f"**{resume_strength:.0f}%**"
    )


    if resume_strength >= 75:

        st.success(
            "Excellent technical skill coverage! 🚀"
        )

    elif resume_strength >= 50:

        st.info(
            "Good technical skill coverage."
        )

    else:

        st.warning(
            "Consider adding more relevant technical skills."
        )


    # =========================================================
    # TOP JOB
    # =========================================================

    st.header(
        "🏆 Top Job Recommendation"
    )

    st.subheader(
        best_job["job_title"]
    )

    st.progress(
        min(
            int(best_score),
            100
        )
    )

    st.write(
        f"### {best_score:.2f}% Match"
    )


    col1, col2 = (
        st.columns(2)
    )


    with col1:

        st.write(
            "### ✅ Matching Skills"
        )

        if best_job["matched_skills"]:

            for skill in best_job[
                "matched_skills"
            ]:

                st.write(
                    f"• {skill.title()}"
                )

        else:

            st.write(
                "No matching skills"
            )


    with col2:

        st.write(
            "### ❌ Skills to Improve"
        )

        if best_job["missing_skills"]:

            for skill in best_job[
                "missing_skills"
            ]:

                st.write(
                    f"• {skill.title()}"
                )

        else:

            st.success(
                "No missing skills 🎉"
            )


    # =========================================================
    # SKILL GAP ANALYSIS
    # =========================================================

    st.header(
        "🎯 Skill Gap Analysis"
    )

    missing_for_top_job = (
        best_job["missing_skills"]
    )


    if missing_for_top_job:

        st.write(
            "Skills that could improve "
            "your match for the recommended role:"
        )


        for number, skill in enumerate(
            missing_for_top_job,
            start=1
        ):

            st.write(
                f"**{number}. {skill.title()}**"
            )


        st.info(
            "💡 Learning these skills and "
            "adding relevant projects can "
            "improve your job match."
        )

    else:

        st.success(
            "You already have all required skills! 🎉"
        )


    # =========================================================
    # RECOMMENDED SKILLS
    # =========================================================

    st.header(
        "📚 Recommended Skills to Learn"
    )


    if missing_for_top_job:

        learning_data = pd.DataFrame({

            "Priority": range(
                1,
                len(missing_for_top_job) + 1
            ),

            "Skill": [

                skill.title()

                for skill
                in missing_for_top_job

            ]

        })


        st.dataframe(
            learning_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.write(
            "No additional skills recommended."
        )


    # =========================================================
    # JOB RECOMMENDATIONS
    # =========================================================

    st.header(
        "💼 Job Recommendations"
    )


    chart_data = (

        recommended_jobs[
            [
                "job_title",
                "match_score"
            ]
        ]

        .set_index(
            "job_title"
        )

    )


    st.bar_chart(
        chart_data
    )


    # =========================================================
    # DETAILED JOB ANALYSIS
    # =========================================================

    st.header(
        "📋 Detailed Job Analysis"
    )


    for rank, (
        index,
        job
    ) in enumerate(
        recommended_jobs.iterrows(),
        start=1
    ):

        if rank > 10:
            break


        with st.expander(

            f"#{rank} "
            f"{job['job_title']} — "
            f"{job['match_score']:.2f}%"

        ):

            col1, col2 = (
                st.columns(2)
            )


            with col1:

                st.write(
                    "### ✅ Matched Skills"
                )


                if job["matched_skills"]:

                    st.write(
                        ", ".join(
                            job["matched_skills"]
                        )
                    )

                else:

                    st.write(
                        "No matching skills"
                    )


            with col2:

                st.write(
                    "### ❌ Missing Skills"
                )


                if job["missing_skills"]:

                    st.write(
                        ", ".join(
                            job["missing_skills"]
                        )
                    )

                else:

                    st.write(
                        "No missing skills"
                    )


    # =========================================================
    # NEW FEATURE
    # COMPLETE RESUME IMPROVEMENT
    # =========================================================

    st.divider()

    st.header(
        "📝 How to Improve Your Entire Resume"
    )

    st.write(
        "This section analyzes your resume and provides "
        "a practical improvement plan based on your "
        "detected skills, ATS score, resume sections, "
        "and recommended job."
    )


    # =========================================================
    # RESUME IMPROVEMENT SCORE
    # =========================================================

    improvement_score = ats_score


    st.subheader(
        f"🚀 Resume Improvement Readiness: "
        f"{improvement_score:.1f}%"
    )

    st.progress(
        int(improvement_score)
    )


    # =========================================================
    # IMPROVEMENT SUMMARY
    # =========================================================

    if improvement_score >= 80:

        st.success(
            "Your resume is already strong! "
            "Focus on small improvements and "
            "job-specific customization."
        )

    elif improvement_score >= 60:

        st.info(
            "Your resume has a good foundation. "
            "Improving keywords, skills, and content "
            "can make it stronger."
        )

    else:

        st.warning(
            "Your resume needs several improvements "
            "to become more ATS-friendly and "
            "job-relevant."
        )


    # =========================================================
    # IMPROVEMENT CHECKLIST
    # =========================================================

    st.subheader(
        "✅ Resume Improvement Checklist"
    )


    # ---------------------------------------------------------
    # 1. SKILLS
    # ---------------------------------------------------------

    if total_skills >= 15:

        st.success(
            "✅ Skills: Good technical skill coverage."
        )

    else:

        st.warning(
            f"⚠️ Skills: You have {total_skills} "
            "detected skills. Consider adding "
            "more relevant technical skills."
        )


    # ---------------------------------------------------------
    # 2. JOB-SPECIFIC SKILLS
    # ---------------------------------------------------------

    if missing_for_top_job:

        st.warning(
            "⚠️ Job Skills: Add or learn these "
            "skills for your top recommended role: "
            +
            ", ".join(
                skill.title()
                for skill in missing_for_top_job
            )
        )

    else:

        st.success(
            "✅ Job Skills: You already have "
            "the required skills for your top role."
        )


    # ---------------------------------------------------------
    # 3. RESUME SECTIONS
    # ---------------------------------------------------------

    if missing_sections:

        st.warning(
            "⚠️ Resume Sections: Consider adding "
            "these sections: "
            +
            ", ".join(
                section.title()
                for section in missing_sections
            )
        )

    else:

        st.success(
            "✅ Resume Sections: Major resume sections "
            "were detected."
        )


    # ---------------------------------------------------------
    # 4. KEYWORDS
    # ---------------------------------------------------------

    if ats_keyword_score >= 70:

        st.success(
            "✅ Keywords: Good keyword alignment "
            "with your recommended job."
        )

    elif ats_keyword_score >= 40:

        st.info(
            "⚠️ Keywords: Add more keywords from "
            "the target job description naturally "
            "inside your resume."
        )

    else:

        st.warning(
            "❌ Keywords: Your resume has low keyword "
            "alignment with the recommended job. "
            "Use relevant job-specific terminology."
        )


    # ---------------------------------------------------------
    # 5. PROJECTS
    # ---------------------------------------------------------

    if "projects" in cleaned_resume:

        st.success(
            "✅ Projects: A project section was detected."
        )

    else:

        st.warning(
            "⚠️ Projects: Add a Projects section "
            "with 2–3 relevant technical projects."
        )


    # ---------------------------------------------------------
    # 6. EXPERIENCE / INTERNSHIP
    # ---------------------------------------------------------

    if (
        "experience" in cleaned_resume
        or
        "internships" in cleaned_resume
    ):

        st.success(
            "✅ Experience: Experience or internship "
            "content was detected."
        )

    else:

        st.info(
            "💡 Experience: If you have internships, "
            "training, freelance work, or practical "
            "experience, add them to your resume."
        )


    # =========================================================
    # TOP PRIORITIES
    # =========================================================

    st.subheader(
        "🎯 Top Priorities for Your Resume"
    )


    priority_number = 1


    if missing_for_top_job:

        st.write(
            f"**{priority_number}.** Add relevant skills: "
            +
            ", ".join(
                skill.title()
                for skill in missing_for_top_job[:5]
            )
        )

        priority_number += 1


    if missing_sections:

        st.write(
            f"**{priority_number}.** Add missing resume sections: "
            +
            ", ".join(
                section.title()
                for section in missing_sections[:4]
            )
        )

        priority_number += 1


    if ats_keyword_score < 70:

        st.write(
            f"**{priority_number}.** Improve job-specific "
            "keywords based on your target role."
        )

        priority_number += 1


    if total_skills < 15:

        st.write(
            f"**{priority_number}.** Add relevant technical "
            "skills that you genuinely know."
        )

        priority_number += 1


    if "projects" not in cleaned_resume:

        st.write(
            f"**{priority_number}.** Add 2–3 strong technical "
            "projects with technologies and outcomes."
        )

        priority_number += 1


    st.write(
        f"**{priority_number}.** Customize your resume "
        "for each job instead of using exactly the "
        "same resume everywhere."
    )


    # =========================================================
    # RESUME CONTENT TIPS
    # =========================================================

    st.subheader(
        "💡 Resume Writing Tips"
    )


    tips = [

        "Use clear section headings such as Education, Skills, Projects, Experience and Certifications.",

        "Use job-relevant technical keywords naturally instead of keyword stuffing.",

        "Describe projects using the technology used and what you actually built.",

        "Use measurable results wherever possible, such as percentages, counts or performance improvements.",

        "Keep formatting simple and readable so ATS systems can process the resume.",

        "List your strongest and most relevant technical skills first.",

        "Customize the resume according to the job role you are applying for.",

        "Avoid adding skills that you do not actually know."
    ]


    for tip in tips:

        st.write(
            f"• {tip}"
        )


    # =========================================================
    # RECOMMENDED RESUME STRUCTURE
    # =========================================================

    st.subheader(
        "📄 Recommended Resume Structure"
    )


    structure_data = pd.DataFrame({

        "Priority": [

            1,
            2,
            3,
            4,
            5,
            6,
            7

        ],

        "Section": [

            "Professional Summary / Career Objective",
            "Technical Skills",
            "Education",
            "Projects",
            "Internships / Experience",
            "Certifications",
            "Achievements"

        ],

        "Purpose": [

            "Quickly explain your profile and target role.",
            "Show relevant technical skills.",
            "Show academic background.",
            "Demonstrate practical technical work.",
            "Show real-world experience.",
            "Show completed courses and certifications.",
            "Highlight important accomplishments."

        ]

    })


    st.dataframe(
        structure_data,
        use_container_width=True,
        hide_index=True
    )


    # =========================================================
    # TARGET ROLE IMPROVEMENT
    # =========================================================

    st.subheader(
        "🎯 Improve Specifically for Your Top Job"
    )


    st.write(
        f"### {best_job['job_title']}"
    )


    st.write(
        f"Current match: **{best_score:.1f}%**"
    )


    if best_job["missing_skills"]:

        st.write(
            "To improve your match, focus on:"
        )

        for skill in best_job[
            "missing_skills"
        ]:

            st.write(
                f"📚 **{skill.title()}**"
            )

    else:

        st.success(
            "🎉 Your detected skills already cover "
            "the requirements of this role."
        )


    # =========================================================
    # FINAL RECOMMENDATION
    # =========================================================

    st.subheader(
        "🏁 Final Resume Recommendation"
    )


    if ats_score >= 80 and best_score >= 70:

        st.success(
            "🚀 Your resume is in a strong position. "
            "Before applying, customize the resume "
            "slightly for each job and highlight the "
            "skills requested in the job description."
        )

    elif ats_score >= 60:

        st.info(
            "👍 Your resume has a good foundation. "
            "Improve the missing skills, job-specific "
            "keywords and resume sections before applying."
        )

    else:

        st.warning(
            "📈 Focus first on improving your technical "
            "skills, resume structure, keywords and "
            "project/experience content."
        )


    # =========================================================
    # EXPLORE ANY JOB
    # =========================================================

    st.divider()

    st.header(
        "🎯 Explore Any Job"
    )

    st.write(
        "Explore all available job roles, check your "
        "skill match, and identify skills you should improve."
    )


    # =========================================================
    # LOAD JOBS
    # =========================================================

    explore_jobs = load_jobs().copy()


    # =========================================================
    # FILTER SECTION
    # =========================================================

    filter_col1, filter_col2 = (
        st.columns(2)
    )


    with filter_col1:

        if "category" in explore_jobs.columns:

            categories = sorted(
                explore_jobs["category"]
                .dropna()
                .unique()
                .tolist()
            )

        else:

            categories = []


        selected_category = st.selectbox(
            "🏷️ Filter by Job Category",
            ["All Categories"] + categories
        )


    with filter_col2:

        search_job = st.text_input(
            "🔎 Search Job Role",
            placeholder="Example: Python Developer"
        )


    # =========================================================
    # APPLY FILTER
    # =========================================================

    filtered_jobs = (
        explore_jobs.copy()
    )


    if selected_category != "All Categories":

        filtered_jobs = filtered_jobs[
            filtered_jobs["category"]
            ==
            selected_category
        ]


    if search_job.strip():

        filtered_jobs = filtered_jobs[
            filtered_jobs["job_title"]
            .str.contains(
                search_job.strip(),
                case=False,
                na=False
            )
        ]


    # =========================================================
    # NO JOB FOUND
    # =========================================================

    if filtered_jobs.empty:

        st.warning(
            "No job roles found. Try another search."
        )

    else:

        # =====================================================
        # SELECT JOB
        # =====================================================

        selected_job_title = st.selectbox(
            "💼 Select a Job Role",
            sorted(
                filtered_jobs[
                    "job_title"
                ].tolist()
            )
        )


        # =====================================================
        # GET SELECTED JOB
        # =====================================================

        selected_job = filtered_jobs[
            filtered_jobs["job_title"]
            ==
            selected_job_title
        ].iloc[0]


        # =====================================================
        # REQUIRED SKILLS
        # =====================================================

        selected_job_skills = [

            skill.strip().lower()

            for skill in str(
                selected_job["skills"]
            ).split(",")

            if skill.strip()

        ]


        # =====================================================
        # MATCH SKILLS
        # =====================================================

        selected_matched = []

        selected_missing = []


        for skill in selected_job_skills:

            if skill in resume_skills:

                selected_matched.append(
                    skill
                )

            else:

                selected_missing.append(
                    skill
                )


        # =====================================================
        # SKILL MATCH SCORE
        # =====================================================

        if selected_job_skills:

            selected_skill_score = (

                len(selected_matched)
                /
                len(selected_job_skills)

            ) * 100

        else:

            selected_skill_score = 0


        # =====================================================
        # JOB HEADER
        # =====================================================

        st.divider()

        st.subheader(
            f"💼 {selected_job_title}"
        )


        # =====================================================
        # JOB INFORMATION
        # =====================================================

        info_col1, info_col2, info_col3 = (
            st.columns(3)
        )


        with info_col1:

            st.metric(
                "📊 Skill Match",
                f"{selected_skill_score:.1f}%"
            )


        with info_col2:

            if "category" in selected_job:

                st.metric(
                    "🏷️ Category",
                    str(
                        selected_job["category"]
                    )
                )


        with info_col3:

            if "experience_level" in selected_job:

                st.metric(
                    "💼 Experience",
                    str(
                        selected_job["experience_level"]
                    )
                )


        # =====================================================
        # MATCH PROGRESS
        # =====================================================

        st.write(
            "### 📈 Your Skill Match"
        )

        st.progress(
            min(
                int(selected_skill_score),
                100
            )
        )


        if selected_skill_score >= 80:

            st.success(
                "🟢 Excellent match! "
                "You have most of the required skills."
            )

        elif selected_skill_score >= 60:

            st.info(
                "🟡 Good match! "
                "A few additional skills can improve your profile."
            )

        elif selected_skill_score >= 40:

            st.warning(
                "🟠 Moderate match. "
                "Consider learning the missing skills."
            )

        else:

            st.error(
                "🔴 Low match. "
                "You should improve several required skills."
            )


        # =====================================================
        # JOB DETAILS
        # =====================================================

        st.subheader(
            "📝 Job Details"
        )


        detail_col1, detail_col2 = (
            st.columns(2)
        )


        with detail_col1:

            if "category" in selected_job:

                st.write(
                    "**🏷️ Category:** "
                    +
                    str(
                        selected_job["category"]
                    )
                )


            if "experience_level" in selected_job:

                st.write(
                    "**💼 Experience Level:** "
                    +
                    str(
                        selected_job["experience_level"]
                    )
                )


        with detail_col2:

            if "education" in selected_job:

                st.write(
                    "**🎓 Education:** "
                    +
                    str(
                        selected_job["education"]
                    )
                )


        st.write(
            "### 📖 Job Description"
        )

        st.write(
            str(
                selected_job["description"]
            )
        )


        # =====================================================
        # REQUIRED SKILLS
        # =====================================================

        st.subheader(
            "🛠️ Required Skills"
        )


        required_text = " • ".join(
            skill.title()
            for skill in selected_job_skills
        )


        st.info(
            required_text
        )


        # =====================================================
        # SKILL GAP ANALYSIS
        # =====================================================

        st.subheader(
            "🎯 Skill Gap Analysis"
        )


        gap_col1, gap_col2 = (
            st.columns(2)
        )


        with gap_col1:

            st.write(
                "### ✅ Skills You Have"
            )


            if selected_matched:

                for skill in selected_matched:

                    st.success(
                        f"✓ {skill.title()}"
                    )

            else:

                st.write(
                    "No matching skills found."
                )


        with gap_col2:

            st.write(
                "### ❌ Skills to Improve"
            )


            if selected_missing:

                for skill in selected_missing:

                    st.warning(
                        f"• {skill.title()}"
                    )

            else:

                st.success(
                    "🎉 You have all the required skills!"
                )


        # =====================================================
        # LEARNING RECOMMENDATIONS
        # =====================================================

        st.subheader(
            "📚 Recommended Skills to Learn"
        )


        if selected_missing:

            learning_df = pd.DataFrame({

                "Priority": range(
                    1,
                    len(selected_missing) + 1
                ),

                "Skill to Learn": [

                    skill.title()

                    for skill
                    in selected_missing

                ]

            })


            st.dataframe(
                learning_df,
                use_container_width=True,
                hide_index=True
            )


            st.info(
                "💡 Learning these skills and "
                "building projects with them can "
                "increase your chances of matching "
                "this role."
            )

        else:

            st.success(
                "🚀 No additional skills recommended. "
                "You are well matched for this role!"
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Resume Screening & Job Recommendation System | "
    "Python • NLP • TF-IDF • Machine Learning • Streamlit"
)