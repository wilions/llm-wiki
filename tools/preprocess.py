#!/usr/bin/env python3
"""
Wiki source preprocessor — converts any file format to markdown for ingestion.

Supported formats:
  Documents : PDF, DOCX, PPTX, XLSX, XLS, EPUB, CSV, JSON, XML, ZIP
  Images    : JPEG, PNG, GIF, WebP  (OCR + optional AI descriptions)
  Audio     : WAV, MP3              (speech transcription via Whisper)
  Video     : YouTube URLs          (transcript extraction)
  Web       : HTTP/HTTPS URLs       (clean text extraction)

Usage:
    python tools/preprocess.py <file_or_url> [output_dir]

    python tools/preprocess.py paper.pdf
    python tools/preprocess.py slides.pptx raw/
    python tools/preprocess.py data.xlsx
    python tools/preprocess.py figure.png
    python tools/preprocess.py recording.mp3
    python tools/preprocess.py https://www.youtube.com/watch?v=VIDEO_ID
    python tools/preprocess.py https://example.com/article

Output is saved to raw/<stem>.md (or raw/<url-slug>.md for URLs).
Install: pip install 'markitdown[all]'
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse


SUPPORTED_EXTENSIONS = {
    # Documents
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".csv", ".json", ".xml", ".epub", ".zip",
    # Images
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    # Audio
    ".wav", ".mp3",
    # Text (pass-through)
    ".md", ".txt", ".html", ".htm",
}


def _slug_from_url(url: str) -> str:
    """Derive a filesystem-safe slug from a URL."""
    parsed = urlparse(url)
    parts = (parsed.netloc + parsed.path).strip("/")
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", parts)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug[:100] or "web-source"


def preprocess(source: str, output_dir: str = "raw", llm_client=None, llm_model: str = "") -> str:
    """
    Convert source file or URL to markdown.

    Args:
        source:     File path or URL to convert.
        output_dir: Directory to write the .md output (default: raw/).
        llm_client: Optional OpenAI-compatible client for AI image descriptions.
        llm_model:  Model name to use with llm_client.

    Returns:
        Path to the output .md file.
    """
    try:
        from markitdown import MarkItDown
    except ImportError:
        print(
            "markitdown is not installed.\n"
            "Run: pip install 'markitdown[all]'\n"
            "Or for specific formats: pip install 'markitdown[pdf,docx,pptx,xlsx,audio-transcription]'",
            file=sys.stderr,
        )
        sys.exit(1)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    is_url = source.startswith(("http://", "https://"))

    # Determine output filename
    if is_url:
        slug = _slug_from_url(source)
        out_file = out_dir / f"{slug}.md"
    else:
        src = Path(source)
        ext = src.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            print(f"Warning: extension '{ext}' may not be supported. Attempting anyway.", file=sys.stderr)
        # Pass-through: plain text / markdown — copy as-is
        if ext in (".md", ".txt"):
            out_file = out_dir / src.name
            out_file.write_text(src.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            print(f"Copied  → {out_file}")
            return str(out_file)
        out_file = out_dir / f"{src.stem}.md"

    # Build MarkItDown instance
    kwargs = {}
    if llm_client:
        kwargs["llm_client"] = llm_client
        kwargs["llm_model"] = llm_model or "claude-sonnet-4-6"
        kwargs["llm_prompt"] = (
            "Describe this image in technical detail. Include: layout, axes labels, "
            "data trends, annotations, color coding, and any text visible. "
            "Be precise — this description will be used for scientific literature indexing."
        )

    md = MarkItDown(**kwargs)

    try:
        result = md.convert(source)
    except Exception as e:
        print(f"Conversion failed for '{source}': {e}", file=sys.stderr)
        sys.exit(1)

    content = result.text_content.strip()
    if not content:
        print(f"Warning: converted output is empty for '{source}'", file=sys.stderr)

    out_file.write_text(content, encoding="utf-8")
    print(f"Converted → {out_file}")
    return str(out_file)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    source = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "raw"

    # Optional: AI-enhanced image descriptions via Anthropic SDK
    llm_client = None
    llm_model = ""
    if "--ai-images" in sys.argv:
        try:
            import anthropic
            from openai import OpenAI
            # Use Anthropic via OpenAI-compatible shim for markitdown
            llm_client = OpenAI(
                api_key=__import__("os").environ.get("ANTHROPIC_API_KEY", ""),
                base_url="https://api.anthropic.com/v1/",
            )
            llm_model = "claude-sonnet-4-6"
        except ImportError:
            print("--ai-images requires: pip install anthropic openai", file=sys.stderr)

    preprocess(source, output_dir, llm_client=llm_client, llm_model=llm_model)


if __name__ == "__main__":
    main()
