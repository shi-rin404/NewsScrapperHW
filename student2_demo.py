"""Student 2 demo: load, inspect, and index scraped news records."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from indexing.redis_indexer import NewsRedisIndexer
from processing.article_loader import load_all_articles, print_sample_records


def main() -> None:
    load_dotenv()
    data_dir = os.getenv("DATA_DIR", "data")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    index_name = os.getenv("REDIS_KEY_PREFIX", "news_articles")

    try:
        articles = load_all_articles(data_dir)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return

    print(f"Loaded article count: {len(articles)}")
    print_sample_records(articles, limit=5)

    try:
        indexer = NewsRedisIndexer(url=redis_url, key_prefix=index_name)
        indexer.create_index()
        indexed_count = indexer.index_articles(articles)

        print(f"Indexed article count: {indexed_count}")
        print(f"Redis document count: {indexer.count_documents()}")

        for item in indexer.verify_sample(limit=5):
            print(item)
    except Exception as exc:
        print(f"[ERROR] Redis operation failed: {exc}")


if __name__ == "__main__":
    main()
