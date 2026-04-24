"""Student 2 demo: load, inspect, and index scraped news records."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from indexing.elasticsearch_indexer import NewsElasticsearchIndexer
from processing.article_loader import load_all_articles, print_sample_records


def main() -> None:
    load_dotenv()
    data_dir = os.getenv("DATA_DIR", "data")
    elastic_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    index_name = os.getenv("ELASTICSEARCH_INDEX", "news_articles")

    try:
        articles = load_all_articles(data_dir)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return

    print(f"Loaded article count: {len(articles)}")
    print_sample_records(articles, limit=5)

    try:
        indexer = NewsElasticsearchIndexer(url=elastic_url, index_name=index_name)
        indexer.create_index()
        indexed_count = indexer.index_articles(articles)

        print(f"Indexed article count: {indexed_count}")
        print(f"Elasticsearch document count: {indexer.count_documents()}")

        for item in indexer.verify_sample(limit=5):
            print(item)
    except Exception as exc:
        print(f"[ERROR] Elasticsearch operation failed: {exc}")


if __name__ == "__main__":
    main()
