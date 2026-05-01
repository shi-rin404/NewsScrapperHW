"""Redis indexing utilities for normalized news articles."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from redis import Redis


class NewsRedisIndexer:
    def __init__(self, url: str = "redis://localhost:6379/0", key_prefix: str = "news_articles"):
        self.client = Redis.from_url(url, decode_responses=True)
        self.key_prefix = key_prefix
        self.index_key = f"{key_prefix}:ids"

    def create_index(self) -> None:
        # A dedicated Redis Set keeps track of stored document ids.
        self.client.sadd(self.index_key, *[])

    def index_articles(self, articles: list[dict]) -> int:
        if not articles:
            return 0

        now = datetime.now(timezone.utc).isoformat()
        indexed_count = 0

        with self.client.pipeline(transaction=False) as pipe:
            for item in articles:
                item_id = item["id"]
                doc_key = f"{self.key_prefix}:doc:{item_id}"
                doc = {
                    "id": item_id,
                    "source": item["source"],
                    "url": item["url"],
                    "text": item["text"],
                    "scraped_at": item["scraped_at"],
                    "run_index": item["run_index"],
                    "article_index": item["article_index"],
                    "indexed_at": now,
                }
                pipe.set(doc_key, json.dumps(doc, ensure_ascii=False))
                pipe.sadd(self.index_key, item_id)
                indexed_count += 1
            pipe.execute()

        return indexed_count

    def count_documents(self) -> int:
        return int(self.client.scard(self.index_key))

    def verify_sample(self, limit: int = 5) -> list[dict]:
        ids = list(self.client.smembers(self.index_key))
        if not ids:
            return []

        docs: list[dict] = []
        for item_id in ids[:limit]:
            raw_doc = self.client.get(f"{self.key_prefix}:doc:{item_id}")
            if not raw_doc:
                continue
            docs.append(json.loads(raw_doc))
        return docs
