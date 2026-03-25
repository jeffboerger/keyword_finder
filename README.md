# Resume Keyword Analyzer

## Live Demo
[Try the Resume Keyword Analyzer](https://keywordfinder-i35ugxfb5kexfqc4mzokrp.streamlit.app/)

## Overview
A Python tool that scores your resume against a job description by matching 
industry keywords. Inspired by *What Color Is Your Parachute* by Richard Bolles 
— the idea being to match your language to what employers are actually looking for.

Built to solve a real problem: most job seekers apply blindly without knowing 
how well their resume aligns with the language in the job posting. This tool 
makes that gap visible and actionable.

## Features
- **Role-specific keyword lists** — Select Data Engineer, Data Analyst, or 
  Software Engineer to load targeted keyword sets
- **Fuzzy matching** — Catches keyword variations (e.g. "python scripting" 
  matches "python")
- **Resume score** — Percentage match against the job description keywords
- **Gap analysis** — Shows exactly which keywords to add to reach 70% match
- **Flexible input** — Paste job description directly or upload resume as .txt file
- **CLI support** — Run from the terminal against any job description file or URL

## Tech Stack
- Python
- Streamlit
- thefuzz (fuzzy string matching)
- BeautifulSoup4 (URL scraping)
- NLTK

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
```

## Project Structure
- `keyword_finder.py` — Core logic: keyword loading, fuzzy matching, scoring, reporting
- `app.py` — Streamlit web interface
- `scripts/build_keyword_list.py` — Script for scraping and building keyword lists
- `data/de_keywords.csv` — Data Engineering keyword list
- `data/da_keywords.csv` — Data Analytics keyword list
- `data/swe_keywords.csv` — Software Engineering keyword list
- `data/tech_keywords.csv` — Combined tech keyword list

## Background
The keyword list was originally inspired by *What Color Is Your Parachute* 
by Richard Bolles, which emphasizes matching your skills language to employer 
language. The list was expanded by manually analyzing real DE, DA, and SWE 
job postings and is continuously refined as new tools and frameworks emerge 
in the job market.

## Future Improvements
- Add weighted scoring based on keyword frequency across job postings
- Expand keyword lists with more role-specific terms
- Add PDF resume support
- Add phrase matching for multi-word technical terms
- Integrate with job board APIs for direct URL importing
- How to Market this for Businesses, so they can see who to interview?
- **Employer Mode** - A Second page for hiring managers to upload multiple resumes, automatically score and rank all candidates against a job description, and view results in an interactive table with click-to-expand resume preview and CSV Export