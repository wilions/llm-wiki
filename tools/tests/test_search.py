"""Tests for wiki search CLI."""
import os
import tempfile
from pathlib import Path

import pytest

# Adjust import path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from search import search_wiki, rank_results, format_result


@pytest.fixture
def wiki_dir(tmp_path):
    """Create a minimal wiki tree for testing."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()

    (wiki / "concepts").mkdir()
    (wiki / "entities").mkdir()

    (wiki / "concepts" / "solidification.md").write_text(
        "---\ntitle: Solidification\ntags: [solidification]\n---\n"
        "# Solidification\nColumnar grain growth occurs in Ti64.\n"
        "The columnar-to-equiaxed transition (CET) is important.\n"
    )
    (wiki / "concepts" / "microstructure.md").write_text(
        "---\ntitle: Microstructure\ntags: [microstructure]\n---\n"
        "# Microstructure\nAlpha prime martensite forms in Ti64 during L-PBF.\n"
    )
    (wiki / "entities" / "alloy-systems.md").write_text(
        "---\ntitle: Alloy Systems\ntags: [alloys]\n---\n"
        "# Alloy Systems\nTi64 is the most common AM alloy.\n"
    )
    return wiki


def test_search_finds_matching_files(wiki_dir):
    results = search_wiki("Ti64", wiki_dir)
    paths = [r["path"] for r in results]
    assert any("solidification" in p for p in paths)
    assert any("microstructure" in p for p in paths)
    assert any("alloy-systems" in p for p in paths)


def test_search_no_match_returns_empty(wiki_dir):
    results = search_wiki("nonexistent_term_xyz", wiki_dir)
    assert results == []


def test_rank_results_orders_by_score_descending():
    results = [
        {"path": "a.md", "score": 1, "snippet": ""},
        {"path": "b.md", "score": 5, "snippet": ""},
        {"path": "c.md", "score": 3, "snippet": ""},
    ]
    ranked = rank_results(results)
    assert ranked[0]["score"] == 5
    assert ranked[1]["score"] == 3
    assert ranked[2]["score"] == 1


def test_search_case_insensitive(wiki_dir):
    results_lower = search_wiki("ti64", wiki_dir)
    results_upper = search_wiki("Ti64", wiki_dir)
    assert len(results_lower) == len(results_upper)


def test_format_result_includes_path_and_snippet():
    result = {"path": "wiki/concepts/solidification.md", "score": 3, "snippet": "columnar grain growth"}
    formatted = format_result(result)
    assert "solidification.md" in formatted
    assert "columnar grain growth" in formatted
    assert "3" in formatted


def test_search_returns_snippet(wiki_dir):
    results = search_wiki("columnar", wiki_dir)
    assert len(results) >= 1
    assert results[0]["snippet"] != ""
