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
    if len(job_keywords) == 0:
        return 0
    percent_score = (len(in_both) / len(job_keywords)) * 100
    return percent_score

def write_report(output_path, score, results):
    with open(output_path, 'w') as f:
        # Resume Score
        f.write(f"Resume Score:\n\n{score:.1f}%\n\n")
        # Job Only
        f.write(f"Keywords to Add to Resume:\n")
        f.write(f"{len(results['job_only'])}\n\n")
        for keyword in results["job_only"]:
            f.write(keyword + "\n")
        f.write("\n")
        # In Both
        f.write(f"Keywords in Both:\n")
        f.write(f"{len(results['in_both'])}\n\n")
        for keyword in results["in_both"]:
            f.write(keyword + "\n")
        f.write("\n")
        # Resume Only
        f.write(f"Resume Only:\n")
        f.write(f"{len(results['resume_only'])}\n\n")
        for keyword in results["resume_only"]:
            f.write(keyword + "\n")
        f.write("\n")

def parse_args():
    parser = argparse.ArgumentParser(description="Keyword match your resume to a job description.")
    parser.add_argument("--job",      required=True,  help="Path to job description .txt file")
    parser.add_argument("--resume",   required=True,  help="Path to your resume .txt file")
    parser.add_argument("--keywords", default="data/keywords.csv", help="Path to keyword CSV")
    parser.add_argument("--output",   default="Report.txt",        help="Output report filename")
    return parser.parse_args()

def main():
    args = parse_args()
    keyword_list = load_keywords(args.keywords)
    job_text = load_text(args.job)
    resume_text = load_text(args.resume)

    job_keywords = find_matches(keyword_list, job_text)
    resume_keywords = find_matches(keyword_list, resume_text)

    results = compare_keywords(job_keywords, resume_keywords)
    score = calculate_score(job_keywords, results["in_both"])
    write_report("Report.txt", score, results)

if __name__ == "__main__":
    main()
