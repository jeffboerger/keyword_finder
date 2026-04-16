# Resume Keyword Analyzer

## Live Demo
[Try the Resume Keyword Analyzer](https://keywordfinder-i35ugxfb5kexfqc4mzokrp.streamlit.app/)

## Overview
A Python NLP tool that scores your resume against a job description by matching
industry keywords using fuzzy string matching. Inspired by *What Color Is Your Parachute*
by Richard Bolles — the idea being to match your language to what employers are actually
looking for.

Built to solve a real problem: most job seekers apply blindly without knowing how well
their resume aligns with the language in the job posting. This tool makes that gap
visible and actionable — and now highlights it directly in the job description itself.

## Features
- **Highlighted Job Description** — after analysis, the full JD renders with color-coded highlights
  - 🟢 Green = keyword in both JD and resume (you have it)
  - 🟡 Yellow = keyword in JD but missing from resume (add this)
- **N-gram phrase matching** — multi-word phrases like "data analytics" and "attention to detail" highlight as a single unit
- **Role-specific keyword sets** — Select Data Engineer, Data Analyst, or Software Engineer
- **Fuzzy matching** — catches keyword variations using thefuzz/RapidFuzz with 90% threshold
- **Resume score** — percentage match against job description keywords
- **Gap analysis** — shows exactly which keywords to add to reach 70% match
- **Flexible resume input** — paste text or upload .txt, .docx, or .pdf
- **Job description input** — paste text, upload file, or scrape directly from a URL
- **CLI support** — run from the terminal against any job description file or URL

## Tech Stack
- Python 3.11
- Streamlit
- thefuzz / RapidFuzz (fuzzy string matching)
- pdfplumber (PDF resume extraction)
- python-docx (.docx resume extraction)
- BeautifulSoup4 (URL scraping)
- Requests

## Keyword Files
Three comprehensive keyword files covering 1,000+ terms across all data roles:

| File | Keywords | Description |
|---|---|---|
| `data_jobs_keywords.csv` | 717 | Core technical keywords with categories — tools, frameworks, concepts, cloud platforms, ML/AI |
| `soft_skills_keywords.csv` | 140 | Soft skills and interpersonal keywords |
| `industry_keywords.csv` | 346 | Industry-specific terms — fintech, healthcare, retail, supply chain, GenAI |

Keywords were sourced from real 2024–2026 job postings across Indeed, LinkedIn, Dice, and Built In,
cross-referenced with the 365 Data Science 2025 Job Outlook and Kaggle State of Data Science 2024 surveys.

## How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/jeffboerger/keyword_finder.git
cd keyword_finder
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Launch the Streamlit app
```bash
streamlit run app.py
```

5. Or run from the command line
```bash
python3 keyword_finder.py --job data/job_desc.txt --resume data/resume.txt
python3 keyword_finder.py --url https://jobs.example.com/posting --resume data/resume.txt
```

## Project Structure
```
keyword_finder/
├── app.py                        # Streamlit web interface
├── keyword_finder.py             # Core logic: loading, fuzzy matching, scoring, reporting
├── data/
│   ├── data_jobs_keywords.csv    # 717 technical keywords with categories
│   ├── soft_skills_keywords.csv  # 140 soft skill keywords
│   ├── industry_keywords.csv     # 346 industry-specific keywords
│   ├── keyword_documentation.md  # Methodology and scoring recommendations
│   ├── de_keywords.csv           # Data Engineering role-specific list (role selector)
│   ├── da_keywords.csv           # Data Analytics role-specific list (role selector)
│   └── swe_keywords.csv          # Software Engineering role-specific list (role selector)
└── requirements.txt
```

## Background
The keyword list was originally inspired by *What Color Is Your Parachute* by Richard Bolles,
which emphasizes matching your skills language to employer language. The list has been
significantly expanded using real job posting research across multiple sources and is
continuously refined as new tools and frameworks emerge in the data engineering market.

This tool is actively used by the author to optimize every job application — each posting
is run through the analyzer before submitting to identify and close keyword gaps.

## Future Improvements
- **Click-to-dismiss false positives** — remove fuzzy matched keywords that don't apply, recalculate score dynamically
- **Two-column view** — JD highlighted on left, matching resume bullet on right
- **Weighted scoring** — keywords weighted by frequency across job postings
- **Employer Mode** — upload multiple resumes, rank all candidates against a JD, export to CSV
- Expand role-specific keyword sets with more granular filtering by category
- Integrate with job board APIs for direct URL importing
