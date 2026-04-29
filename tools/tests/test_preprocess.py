"""Tests for tools/preprocess.py — all offline, no markitdown required."""
import sys
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from preprocess import _slug_from_url, preprocess, SUPPORTED_EXTENSIONS


# ---------------------------------------------------------------------------
# _slug_from_url
# ---------------------------------------------------------------------------

class TestSlugFromUrl:
    def test_youtube(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        slug = _slug_from_url(url)
        assert "youtube" in slug
        assert len(slug) <= 100

    def test_simple_url(self):
        slug = _slug_from_url("https://example.com/paper/2025")
        assert "example" in slug
        assert "/" not in slug

    def test_no_double_dashes(self):
        slug = _slug_from_url("https://a.b.c/d/e/f")
        assert "--" not in slug

    def test_max_length(self):
        long_url = "https://example.com/" + "a" * 200
        assert len(_slug_from_url(long_url)) <= 100

    def test_empty_path(self):
        slug = _slug_from_url("https://example.com")
        assert len(slug) > 0


# ---------------------------------------------------------------------------
# SUPPORTED_EXTENSIONS
# ---------------------------------------------------------------------------

class TestSupportedExtensions:
    def test_documents(self):
        for ext in [".pdf", ".docx", ".pptx", ".xlsx", ".epub", ".csv"]:
            assert ext in SUPPORTED_EXTENSIONS

    def test_images(self):
        for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            assert ext in SUPPORTED_EXTENSIONS

    def test_audio(self):
        for ext in [".wav", ".mp3"]:
            assert ext in SUPPORTED_EXTENSIONS

    def test_passthrough(self):
        for ext in [".md", ".txt"]:
            assert ext in SUPPORTED_EXTENSIONS


# ---------------------------------------------------------------------------
# preprocess() — mocked markitdown
# ---------------------------------------------------------------------------

class TestPreprocess:
    def _make_mock_md(self, text="# Converted content\n\nSome text."):
        mock_result = MagicMock()
        mock_result.text_content = text
        mock_md_instance = MagicMock()
        mock_md_instance.convert.return_value = mock_result
        mock_md_class = MagicMock(return_value=mock_md_instance)
        return mock_md_class, mock_md_instance

    def test_pdf_conversion(self, tmp_path):
        fake_pdf = tmp_path / "paper.pdf"
        fake_pdf.write_bytes(b"%PDF-fake")

        mock_md_class, mock_md_instance = self._make_mock_md("# Paper\n\nContent here.")

        with patch.dict("sys.modules", {"markitdown": MagicMock(MarkItDown=mock_md_class)}):
            out = preprocess(str(fake_pdf), str(tmp_path))

        assert out.endswith("paper.md")
        assert Path(out).read_text() == "# Paper\n\nContent here."
        mock_md_instance.convert.assert_called_once_with(str(fake_pdf))

    def test_docx_conversion(self, tmp_path):
        fake_docx = tmp_path / "report.docx"
        fake_docx.write_bytes(b"PK fake docx")

        mock_md_class, _ = self._make_mock_md("# Report")

        with patch.dict("sys.modules", {"markitdown": MagicMock(MarkItDown=mock_md_class)}):
            out = preprocess(str(fake_docx), str(tmp_path))

        assert out.endswith("report.md")

    def test_url_conversion(self, tmp_path):
        url = "https://example.com/article"
        mock_md_class, mock_md_instance = self._make_mock_md("# Article\n\nWeb content.")

        with patch.dict("sys.modules", {"markitdown": MagicMock(MarkItDown=mock_md_class)}):
            out = preprocess(url, str(tmp_path))

        assert out.endswith(".md")
        assert "example" in Path(out).name
        mock_md_instance.convert.assert_called_once_with(url)

    def test_markdown_passthrough(self, tmp_path):
        src = tmp_path / "notes.md"
        src.write_text("# Notes\n\nAlready markdown.", encoding="utf-8")

        with patch.dict("sys.modules", {"markitdown": MagicMock()}):
            out = preprocess(str(src), str(tmp_path))

        assert out.endswith("notes.md")
        assert Path(out).read_text() == "# Notes\n\nAlready markdown."

    def test_txt_passthrough(self, tmp_path):
        src = tmp_path / "abstract.txt"
        src.write_text("Plain text content.", encoding="utf-8")

        with patch.dict("sys.modules", {"markitdown": MagicMock()}):
            out = preprocess(str(src), str(tmp_path))

        assert Path(out).read_text() == "Plain text content."

    def test_output_dir_created(self, tmp_path):
        fake_pdf = tmp_path / "paper.pdf"
        fake_pdf.write_bytes(b"%PDF")
        new_dir = tmp_path / "subdir" / "raw"

        mock_md_class, _ = self._make_mock_md("content")

        with patch.dict("sys.modules", {"markitdown": MagicMock(MarkItDown=mock_md_class)}):
            preprocess(str(fake_pdf), str(new_dir))

        assert new_dir.exists()

    def test_missing_markitdown_exits(self, tmp_path):
        fake_pdf = tmp_path / "paper.pdf"
        fake_pdf.write_bytes(b"%PDF")

        with patch.dict("sys.modules", {"markitdown": None}):
            with pytest.raises(SystemExit):
                preprocess(str(fake_pdf), str(tmp_path))

    def test_image_with_llm_client(self, tmp_path):
        fake_img = tmp_path / "figure.png"
        fake_img.write_bytes(b"\x89PNG fake")

        mock_md_class, mock_md_instance = self._make_mock_md("Figure shows a bar chart.")
        mock_client = MagicMock()

        with patch.dict("sys.modules", {"markitdown": MagicMock(MarkItDown=mock_md_class)}):
            out = preprocess(str(fake_img), str(tmp_path), llm_client=mock_client, llm_model="claude-sonnet-4-6")

        # MarkItDown should have been constructed with llm_client
        call_kwargs = mock_md_class.call_args.kwargs
        assert call_kwargs.get("llm_client") is mock_client
        assert call_kwargs.get("llm_model") == "claude-sonnet-4-6"
        assert Path(out).read_text() == "Figure shows a bar chart."
