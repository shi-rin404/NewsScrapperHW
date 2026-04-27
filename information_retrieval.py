import json
import os
from config import OUTPUT_DIR


def load_all_articles():
    articles = []

    if not os.path.exists(OUTPUT_DIR):
        print(f"A pasta de dados não existe: {OUTPUT_DIR}")
        return articles

    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json"):
            path = os.path.join(OUTPUT_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)

            engine_name = filename.replace(".json", "")

            for run in history:
                scraped_at = run.get("scraped_at", "")

                for article in run.get("articles", []):
                    article["engine"] = engine_name
                    article["scraped_at"] = scraped_at
                    articles.append(article)

    return articles


def search_articles(query, limit=10):
    query = query.lower().strip()
    articles = load_all_articles()
    results = []

    print(f"\nTotal de artigos carregados: {len(articles)}")

    for article in articles:
        title = article.get("title", "").lower()
        content = article.get("content", "").lower()
        summary = article.get("summary", "").lower()
        url = article.get("url", "").lower()

        if query == "all":
            results.append(article)
        elif query in title or query in content or query in summary or query in url:
            results.append(article)

    return results[:limit]


def print_results(results):
    if not results:
        print("No results found.")
        return

    print(f"Resultados apresentados: {len(results)}")

    for i, article in enumerate(results, start=1):
        title = article.get("title") or article.get("headline") or article.get("url") or "Sem título"

        print(f"\n{'='*40}")
        print(f"Artigo {i}")
        print(f"Título: {title}")
        print(f"Fonte: {article.get('engine', 'Unknown')}")
        print(f"Data: {article.get('scraped_at', 'Unknown')}")
        print(f"Link: {article.get('url', 'No URL')}")


if __name__ == "__main__":
    query = input("Search query: ")
    results = search_articles(query)
    print_results(results)