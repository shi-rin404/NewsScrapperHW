"""Elasticsearch indexing utilities for normalized news articles."""

from __future__ import annotations

from datetime import datetime, timezone

from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError


class NewsElasticsearchIndexer:
    def __init__(self, url: str = "http://localhost:9200", index_name: str = "news_articles"):
        self.client = Elasticsearch(url)
        self.index_name = index_name

    def create_index(self) -> None:
        mapping = {
            "mappings": {
                "properties": {
                    "source": {"type": "keyword"},
                    "url": {"type": "keyword"},
                    "text": {"type": "text"},
                    "scraped_at": {"type": "date"},
                    "run_index": {"type": "integer"},
                    "article_index": {"type": "integer"},
                    "indexed_at": {"type": "date"},
                }
            }
        }
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name, **mapping)

    def index_articles(self, articles: list[dict]) -> int:
        if not articles:
            return 0

        now = datetime.now(timezone.utc).isoformat()
        actions = []
        for item in articles:
            doc = {
                "source": item["source"],
                "url": item["url"],
                "text": item["text"],
                "scraped_at": item["scraped_at"],
                "run_index": item["run_index"],
                "article_index": item["article_index"],
                "indexed_at": now,
            }
            actions.append(
                {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "_id": item["id"],
                    "_source": doc,
                }
            )

        try:
            success, _ = helpers.bulk(
                self.client,
                actions,
                raise_on_error=False,
                refresh="wait_for",
            )
            return success
        except BulkIndexError as exc:
            first_error = exc.errors[0] if exc.errors else {}
            raise RuntimeError(f"Bulk indexing failed. First error: {first_error}") from exc

    def count_documents(self) -> int:
        response = self.client.count(index=self.index_name)
        return int(response.get("count", 0))

    def verify_sample(self, limit: int = 5) -> list[dict]:
        response = self.client.search(
            index=self.index_name,
            size=limit,
            sort=[{"indexed_at": {"order": "desc"}}],
            query={"match_all": {}},
        )
        hits = response.get("hits", {}).get("hits", [])
        return [{"id": hit.get("_id"), **hit.get("_source", {})} for hit in hits]
