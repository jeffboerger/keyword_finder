# Data Jobs Keyword List — Methodology & Documentation

**Version:** 1.0  
**Last Updated:** April 2026  
**Author:** Research compiled via systematic web research across 50+ sources  

---

## Overview

This documentation covers three CSV files produced for a resume keyword analyzer targeting data engineering, data analytics, data science, and related roles:

| File | Keywords | Description |
|---|---|---|
| `data_jobs_keywords.csv` | 580 | Core technical keywords across all data roles |
| `industry_keywords.csv` | 346 | Industry-specific keywords for fintech, healthcare, retail, supply chain, and GenAI |
| `soft_skills_keywords.csv` | 140 | Soft skills and interpersonal keywords |

**Total unique keywords: ~1,066**

---

## Research Methodology

### Sources Consulted

Keywords were sourced from the following types of materials, all published between 2023–2026:

**Job boards (live postings):**
- Indeed.com (data engineer, data analyst, data scientist, BI analyst, MLOps, data governance postings)
- LinkedIn Jobs (multiple role types)
- Glassdoor (fintech, healthcare, supply chain data roles)
- Dice.com (technical roles, governance specialists)
- Built In (fintech, NYC/Chicago/remote markets)
- Robert Half (contract and FTE data roles)
- ZipRecruiter (supply chain, ecommerce, healthcare)

**Industry research and surveys:**
- 365 Data Science 2024 & 2025 Job Outlook Reports (quantified % mention rates per skill)
- Kaggle State of Data Science 2024 Survey
- LinkedIn 2024 Global Talent Trends Report
- ResumeAdapter ATS keyword analysis (60+ data role keywords)
- Brickset / TealHQ skills databases (role-specific skill frequency analysis)

**Role-specific deep dives:**
- Data Engineering: AWS, Azure, GCP documentation; Databricks blog; dbt Community
- Data Science: Towards Data Science; Boston Institute of Analytics; GeeksforGeeks
- MLOps: Adaface, DevsData, Qubit Labs job description templates
- Data Governance: DAMA-DMBOK frameworks; Collibra, Alation product documentation
- Healthcare: Dice.com HL7/FHIR specialist postings; PMC healthcare informatics study (2024)
- Fintech: Built In fintech listings; CFTE Fintech Job Report
- Supply Chain: Glassdoor, ZipRecruiter, NCSU Supply Chain Resource Cooperative

---

## Selection Criteria

### Inclusion Rules

A keyword was included if it met **at least one** of the following criteria:

1. **High frequency** — Appeared in ≥10% of job postings for at least one role type (DE, DA, DS, MLOps, or BI), based on the 365 Data Science quantitative analysis or equivalent survey data.

2. **Role-defining tool or technology** — A specific named tool, platform, language, or framework that employers list as a required or preferred skill. Examples: `dbt`, `apache iceberg`, `kubeflow`, `collibra`.

3. **Conceptual keyword** — A methodology, process, or architectural pattern that ATS systems are known to scan for. Examples: `medallion architecture`, `change data capture`, `data mesh`.

4. **Emerging industry standard (2023–2026)** — New-to-market tools or concepts appearing in ≥3 distinct job postings in the research window. Examples: `rag`, `vector database`, `lora`, `data contracts`.

5. **Industry-specific term** — Terminology specific to fintech, healthcare, retail/ecommerce, or supply chain that appears in ≥5 industry-specific postings. Examples: `fhir`, `hl7`, `cdc (change data capture)`, `roas`.

### Exclusion Rules

A keyword was **excluded** if it met any of the following:

