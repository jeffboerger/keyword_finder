# Changelog — Resume Keyword Analyzer

All notable changes to this project are documented here.

---

## [2.1.0] — July 2026

### Added
- **Weighted scoring** (from Planned) — keywords weighted by category importance;
  core data-engineering tools count 3x a soft skill. Shown alongside the simple
  score in both the app and CLI reports.
- **Test suite** — pytest coverage for matching behavior (word boundaries,
  plural tolerance, BOM/header handling, scoring).
- Corpus additions from two JD-harvest triage passes (data analyst, dashboard,
  workflow, scalable, insight, actionable insight, trends, efficiency, finance,
  problem-solving).

### Changed
- **Matching engine rewritten**: word-boundary regex with plural tolerance is
  now the primary matcher; fuzzy matching (RapidFuzz, punctuation-normalized)
  is a fallback for long multi-word phrases only. "java" no longer matches
  "javascript"; "sql" no longer matches "postgresql".
- CLI default keyword source is now the three data/*.csv corpus files
  (previous default pointed at a file that no longer exists — first-run
  CLI usage produced 0% scores).
- Keyword loading uses utf-8-sig (fixes BOM residue on the first keyword).
- requirements.txt trimmed from a full pip freeze to actual dependencies;
  thefuzz replaced with direct rapidfuzz.
- URL scraping strips script/style/nav/header/footer before text extraction.

### Removed
- Role selector checkboxes in the app — they were never wired to keyword
  loading, and the role-specific CSVs they implied don't exist. May return
  backed by per-role keyword subsets.

### Fixed
- Uploaded resume temp files are now deleted after parsing.
- Exclusion set no longer rebuilt on every loop iteration.

---

## [2.0.0] — April 2026

### Added
- **Highlighted Job Description view** — JD now renders with color-coded highlights after analysis
  - 🟢 Green = keyword found in both JD and resume (you have it)
  - 🟡 Yellow = keyword found in JD but missing from resume (add this)
- **N-gram matching in highlighter** — checks trigrams, then bigrams, then single words before highlighting, so multi-word phrases like "data analytics" and "attention to detail" highlight as a single unit
- **New comprehensive keyword files** replacing old flat lists:
  - `data_jobs_keywords.csv` — 717 keywords across all data roles with categories
  - `soft_skills_keywords.csv` — 140 soft skill keywords with categories
  - `industry_keywords.csv` — 346 industry-specific keywords (fintech, healthcare, retail, supply chain, GenAI)
- **Keyword documentation** — `keyword_documentation.md` describing methodology, sources, and scoring recommendations
- **PDF resume support** — upload .pdf resumes via pdfplumber
- **Word document resume support** — upload .docx resumes via python-docx

### Changed
- Keyword loading now uses three comprehensive categorized files instead of flat role-specific lists
- `load_keywords()` now skips header rows automatically and handles multi-column CSV formats
- Highlighting preserves original JD formatting including line breaks and paragraph structure

### Fixed
- `load_keywords()` was including the header row "keyword" as a keyword — fixed with header detection
- Single-word highlighting was matching partial phrases incorrectly — fixed with n-gram priority order

---

## [1.2.0] — Early 2026

### Added
- URL scraping support — paste a job posting URL instead of text via Requests and BeautifulSoup4
- `.docx` and `.pdf` resume upload support
- Role selector checkboxes — Data Engineer, Data Analyst, Software Engineer
- Gap analysis — shows how many keywords needed to reach 70% match threshold

### Changed
- Streamlit UI redesigned with role selector, file uploader, and structured results display
- Score display updated with metric cards

---

## [1.1.0] — Late 2024

### Added
- Fuzzy string matching via thefuzz/RapidFuzz — catches keyword variations with 90% threshold
- Exact matching for short keywords (3 chars or less)
- Exclusion list for noise words (or, bi, gui, etc.)
- `calculate_score()` returns both percentage and keywords needed to reach 70%
- `write_report()` outputs full gap analysis to text file

### Changed
- Refactored from single script to modular functions with single responsibility
- Added argparse CLI — `--job`, `--url`, `--resume`, `--keywords`, `--output` flags

---

## [1.0.0] — Mid 2024

### Initial Release
- Basic keyword matching against a flat CSV keyword list
- Resume and job description loaded from text files
- Score calculated as percentage of job keywords found in resume
- Report written to text file
- Inspired by *What Color Is Your Parachute* — match your language to employer language

---

## Planned

- **Click-to-dismiss false positives** — remove fuzzy matched keywords that don't actually apply, recalculate score dynamically
- **Two-column view** — JD highlighted on left, matching resume bullet on right
- **Employer Mode** — upload multiple resumes, rank all candidates against a JD, export to CSV
