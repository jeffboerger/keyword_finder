import csv
import argparse
from thefuzz import fuzz

def load_keywords(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]
    

def load_text(path):
    with open(path, 'r') as f:
        return f.read()

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
    parser.add_argument("--job",      required=True,  help="Path to job description .txt file")
    parser.add_argument("--resume",   required=True,  help="Path to your resume .txt file")
    parser.add_argument("--keywords", default="data/keywords.csv", help="Path to keyword CSV")
    parser.add_argument("--output",   default="Report.txt",        help="Output report filename")
    return parser.parse_args()

def main():
    args = parse_args()

    # Load all inputs
    print("Loading keywords and files...")
    keyword_list = load_keywords(args.keywords)
    job_text = load_text(args.job)
    resume_text = load_text(args.resume)    

    print("Analyzing matches...")
    job_keywords = find_matches(keyword_list, job_text)
    resume_keywords = find_matches(keyword_list, resume_text)
    results = compare_keywords(job_keywords, resume_keywords)

    # Score and Report
    score, needed_for_70 = calculate_score(job_keywords, results["in_both"])
    write_report(args.output, score, needed_for_70, results)

    # Confirm to the user in the terminal
    print(f"Report written to: {args.output}")
    print(f"Score: {score:.1f}% | Need {needed_for_70:.0f} more to hit 70%")

if __name__ == "__main__":
    main()
