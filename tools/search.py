#!/usr/bin/env python3
"""
Wiki search CLI.

Usage:
    python tools/search.py <query> [wiki_dir]
    python tools/search.py "Ti64 fatigue"
    python tools/search.py "solidification" wiki/

Ranks pages by match count, prints top results with snippets.
"""
import re
import sys
from pathlib import Path


def search_wiki(query: str, wiki_dir: Path) -> list[dict]:
    """
    Search all .md files in wiki_dir for query (case-insensitive).
    Returns list of dicts: {path, score, snippet}.
    """
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []

    for md_file in Path(wiki_dir).rglob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        matches = pattern.findall(text)
        if not matches:
            continue

        # Find first matching line for snippet
        snippet = ""
        for line in text.splitlines():
            if pattern.search(line):
                snippet = line.strip()[:120]
                break

        results.append({
            "path": str(md_file),
            "score": len(matches),
            "snippet": snippet,
        })

    return rank_results(results)


def rank_results(results: list[dict]) -> list[dict]:
    """Sort results by score descending."""
    return sorted(results, key=lambda r: r["score"], reverse=True)


def format_result(result: dict) -> str:
    """Format a single result for CLI output."""
    path = result["path"]
    score = result["score"]
    snippet = result["snippet"]
    return f"[{score}] {path}\n    {snippet}"


def main():
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [wiki_dir]", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    wiki_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("wiki")

    if not wiki_dir.exists():
        print(f"Error: wiki directory not found: {wiki_dir}", file=sys.stderr)
        sys.exit(1)

    results = search_wiki(query, wiki_dir)

    if not results:
        print(f"No results for: {query!r}")
        return

    print(f"Results for {query!r} ({len(results)} pages):\n")
    for result in results[:10]:  # top 10
        print(format_result(result))
        print()


if __name__ == "__main__":
    main()
