from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from docx import Document
from rapidfuzz import fuzz
import pdfplumber

# Default corpus: the three categorized keyword files
DEFAULT_KEYWORD_FILES = [
    "data/data_jobs_keywords.csv",
    "data/soft_skills_keywords.csv",
    "data/industry_keywords.csv",
]

# Ambiguous short tokens that only cause false positives (module-level:
# built once, not rebuilt inside the matching loop)
EXCLUDE = {"or", "ar", "rn", "pr", "ui", "os", "bi", "gui",
           "c", "r", "e", "lan", "flex", "art", "creative"}

# Category weights for weighted scoring — high-signal technical categories
# outweigh soft skills, per real screening behavior
CATEGORY_WEIGHTS = {
    "data engineering": 3.0,
    "etl tools": 3.0,
    "orchestration tools": 3.0,
    "transformation tools": 3.0,
    "databases": 2.5,
    "cloud platforms": 2.5,
    "cloud data platforms": 2.5,
    "cloud services": 2.5,
    "big data frameworks": 2.5,
    "programming languages": 2.0,
    "python libraries": 2.0,
    "analytics": 2.0,
    "visualization tools": 2.0,
    "data science": 1.5,
    "mlops": 1.5,
    "data governance": 1.5,
    "concepts": 1.0,
    "advanced concepts": 1.0,
    "certifications": 1.0,
    "education": 1.0,
}
DEFAULT_WEIGHT = 1.0


def load_keywords(path):
    """Load keyword strings (column 0). Handles BOM, headers, blank rows."""
    keywords = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            kw = row[0].lower().strip()
            if kw in ("keyword", "candidate"):   # header rows
                continue
            keywords.append(kw)
    return keywords


