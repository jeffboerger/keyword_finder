import csv
import argparse
from thefuzz import fuzz
import requests
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber

def load_keywords(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        keywords = []
        for i, row in enumerate(reader):
            if not row:
                continue
            # Skip header row if first column is literally "keyword"
            if i == 0 and row[0].lower().strip() == "keyword":
                continue
            keywords.append(row[0].lower().strip())
        return keywords
    

def load_text(path):
    with open(path, 'r') as f:
        return f.read()
    
def load_docx(file_path):
    """Extract text from a Word Document (.docx file)"""
    doc = Document(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])

def load_pdf(file_path):
    """Extract text from a PDF File."""
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text

def scrape_job_url(url):
    """
    Fetch a job posting from a URL and return the text content.
    Returns a string in same format as load_text() so pipeline continues to work
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def find_matches(keyword_list, text):
    matches = []
    text = text.lower()


    for key in keyword_list:
        key = key.lower()

        exclude = {'or', 'ar', 'rn', 'pr', 'ui', 'os', 'bi', 'gui', 
               'c', 'r', 'e', 'lan', 'flex', 'art', 'creative'}

        if key in exclude:
            continue

        if len(key) <= 3:
            if key in text:
                matches.append(key)
        else:         
            score = fuzz.partial_ratio(key, text)
            if score >= 90:
                matches.append(key)
    return matches

def compare_keywords(job_keywords, resume_keywords):
    job_set = set(job_keywords)
    resume_set = set(resume_keywords)

    in_both = job_set & resume_set
    job_only = job_set - resume_set
    resume_only = resume_set - job_set

    return {
        "in_both": list(in_both),
        "job_only": list(job_only),
        "resume_only": list(resume_only)
    }

def calculate_score(job_keywords, in_both):
    """
    Score = how many job keywords are covered by the resume.
    Also returns how many more keywords are needed to hit 70%.
    """
    total = len(job_keywords)
    matched = len(in_both)
    score = (matched / total * 100) if total > 0 else 0
    needed_for_70 = max(0, (total * 0.7) - matched)
    return score, needed_for_70

def write_section(file, label, keyword_list):
    """Write a Single Labeled Section to an already-open file"""
    file.write(f"{label}:\n")
    file.write(f"{len(keyword_list)}\n\n")
    for kw in keyword_list:
        file.write(kw + "\n")
    file.write("\n\n")

def write_report(output_path, score, needed_for_70, results):
    """
    Build the full report file.
    Accepts the score, the gap-to-70, and the results dict from compare_keywords().
    """
    with open(output_path, 'w') as f:
        f.write("Resume Score with this Job Description:\n\n")
        f.write(f"{score:.1f}%\n\n")
        f.write(f"Add {needed_for_70:.0f} keywords to reach 70%\n\n")
        write_section(f, "Keywords to Add to Resume (in Job Description, not Resume)", results["job_only"])
        write_section(f, "Keywords in Both Job Description and Resume", results["in_both"])
        write_section(f, "Keywords in Resume Only", results["resume_only"])

def parse_args():
    parser = argparse.ArgumentParser(description="Keyword match your resume to a job description.")
    parser.add_argument("--job",      required=False,  help="Path to job description .txt file")
    parser.add_argument("--url",      required= False, help="URL of job posting to scrape")
    parser.add_argument("--resume",   required=True,  help="Path to your resume .txt file")
    parser.add_argument("--keywords", default="data/ai_generated_keyword_list.csv", help="Path to keyword CSV")
    parser.add_argument("--output",   default="Report.txt",        help="Output report filename")
    return parser.parse_args()

def main():
    args = parse_args()

    # Load keywords
    print("Loading keywords and files...")
    keyword_list = load_keywords(args.keywords)

    # Load job description
    if args.url:
        print(f"Scraping job posting from {args.url}...")
        job_text = scrape_job_url(args.url)
    elif args.job:
        ext = args.job.split('.')[-1].lower()
        if ext == 'docx':
            job_text = load_docx(args.job)
        elif ext == 'pdf':
            job_text = load_pdf(args.job)
        else:
            job_text = load_text(args.job)
    else:
        print("Error: please provide either --job or --url")
        return

    # Load resume
    print("Analyzing matches...")
    ext = args.resume.split('.')[-1].lower()
    if ext == 'docx':
        resume_text = load_docx(args.resume)
    elif ext == 'pdf':
        resume_text = load_pdf(args.resume)
    else:
        resume_text = load_text(args.resume)

    # Run matching
    job_keywords    = find_matches(keyword_list, job_text)
    resume_keywords = find_matches(keyword_list, resume_text)
    results         = compare_keywords(job_keywords, resume_keywords)

    # Score and report
    score, needed_for_70 = calculate_score(job_keywords, results["in_both"])
    write_report(args.output, score, needed_for_70, results)

    # Confirm to user
    print(f"Report written to: {args.output}")
    print(f"Score: {score:.1f}% | Need {needed_for_70:.0f} more to hit 70%")


if __name__ == "__main__":
    main()
