import streamlit as st
from keyword_finder import(
    load_keywords, load_text, find_matches,compare_keywords, calculate_score, write_report
)

st.title ("Resume Keyword Analyzer")
st.caption("Inspired by What Color is Your Parachute - match your language to employer language")

# Role Selector
st.subheader("Select Target Role")
col1, col2, col3 = st.columns(3)
de = col1.checkbox("Data Engineer", value=True)
da = col2.checkbox("Data Analyst", value=True)
swe = col3.checkbox("Software Engineer", value=True)

# Load Keywords based on Role Selection
keywords = []

if de:
    keywords += load_keywords('data/de_keywords.csv')
if da:
    keywords += load_keywords('data/da_keywords.csv')
if swe:
    keywords += load_keywords('data/swe_keywords.csv')

# Remove Duplicates
keywords = list(set(keywords))

if not keywords:
    st.warning("Please select at least one role above.")
    st.stop()

st.caption(f"Analyzing Against {len(keywords)} keywords.")

# Input Section
st.subheader("Job Description")
job_text = st.text_area("Paste the job description here", height=200)

st.subheader("Your Resume")
resume_option = st.radio("Input method", ["Paste text", "Upload file"], horizontal=True)

if resume_option == "Upload file":
    uploaded_file = st.file_uploader("Upload resume as .txt file", type=["txt"])
    if uploaded_file:
        resume_text = uploaded_file.read().decode("utf-8")
    else:
        resume_text = ""
else:
    resume_text = st.text_area("Paste your resume here", height=200)


if st.button("Analyze"):
    if not job_text or not resume_text:
        st.warning("Please paste both a job description and your resume.")
    else:
        with st.spinner("Analyzing..."):
            job_keywords = find_matches(keywords, job_text)
            resume_keywords = find_matches(keywords, resume_text)
            results = compare_keywords(job_keywords, resume_keywords)
            score, needed = calculate_score(job_keywords, results["in_both"])

        # Display Results
        st.subheader("Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Match Score", f"{score:.1f}%")
        col2.metric("Keywords Matched", len(results["in_both"]))
        col3.metric("Keywords to Add", len(results["job_only"]))

        if needed > 0:
            st.info(f"Add {needed:.0f} more keywords to reach 70%")
        else:
            st.success("You're above 70% — strong match!")

        if results["job_only"]:
            st.subheader("Keywords to Add to Your Resume")
            st.write(", ".join(sorted(results["job_only"])))

        if results["in_both"]:
            st.subheader("Keywords You Already Have")
            st.write(", ".join(sorted(results["in_both"])))