def load_categories(paths=None):
    """keyword -> category across the corpus files (for weighted scoring)."""
    cats = {}
    for path in paths or DEFAULT_KEYWORD_FILES:
        if not Path(path).exists():
            continue
        with open(path, newline="", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                if not row or not row[0].strip():
                    continue
                kw = row[0].lower().strip()
                if kw in ("keyword", "candidate"):
                    continue
                cat = row[1].lower().strip() if len(row) > 1 else ""
                cats.setdefault(kw, cat)
    return cats


def load_text(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def load_docx(file_path):
    """Extract text from a Word Document (.docx file)"""
    doc = Document(file_path)
    return " ".join(paragraph.text for paragraph in doc.paragraphs)


def load_pdf(file_path):
    """Extract text from a PDF File."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def scrape_job_url(url):
    """Fetch a job posting URL and return its visible text."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def find_matches(keyword_list, text):
    """Keywords from keyword_list present in text.

    Word-boundary regex first (plural-tolerant: 'reconciliation' matches
    'reconciliations'), so 'java' never matches 'javascript' and 'sql'
    never matches 'postgresql'. Fuzzy matching is a fallback for long
    multi-word phrases only, where slight rewording is common.
    """
    text_l = text.lower()
    # punctuation-normalized copy for the fuzzy path ("extract, transform, load")
    text_fuzzy = re.sub(r"\s+", " ", re.sub(r"[,;:()/|]", " ", text_l))
    matches = []
    for key in dict.fromkeys(k.lower().strip() for k in keyword_list):
        if key in EXCLUDE:
            continue
        if re.search(r"(?<![a-z0-9])" + re.escape(key) + r"(?:s|es)?(?![a-z0-9])",
                     text_l):
            matches.append(key)
        elif " " in key and len(key) > 8:
            if fuzz.partial_ratio(key, text_fuzzy) >= 95:
                matches.append(key)
    return matches


def compare_keywords(job_keywords, resume_keywords):
    job_set = set(job_keywords)
    resume_set = set(resume_keywords)
    return {
        "in_both": list(job_set & resume_set),
        "job_only": list(job_set - resume_set),
        "resume_only": list(resume_set - job_set),
    }


def calculate_score(job_keywords, in_both):
    """Simple coverage: % of job keywords found in resume, + gap to 70%."""
    total = len(job_keywords)
    matched = len(in_both)
    score = (matched / total * 100) if total > 0 else 0
    needed_for_70 = max(0, (total * 0.7) - matched)
    return score, needed_for_70


def calculate_weighted_score(job_keywords, in_both, categories):
    """Category-weighted coverage: matching 'airflow' counts 3x a soft skill."""
    def w(kw):
        return CATEGORY_WEIGHTS.get(categories.get(kw, ""), DEFAULT_WEIGHT)
    total = sum(w(k) for k in set(job_keywords))
    matched = sum(w(k) for k in set(in_both))
    return (matched / total * 100) if total > 0 else 0


def write_section(file, label, keyword_list):
    """Write a Single Labeled Section to an already-open file"""
    file.write(f"{label}:\n{len(keyword_list)}\n\n")
    for kw in sorted(keyword_list):
        file.write(kw + "\n")
    file.write("\n\n")


def write_report(output_path, score, needed_for_70, results, weighted=None):
    with open(output_path, "w") as f:
        f.write("Resume Score with this Job Description:\n\n")
        f.write(f"{score:.1f}%\n")
        if weighted is not None:
            f.write(f"Weighted (by category importance): {weighted:.1f}%\n")
        f.write(f"\nAdd {needed_for_70:.0f} keywords to reach 70%\n\n")
        write_section(f, "Keywords to Add to Resume (in Job Description, not Resume)", results["job_only"])
        write_section(f, "Keywords in Both Job Description and Resume", results["in_both"])
        write_section(f, "Keywords in Resume Only", results["resume_only"])


def parse_args():
    parser = argparse.ArgumentParser(description="Keyword match your resume to a job description.")
    parser.add_argument("--job", help="Path to job description file (.txt/.docx/.pdf)")
    parser.add_argument("--url", help="URL of job posting to scrape")
    parser.add_argument("--resume", required=True, help="Path to your resume (.txt/.docx/.pdf)")
    parser.add_argument("--keywords", default=None,
                        help="Custom keyword CSV (default: the three data/*.csv corpus files)")
    parser.add_argument("--output", default="Report.txt", help="Output report filename")
    return parser.parse_args()


def _load_any(path):
    ext = path.split(".")[-1].lower()
    if ext == "docx":
        return load_docx(path)
    if ext == "pdf":
        return load_pdf(path)
    return load_text(path)


def main():
    args = parse_args()

    print("Loading keywords and files...")
    if args.keywords:
        keyword_list = load_keywords(args.keywords)
        categories = load_categories([args.keywords])
    else:
        keyword_list = []
        for path in DEFAULT_KEYWORD_FILES:
            if Path(path).exists():
                keyword_list += load_keywords(path)
        categories = load_categories()
    if not keyword_list:
        print("Error: no keyword files found (looked for data/*.csv)")
        return

    if args.url:
        print(f"Scraping job posting from {args.url}...")
        job_text = scrape_job_url(args.url)
    elif args.job:
        job_text = _load_any(args.job)
    else:
        print("Error: please provide either --job or --url")
        return

    print("Analyzing matches...")
    resume_text = _load_any(args.resume)

    job_keywords = find_matches(keyword_list, job_text)
    resume_keywords = find_matches(keyword_list, resume_text)
    results = compare_keywords(job_keywords, resume_keywords)

    score, needed_for_70 = calculate_score(job_keywords, results["in_both"])
    weighted = calculate_weighted_score(job_keywords, results["in_both"], categories)
    write_report(args.output, score, needed_for_70, results, weighted)

    print(f"Report written to: {args.output}")
    print(f"Score: {score:.1f}% (weighted {weighted:.1f}%) | Need {needed_for_70:.0f} more to hit 70%")


if __name__ == "__main__":
    main()
