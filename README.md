# PW-Wiki

A persistent, compounding knowledge base for materials-science research — maintained by Claude, owned by you.

Focused on metal additive manufacturing (AM), high-entropy alloys (HEA/MPEA), and structural alloy development. Implements [Karpathy's LLM Wiki pattern](https://x.com/karpathy/status/1761467904737067456): instead of re-deriving answers from raw documents every time, Claude builds and maintains a structured, interlinked wiki that grows richer with every source ingested and every question asked.

---

## Structure

```
pw-wiki/
├── raw/              ← Drop source documents here (you own this, Claude never modifies it)
│   └── assets/       ← Images referenced in raw sources
├── wiki/             ← All wiki pages (Claude owns this)
│   ├── index.md      ← Content catalog — every page, one-line summary
│   ├── log.md        ← Append-only operation log
│   ├── overview.md   ← Evolving field synthesis
│   ├── sources/      ← One summary page per ingested source
│   ├── entities/     ← Alloy systems, AM processes, researchers, tools
│   └── concepts/     ← Solidification, microstructure, MLIPs, GNNs, …
├── tools/
│   ├── preprocess.py ← Convert any file format → markdown before ingest
│   └── tests/        ← Offline unit tests for tools
└── CLAUDE.md         ← Schema, operations guide, domain vocabulary
```

---

## Operations

Three operations, triggered by telling Claude what to do:

| Say | Operation | What happens |
|-----|-----------|-------------|
| `ingest <file>` | **Ingest** | Claude reads the source, discusses key takeaways, writes a summary page, updates all entity/concept pages, cross-links everything |
| Ask a question | **Query** | Claude reads the index, synthesizes an answer with citations, offers to file it as a wiki page |
| `lint the wiki` | **Lint** | Claude audits for broken links, orphan pages, contradictions, stale claims, coverage gaps — writes a report |

A single ingest typically touches 8–15 wiki pages.

---

## Supported Source Formats

Drop any file into `raw/` and run the preprocessor if it's not already markdown:

```bash
# One-time install
pip install 'markitdown[all]'

# Convert before ingesting
python tools/preprocess.py raw/paper.pdf          # → raw/paper.md
python tools/preprocess.py raw/slides.pptx        # → raw/slides.md
python tools/preprocess.py raw/data.xlsx          # → raw/data.md
python tools/preprocess.py raw/figure.png --ai-images  # → raw/figure.md (AI description)
python tools/preprocess.py raw/interview.mp3      # → raw/interview.md (transcription)
python tools/preprocess.py https://youtube.com/watch?v=...  # → raw/<slug>.md (transcript)
python tools/preprocess.py https://example.com/article     # → raw/<slug>.md
```

| Category | Formats |
|----------|---------|
| Documents | PDF, DOCX, PPTX, XLSX, XLS, EPUB |
| Data | CSV, JSON, XML, ZIP |
| Images / figures | JPEG, PNG, GIF, WebP — OCR + optional AI descriptions |
| Audio | WAV, MP3 — speech transcribed via Whisper |
| Video | YouTube URLs — transcript extracted |
| Web | Any HTTP/HTTPS URL |
| Plain text | MD, TXT — no conversion needed |

Markdown and plain text files can be dropped directly into `raw/` and ingested without preprocessing.

---

## Wiki Skills

Install the companion skill set for use from any working directory:

```bash
# From wilions/wiki-skills (9 skills)
/plugin install wiki-skills@wilions/wiki-skills
```

| Skill | Purpose |
|-------|---------|
| `wiki-init` | Bootstrap a new wiki |
| `wiki-ingest` | Add a source (file, URL, pasted text) |
| `wiki-query` | Answer a question from wiki content |
| `wiki-lint` | Structural audit — broken links, orphans, contradictions |
| `wiki-update` | Revise existing pages with diff preview |
| `wiki-research` | Parallel 5-angle investigation with anti-bias round |
| `wiki-librarian` | Score all pages: freshness / depth / connectivity |
| `wiki-output` | Export wiki as report, slides, glossary, or timeline |
| `wiki-stats` | Fast metrics dashboard with threshold warnings |

---

## Search

```bash
python tools/search.py "Ti64 fatigue"
python tools/search.py "solidification" wiki/
```

Ranks wiki pages by keyword match count, returns top 10 with snippets.

---

## Wiki Conventions

- All pages use YAML frontmatter: `title`, `type`, `tags`, `sources`, `last_updated`
- Cross-references use Obsidian wiki-link syntax: `[[page-name]]`
- Conflicts are marked: `> ⚠️ **Conflict:** Source A says X; Source B says Y.`
- `raw/` is immutable — Claude reads it but never writes to it
- `wiki/log.md` is append-only — never rewritten, only appended
- `wiki/lint-*.md` files are maintenance artifacts, not knowledge pages

---

## Commit Convention

| Operation | Message format |
|-----------|---------------|
| Ingest | `ingest: <source title>` |
| Query filed | `query: <question slug>` |
| Lint | `lint: YYYY-MM-DD` |
| Schema change | `schema: <what changed>` |
