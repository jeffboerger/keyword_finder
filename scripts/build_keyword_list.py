import requests
import csv
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
from googlesearch import search


nltk.download('stopwords')

# Entry Level DE Job Posting URLs
JOB_URLS = [
    "https://jobs.ashbyhq.com/ramp/e577622f-6657-4e53-8941-b3a774b04448",
    "https://boards.greenhouse.io/snowflake/jobs/7696018002",
    "https://boards.greenhouse.io/databricks/jobs/6865870002",
    "https://jobs.lever.co/dbt-labs",
    "https://boards.greenhouse.io/fivetran",
]
# Keywords to always include regardless of frequency
DE_CORE_KEYWORDS = [
    'python', 'sql', 'snowflake', 'dbt', 'airflow', 'redshift', 'bigquery', 
    'spark', 'kafka', 'databricks', 'fivetran', 'airbyte', 'docker', 
    'kubernetes', 'terraform', 'parquet', 'delta lake', 'data lakehouse', 
    'elt', 'etl', 'data pipeline', 'data modeling', 'schema design', 
    'orchestration', 'ci/cd', 'bash', 'scala', 'prefect', 'dagster',
    'git', 'linux', 'aws', 'azure', 'gcp', 'pandas', 'pyspark',
    'data warehouse', 'data lake', 'data quality', 'data governance'
]

def scrape_text(url):
    """Fetch and extract text from a job posting URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove navigation, headers, footers, scripts
        for tag in soup(['nav', 'header', 'footer', 'script', 
                        'style', 'aside', 'form']):
            tag.decompose()
        
        # Only grab paragraph and list content
        content = []
        for tag in soup.find_all(['p', 'li', 'h1', 'h2', 'h3']):
            content.append(tag.get_text(separator=' ', strip=True))
        
        return ' '.join(content).lower()
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""
    
def extract_keywords(text):
    """Extract meaningful words from text, filtering out stop words."""
    stop_words = set(stopwords.words('english'))
    
    # Add custom noise words common on job posting pages
    web_noise = {
        'june', 'july', 'august', 'january', 'february', 'march', 'april',
        'may', 'september', 'october', 'november', 'december',
        'francisco', 'york', 'login', 'skip', 'page', 'click', 'view',
        'read', 'find', 'learn', 'join', 'open', 'free', 'best', 'make',
        'take', 'want', 'need', 'work', 'time', 'days', 'week', 'month',
        'year', 'don', 'miss', 'blog', 'news', 'press', 'summit', 'tour',
        'demo', 'podcast', 'spotlight', 'featured', 'latest', 'biggest',
        'current', 'drive', 'move', 'share', 'world', 'life', 'thing',
        'right', 'start', 'offer', 'pride', 'trust', 'space', 'center',
        'promote', 'connect', 'access', 'create', 'discover', 'explore',
        'overview', 'edition', 'partners', 'ventures', 'alliance', 'agents',
        'parents', 'providers', 'champions', 'communities', 'announcements'
    }
    
    stop_words.update(web_noise)

    words = text.split()
    cleaned = []
    for word in words:
        word = word.strip('.,;:()[]{}"\'-')
        if len(word) > 3 and word not in stop_words:
            cleaned.append(word)
    return cleaned


def scrape_all_jobs(urls):
    """Scrape all job URLs and return combined word frequency."""
    all_words = []
    for i, url in enumerate(urls):
        print(f"Scraping {i+1}/{len(urls)}: {url}")
        text = scrape_text(url)
        if text:
            words = extract_keywords(text)
            all_words.extend(words)
    return Counter(all_words)


def find_job_urls(queries, num_results=5):
    """Search Google for job postings and return URLs."""
    urls = []
    for query in queries:
        print(f"Searching: {query}")
        try:
            results = search(query, num_results=num_results, sleep_interval=2)
            urls.extend(results)
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
    return list(set(urls))


def build_keyword_list(urls, output_csv, top_n=200, existing_csv=None):
    """
    Scrape job postings, extract frequent keywords,
    merge with core DE keywords, save to CSV.
    """
    # Scrape all job postings
    frequency = scrape_all_jobs(urls)

    # Get top N most frequent words
    top_words = [word for word, count in frequency.most_common(top_n)]

    # Load existing keywords only if provided
    existing = []
    if existing_csv:
        with open(existing_csv, newline='') as f:
            reader = csv.reader(f)
            existing = [row[0].lower() for row in reader]

    # Combine scraped keywords with core DE keywords only
    combined = set(top_words + DE_CORE_KEYWORDS + existing)

    # Save to new CSV
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        for keyword in sorted(combined):
            writer.writerow([keyword])

    print(f"Saved {len(combined)} keywords to {output_csv}")



if __name__ == '__main__':
    build_keyword_list(
        urls=JOB_URLS,
        # existing_csv='data/unique_lower_keyword_list.csv',
        output_csv='data/de_keyword_list.csv',
        top_n=200
    )