import streamlit as st
import tempfile
import re
from keyword_finder import (
    load_keywords, find_matches, compare_keywords,
    calculate_score, load_docx, load_pdf
)

st.title("Resume Keyword Analyzer")
st.caption("Inspired by What Color is Your Parachute - match your language to employer language")

# --- Role Selector ---
st.subheader("Select Target Role")
col1, col2, col3 = st.columns(3)
de = col1.checkbox("Data Engineer", value=True)
da = col2.checkbox("Data Analyst", value=True)
swe = col3.checkbox("Software Engineer", value=False)

# --- Load Keywords ---
keywords = []
keywords += load_keywords('data/data_jobs_keywords.csv')
keywords += load_keywords('data/soft_skills_keywords.csv')
keywords += load_keywords('data/industry_keywords.csv')
keywords = list(set(keywords))

if not keywords:
    st.warning("Please select at least one role above.")
    st.stop()

st.caption(f"Analyzing against {len(keywords)} keywords.")

# --- Input Section ---
st.subheader("Job Description")
job_text = st.text_area("Paste the job description here", height=200)

st.subheader("Your Resume")
resume_option = st.radio("Input method", ["Paste text", "Upload file"], horizontal=True)

if resume_option == "Upload file":
    uploaded_file = st.file_uploader(
        "Upload resume (.txt, .docx, or .pdf)",
        type=["txt", "docx", "pdf"]
    )
    if uploaded_file:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == 'txt':
            resume_text = uploaded_file.read().decode("utf-8")
        elif file_type == 'docx':
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                tmp.write(uploaded_file.read())
                resume_text = load_docx(tmp.name)
        elif file_type == 'pdf':
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(uploaded_file.read())
                resume_text = load_pdf(tmp.name)
    else:
        resume_text = ""
else:
    resume_text = st.text_area("Paste your resume here", height=200)


# --- Highlighting Function ---
def highlight_jd(job_text, in_both, job_only):
    """
    Returns HTML of the job description with keywords highlighted.
    Green = keyword in both JD and resume (you have it)
    Yellow = keyword in JD but not resume (gap - add this)
    """
    lines = job_text.split('\n')
    highlighted_lines = []

    for line in lines:
        words = line.split()
        highlighted_words = []
        i = 0

        while i < len(words):
            # Try trigram first
            if i + 2 < len(words):
                trigram = ' '.join([re.sub(r'[^a-z0-9\s]', '', w.lower()) for w in words[i:i+3]])
                if trigram in in_both:
                    phrase = ' '.join(words[i:i+3])
                    highlighted_words.append(
                        f'<span style="background-color:#d4edda; color:#155724; '
                        f'padding:1px 3px; border-radius:3px; font-weight:bold;">{phrase}</span>'
                    )
                    i += 3
                    continue
                elif trigram in job_only:
                    phrase = ' '.join(words[i:i+3])
                    highlighted_words.append(
                        f'<span style="background-color:#fff3cd; color:#856404; '
                        f'padding:1px 3px; border-radius:3px; font-weight:bold;">{phrase}</span>'
                    )
                    i += 3
                    continue

            # Try bigram
            if i + 1 < len(words):
                bigram = ' '.join([re.sub(r'[^a-z0-9\s]', '', w.lower()) for w in words[i:i+2]])
                if bigram in in_both:
                    phrase = ' '.join(words[i:i+2])
                    highlighted_words.append(
                        f'<span style="background-color:#d4edda; color:#155724; '
                        f'padding:1px 3px; border-radius:3px; font-weight:bold;">{phrase}</span>'
                    )
                    i += 2
                    continue
                elif bigram in job_only:
                    phrase = ' '.join(words[i:i+2])
                    highlighted_words.append(
                        f'<span style="background-color:#fff3cd; color:#856404; '
                        f'padding:1px 3px; border-radius:3px; font-weight:bold;">{phrase}</span>'
                    )
                    i += 2
                    continue

            # Fall back to single word
            clean = re.sub(r'[^a-z0-9\s]', '', words[i].lower())
            if clean in in_both:
                highlighted_words.append(
                    f'<span style="background-color:#d4edda; color:#155724; '
                    f'padding:1px 3px; border-radius:3px; font-weight:bold;">{words[i]}</span>'
                )
            elif clean in job_only:
                highlighted_words.append(
                    f'<span style="background-color:#fff3cd; color:#856404; '
                    f'padding:1px 3px; border-radius:3px; font-weight:bold;">{words[i]}</span>'
                )
            else:
                highlighted_words.append(words[i])
            i += 1

        highlighted_lines.append(' '.join(highlighted_words))

    return '<br/>'.join(highlighted_lines)


# --- Analyze ---
if st.button("Analyze"):
    if not job_text or not resume_text:
        st.warning("Please paste both a job description and your resume.")
    else:
        with st.spinner("Analyzing..."):
            job_keywords = find_matches(keywords, job_text)
            resume_keywords = find_matches(keywords, resume_text)
            results = compare_keywords(job_keywords, resume_keywords)
            score, needed = calculate_score(job_keywords, results["in_both"])

        # --- Display Results ---
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
            st.subheader("🟡 Keywords to Add to Your Resume")
            st.write(", ".join(sorted(results["job_only"])))

        if results["in_both"]:
            st.subheader("🟢 Keywords You Already Have")
            st.write(", ".join(sorted(results["in_both"])))

        # --- Highlighted JD ---
        st.divider()
        st.subheader("📋 Highlighted Job Description")
        st.caption("🟢 Green = you have it | 🟡 Yellow = add this to your resume")

        highlighted_html = highlight_jd(
            job_text,
            set(results["in_both"]),
            set(results["job_only"])
        )

        st.markdown(
            f'<div style="line-height:1.8; font-size:0.95rem;">{highlighted_html}</div>',
            unsafe_allow_html=True
        )