- Generic workplace terms with no data-specific meaning (e.g., "teamwork" was moved to the separate soft skills file, not the technical file)
- Trademarked product names unlikely to appear in ATS scanning (e.g., specific vendor product SKUs)
- Role titles themselves (e.g., "data engineer" is not a keyword — it's the job title)
- Extremely rare or niche certifications with negligible market penetration
- Duplicate meaning terms where one canonical form was already included

---

## File Structures

### data_jobs_keywords.csv
```
keyword,category
python,programming languages
sql,programming languages
...
```
**Columns:**
- `keyword` — lowercase keyword string, as it should appear in ATS scanning
- `category` — grouping label for scoring or filtering (e.g., "programming languages", "cloud platforms", "mlops", "data science")

**Categories in this file:**
- programming languages
- big data frameworks
- cloud platforms
- cloud data platforms
- cloud services
- orchestration tools
- transformation tools
- etl tools
- concepts
- databases
- visualization tools
- python libraries
- r packages
- data science
- mlops
- data governance
- data engineering
- soft skills (moved to separate file in v1.1)
- analytics
- advanced concepts
- certifications
- education

---

### industry_keywords.csv
```
keyword,category,industry
credit risk,financial services,fintech
ehr,healthcare,healthcare
...
```
**Columns:**
- `keyword` — lowercase keyword string
- `category` — subcategory within the industry
- `industry` — top-level industry vertical (fintech, healthcare, retail & ecommerce, supply chain & manufacturing, genai & llm)

**Industries covered:**
- **Fintech** (56 keywords): Credit/risk, trading, payments, regulatory compliance, financial modeling
- **Healthcare** (63 keywords): Clinical standards (HL7, FHIR, ICD-10), EHR/EMR systems, health informatics, compliance
- **Retail & Ecommerce** (57 keywords): Digital analytics, attribution, merchandising, customer analytics
- **Supply Chain & Manufacturing** (57 keywords): ERP/SAP, IoT/sensors, logistics, operations research, quality
- **GenAI & LLM** (84 keywords): RAG, vector databases, fine-tuning, LLM frameworks, AI safety

---

### soft_skills_keywords.csv
```
keyword,category,notes
communication skills,core soft skills,appears in nearly every data job posting
data storytelling,core soft skills,high-frequency term in modern data jds
...
```
**Columns:**
- `keyword` — lowercase keyword string
- `category` — soft skill grouping (core soft skills, teamwork, analytical skills, adaptability, organizational skills, leadership, business knowledge, interpersonal, work style, data skills)
- `notes` — optional context on why this keyword is included or how it's used

**Categories in this file:**
- core soft skills
- teamwork
- analytical skills
- adaptability
- organizational skills
- leadership
- business knowledge
- interpersonal
- work style
- data skills

---

## Scoring Recommendations

Since these are split into three files, here are suggested approaches for a two-score system:

### Score 1: Technical Score
Use `data_jobs_keywords.csv` + `industry_keywords.csv`

```python
# Pseudocode
technical_keywords = load_csv('data_jobs_keywords.csv') + load_csv('industry_keywords.csv')
technical_score = count_matches(resume_text, technical_keywords) / len(technical_keywords) * 100
```

Optional: weight by category. High-value categories for most roles:
- **Tier 1 (2x weight):** programming languages, cloud platforms, specific tools relevant to target role
- **Tier 2 (1.5x weight):** concepts, data science, mlops
- **Tier 3 (1x weight):** certifications, education

### Score 2: Soft Skills Score
Use `soft_skills_keywords.csv`

```python
soft_keywords = load_csv('soft_skills_keywords.csv')
soft_score = count_matches(resume_text, soft_keywords) / len(soft_keywords) * 100
```

Consider normalizing both scores to 0–100 scale for display.

---

## Known Limitations

1. **ATS variability** — Different ATS systems scan differently. Some match exact strings; others use synonym matching. This list optimizes for exact or near-exact string matches.

2. **Role specificity** — A data engineer and a data analyst have significantly different keyword profiles. A future version could produce role-specific subsets with frequency weights per role.

3. **Keyword drift** — The GenAI/LLM landscape moves fast. Keywords in the `genai & llm` category should be reviewed every 6 months. As of April 2026, RAG, vector databases, and LLM fine-tuning are solidly mainstream.

4. **Multi-word phrases** — Some keywords are multi-word (e.g., "change data capture", "customer lifetime value"). Your analyzer should handle n-gram matching, not just unigrams.

5. **Case sensitivity** — All keywords are lowercase. Ensure your analyzer normalizes resume text to lowercase before matching.

6. **Acronym handling** — Many terms have both a spelled-out form and an acronym (e.g., `hl7` vs `health level 7`, `clv` vs `customer lifetime value`). Both forms are included where known. Your analyzer should match either form and count it once.

---

## Update Log

| Version | Date | Changes |
|---|---|---|
| 1.0 | April 2026 | Initial release — 580 core + 346 industry + 140 soft skills |

---

## Data Sources Summary

| Source Type | Examples | Role Coverage |
|---|---|---|
| Live job postings (2024–2026) | Indeed, LinkedIn, Dice, Built In, Glassdoor | All roles |
| Quantitative skill frequency studies | 365 Data Science 2025 Outlook, Kaggle Survey 2024 | DE, DS, DA, ML |
| ATS keyword research | ResumeAdapter, TealHQ, CVCompiler | All roles |
| Role-specific deep dives | NCSU SCM, CFTE Fintech Report, PMC Healthcare Study | Industry-specific |
| Official tool documentation | Collibra, dbt, Apache Spark, AWS, Azure | Tools & platforms |
| Academic / research papers | ArXiv soft skills study (2024), AHIMA job analysis | DS, Healthcare |

