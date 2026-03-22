import csv
import argparse


# --- Data Loading ---

def load_keywords(csv_path):
    """Load keyword list from a CSV file. Returns a list of keyword strings."""
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def load_text(file_path):
    """Read a text file and return its contents as a string."""
    with open(file_path, 'r') as f:
        return f.read()


# --- Matching Logic ---

def find_matches(keyword_list, text):
    """
    Return all keywords from keyword_list that appear in text.
    This is still exact string matching — Stage 2 will upgrade this.
    """
    return [kw for kw in keyword_list if kw in text]


def compare_keywords(job_keywords, resume_keywords):
    """
    Compare two lists of matched keywords using set operations.
    Returns a dict with three categories for the report.
    """
    job_set = set(job_keywords)
    resume_set = set(resume_keywords)

    return {
        "in_both":        list(job_set & resume_set),
        "to_add":         list(job_set - resume_set),   # in job, not resume
        "resume_only":    list(resume_set - job_set),   # in resume, not job
    }


def calculate_score(in_both, job_keywords):
    """
    Score = how many job keywords are covered by the resume.
    Also returns how many more keywords are needed to hit 70%.
    """
    total = len(job_keywords)
    matched = len(in_both)
    score = (matched / total * 100) if total > 0 else 0
    needed_for_70 = max(0, (total * 0.7) - matched)
    return score, needed_for_70


# --- Report Writing ---

def write_section(file, label, keyword_list):
    """Write a single labeled section to an already-open file."""
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

        write_section(f, "Keywords to Add to Resume (in Job Description, not Resume)", results["to_add"])
        write_section(f, "Keywords in Both Job Description and Resume", results["in_both"])
        write_section(f, "Keywords in Resume Only", results["resume_only"])


# --- CLI Entry Point ---

def parse_args():
    """
    Define the command-line interface.
    argparse handles --flags, help text, and error messages automatically.
    """
    parser = argparse.ArgumentParser(description="Keyword match your resume to a job description.")

    # Required arguments — no defaults, must be passed in
    parser.add_argument("--job",      required=True,  help="Path to the job description .txt file")
    parser.add_argument("--resume",   required=True,  help="Path to your resume .txt file")

    # Optional arguments — sensible defaults so existing files still work
    parser.add_argument("--keywords", default="unique_keyword_list.csv", help="Path to keyword CSV")
    parser.add_argument("--output",   default="Report.txt",              help="Output report filename")

    return parser.parse_args()


def main():
    args = parse_args()

    # Load all inputs
    keyword_list  = load_keywords(args.keywords)
    job_text      = load_text(args.job)
    resume_text   = load_text(args.resume)

    # Run the matching and comparison
    job_keywords    = find_matches(keyword_list, job_text)
    resume_keywords = find_matches(keyword_list, resume_text)
    results         = compare_keywords(job_keywords, resume_keywords)

    # Score and report
    score, needed = calculate_score(results["in_both"], job_keywords)
    write_report(args.output, score, needed, results)

    # Confirm to the user in the terminal
    print(f"Report written to: {args.output}")
    print(f"Score: {score:.1f}% | Need {needed:.0f} more to hit 70%")


if __name__ == "__main__":
    main()
