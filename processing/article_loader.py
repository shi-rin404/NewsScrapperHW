"""Utilities for loading and normalizing scraped JSON article data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _build_deterministic_id(source: str, url: str, text: str, scraped_at: str) -> str:
    raw = f"{source}|{url}|{text}|{scraped_at}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def load_articles_from_file(path: str) -> list[dict]:
    file_path = Path(path)
    source = file_path.stem
    records: list[dict] = []

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"JSON file not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        print(f"[WARN] Invalid JSON in file: {file_path} ({exc})")
        return []
    except OSError as exc:
        print(f"[WARN] Could not read file: {file_path} ({exc})")
        return []

    if not isinstance(payload, list):
        print(f"[WARN] Unexpected JSON root in file: {file_path}. Expected list.")
        return []

    for run_index, run_item in enumerate(payload):
        if not isinstance(run_item, dict):
            continue

        scraped_at = str(run_item.get("scraped_at", ""))
        articles = run_item.get("articles")
        if not isinstance(articles, list):
            print(f"[WARN] Missing or invalid 'articles' in file: {file_path}, run={run_index}")
            continue

        for article_index, article in enumerate(articles):
            if not isinstance(article, dict):
                continue

            text = str(article.get("text", "")).strip()
            url = str(article.get("url", "")).strip()
            if not text or not url:
                continue

            records.append(
                {
                    "id": _build_deterministic_id(source, url, text, scraped_at),
                    "source": source,
                    "text": text,
                    "url": url,
                    "scraped_at": scraped_at,
                    "run_index": run_index,
                    "article_index": article_index,
                }
            )

    return records


def load_all_articles(data_dir: str = "data") -> list[dict]:
    directory = Path(data_dir)
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Data directory not found: {directory.resolve()}")

    all_records: list[dict] = []
    for json_file in sorted(directory.glob("*.json")):
        all_records.extend(load_articles_from_file(str(json_file)))

    return all_records


def print_sample_records(records: list[dict], limit: int = 5) -> None:
    sample_count = min(limit, len(records))
    for i in range(sample_count):
        rec = records[i]
        print(
            f"Sample record {i + 1}: source={rec['source']} | "
            f"text={rec['text'][:80]} | url={rec['url']}"
        )
