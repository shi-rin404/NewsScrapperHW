# Source
## AI Model
Codex 5.3

## Used Prompts
### Run and Test Request
How can I run and test this?

### Dependency Installation Error
I ran `pip install -r requirements.txt` and got a `greenlet` build error.

### Runtime Requirement Clarification
If I run `main.py`, data will be generated automatically. I need to install the required dependencies for that.

### Python Environment Problem
`ModuleNotFoundError: No module named 'schedule'`
`No suitable Python runtime found`

### Student 2 Next Step Request
The `data` folder is now created automatically. What should I do next for Student 2?

### Docker Engine Error
`failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`

### Elasticsearch Verification Output
`python student2_demo.py`
`Loaded article count: 247`
`Indexed article count: 247`
`Elasticsearch document count: 247`

### Student 2 Requirements File Request
Please create a dedicated requirements file for Student 2.

## Student 2 Specification (from Yapılacaklar.md)
### Goal
Load JSON outputs produced by the scraper, normalize them into a flat record structure, print 5 sample records, and index articles into Elasticsearch for scalable search and storage.

### Required New Files
- `processing/__init__.py`
- `processing/article_loader.py`
- `indexing/__init__.py`
- `indexing/elasticsearch_indexer.py`
- `student2_demo.py`
- `.env.example`

### Required Functions in `processing/article_loader.py`
- `load_articles_from_file(path: str) -> list[dict]`
- `load_all_articles(data_dir: str = "data") -> list[dict]`
- `print_sample_records(records: list[dict], limit: int = 5) -> None`

### Normalized Article Schema
```python
{
    "id": "deterministic_unique_id",
    "source": "bundle_gundem",
    "text": "news title or content",
    "url": "https://...",
    "scraped_at": "2026-04-23T13:00:00",
    "run_index": 0,
    "article_index": 0
}
```

### Data Handling Rules
- Generate deterministic `id` from `source + url + text + scraped_at` (SHA-1).
- If `data` directory is missing, raise a clear error.
- If JSON is invalid, report which file failed without crashing the entire process.
- Skip runs with missing/invalid `articles`.
- Skip entries with empty `text` or `url`.
- Print first 5 records when available.

### Required Class in `indexing/elasticsearch_indexer.py`
- `class NewsElasticsearchIndexer`
  - `__init__(url: str = "http://localhost:9200", index_name: str = "news_articles")`
  - `create_index() -> None`
  - `index_articles(articles: list[dict]) -> int`
  - `count_documents() -> int`
  - `verify_sample(limit: int = 5) -> list[dict]`

### Elasticsearch Index and Mapping
- Index name: `news_articles`
- Fields:
  - `source` (`keyword`)
  - `url` (`keyword`)
  - `text` (`text`)
  - `scraped_at` (`date`)
  - `run_index` (`integer`)
  - `article_index` (`integer`)
  - `indexed_at` (`date`)

### Demo Flow (`student2_demo.py`)
1. Load JSON files from `data`.
2. Print total loaded article count.
3. Print 5 sample records.
4. Create Elasticsearch index.
5. Bulk index article records.
6. Compare loaded count and Elasticsearch document count.
7. Print 5 indexed sample documents.

### Acceptance Criteria
- `python student2_demo.py` runs without unhandled errors.
- `data/*.json` is loaded successfully.
- At least 5 sample records are printed.
- `news_articles` index is created.
- Articles are indexed into Elasticsearch.
- Re-running does not create duplicate documents.
- Loaded count and Elasticsearch count are consistent.

## Student 2 Deliverables
- Added `processing/article_loader.py`
- Added `indexing/elasticsearch_indexer.py`
- Added `student2_demo.py`
- Added `.env.example`
- Added `requirements.student2.txt`
- Updated `requirements.txt` with `elasticsearch>=8,<9` and `python-dotenv`
- Added refresh wait in bulk indexing for consistent Elasticsearch document counts
