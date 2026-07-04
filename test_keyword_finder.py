"""Matching-behavior tests — run with: pytest"""
import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from keyword_finder import (load_keywords, find_matches, calculate_score,
                            calculate_weighted_score, compare_keywords)


def test_java_does_not_match_javascript():
    assert find_matches(["java"], "We use JavaScript everywhere") == []

def test_java_matches_java():
    assert find_matches(["java"], "Experience with Java required") == ["java"]

def test_sql_does_not_match_postgresql_only():
    assert find_matches(["sql"], "We run PostgreSQL") == []

def test_sql_matches_standalone():
    assert "sql" in find_matches(["sql"], "Strong SQL skills and PostgreSQL")

def test_plural_tolerance():
    assert find_matches(["reconciliation"], "monthly commission reconciliations") == ["reconciliation"]
    assert find_matches(["dashboard"], "build dashboards in Tableau") == ["dashboard"]

def test_excluded_noise_words():
    assert find_matches(["or", "bi"], "or bi tools") == []

def test_multiword_fuzzy_fallback():
    # long multi-word phrase with punctuation variance still matches
    assert find_matches(["extract transform load"],
                        "experience with extract, transform, load processes") != []

def test_bom_and_header_handling():
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                     encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "category"])
        w.writerow([".net", "programming languages"])
        w.writerow(["python", "programming languages"])
        path = f.name
    kws = load_keywords(path)
    assert kws == [".net", "python"]          # no BOM residue, no header

def test_scores():
    job = ["python", "sql", "airflow", "communication skills"]
    both = ["python", "sql"]
    score, needed = calculate_score(job, both)
    assert round(score, 1) == 50.0
    cats = {"python": "programming languages", "sql": "programming languages",
            "airflow": "orchestration tools", "communication skills": "core soft skills"}
    weighted = calculate_weighted_score(job, both, cats)
    # matched 2+2=4 of total 2+2+3+1=8 -> 50%; airflow miss hurts more than soft-skill miss
    assert round(weighted, 1) == 50.0
    weighted2 = calculate_weighted_score(job, ["python", "sql", "airflow"], cats)
    assert weighted2 > 80                      # covering airflow jumps the weighted score

def test_compare_keywords():
    r = compare_keywords(["a", "b"], ["b", "c"])
    assert set(r["in_both"]) == {"b"} and set(r["job_only"]) == {"a"}
